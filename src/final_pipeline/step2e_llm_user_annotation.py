"""
Step 2e - LLM behavioural annotation of the USER in every Frames dialogue (Gemini).

Gemini reads the whole conversation (for context) but rates only the user's behaviour against a
fixed codebook (below). Output is constrained to a JSON schema, temperature 0, internal reasoning
disabled. Results are cached in data/interim/llm_user_annotations.jsonl and the script resumes.

Reliability: a random subsample of 100 dialogues is annotated a second time at temperature 0.7
(--retest); agreement per field is computed in step 2f.

The client is created in Gemini API mode with the key from capstone/.env; shell-level Google
Cloud / Vertex settings are never used. Public data only (Microsoft Frames).
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import List

import numpy as np
import pandas as pd
from dotenv import dotenv_values
from pydantic import BaseModel, Field

from common import ROOT, SEED, WORK_DIR, load_frames_raw

MODEL = "gemini-2.5-flash"
OUT = os.path.join(WORK_DIR, "llm_user_annotations.jsonl")
OUT_RETEST = os.path.join(WORK_DIR, "llm_user_annotations_retest.jsonl")
N_RETEST = 100


class Goal(str, Enum):
    explore_destinations = "explore_destinations"
    price_shopping = "price_shopping"
    specific_trip_booking = "specific_trip_booking"
    compare_options = "compare_options"
    information_only = "information_only"
    other = "other"


class Tone(str, Enum):
    positive = "positive"
    neutral = "neutral"
    impatient = "impatient"
    frustrated = "frustrated"


class Outcome(str, Enum):
    booked = "booked"
    no_suitable_option = "no_suitable_option"
    undecided_or_left = "undecided_or_left"
    unclear = "unclear"


class Party(str, Enum):
    solo = "solo"
    couple = "couple"
    family = "family"
    group = "group"
    business = "business"
    unknown = "unknown"


class UserBehaviour(BaseModel):
    primary_goal: Goal = Field(description="The user's main purpose in this conversation")
    secondary_goals: List[Goal] = Field(description="Other purposes that are clearly present (may be empty)")
    price_sensitivity: int = Field(ge=1, le=5, description="1 = price never matters, 5 = price dominates every decision")
    destination_flexibility: int = Field(ge=1, le=5, description="1 = one fixed destination, 5 = open to anywhere")
    date_flexibility: int = Field(ge=1, le=5, description="1 = fixed dates, 5 = fully flexible dates")
    exploration_breadth: int = Field(ge=1, le=5, description="1 = considers a single option, 5 = considers many alternatives")
    decisiveness: int = Field(ge=1, le=5, description="1 = hesitant / cannot decide, 5 = decides quickly and firmly")
    detail_orientation: int = Field(ge=1, le=5, description="1 = no interest in specifics, 5 = asks about many details (amenities, ratings, times)")
    information_upfront: int = Field(ge=1, le=5, description="1 = reveals requirements bit by bit, 5 = states all requirements in the first message")
    revision_tendency: int = Field(ge=1, le=5, description="1 = never changes requirements, 5 = changes requirements repeatedly")
    question_asking: int = Field(ge=1, le=5, description="1 = asks no questions, 5 = asks many questions")
    politeness: int = Field(ge=1, le=5, description="1 = curt or rude, 5 = very polite")
    emotional_tone: Tone
    outcome: Outcome
    party_type: Party
    unusual_conversation: bool = Field(description="True only if the conversation is off-task, nonsensical, or does not resemble a normal travel-booking request")


INSTRUCTION = (
    "You are an expert annotator of customer behaviour in travel-agency conversations. Read the whole "
    "conversation between a USER (customer) and an AGENT, then rate ONLY THE USER's behaviour using the "
    "codebook in the response schema. Base every rating on evidence in the user's messages; use the agent's "
    "messages only as context. Use the full 1-5 range when warranted; 3 means moderate or mixed."
)


def conversation_text(raw):
    return "\n".join(f"{'USER' if t['author'] == 'user' else 'AGENT'}: {t['text']}" for t in raw["turns"])


def truncate(turns, max_user):
    """Keep turns up to and including the max_user-th user message (the agent reply after it is dropped)."""
    out, n = [], 0
    for t in turns:
        if t["author"] == "user":
            if n == max_user:
                break
            n += 1
        elif n == max_user:
            break
        out.append(t)
    return out


def main(retest=False, max_user=0):
    from google import genai
    from google.genai import types
    key = dotenv_values(os.path.join(ROOT, ".env")).get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY missing from capstone/.env")
    client = genai.Client(api_key=key, vertexai=False)
    df = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    raw = load_frames_raw()
    ids = list(df.dialogue_id)
    out, temp = OUT, 0.0
    if retest:
        ids = list(np.random.default_rng(SEED).choice(ids, N_RETEST, replace=False))
        out, temp = OUT_RETEST, 0.7
    if max_user:
        out = os.path.join(WORK_DIR, f"llm_user_annotations_u{max_user}.jsonl")
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["dialogue_id"] for l in open(out) if l.strip()}
    if max_user and not os.path.exists(out):
        # dialogues that are not shortened by the cut-off have identical input text: reuse the full annotation
        full = {json.loads(l)["dialogue_id"]: json.loads(l) for l in open(OUT) if l.strip()}
        with open(out, "w") as f:
            for did in ids:
                if len(truncate(raw[did]["turns"], max_user)) == len(raw[did]["turns"]) and did in full:
                    f.write(json.dumps(dict(full[did], reused_full=True)) + "\n")
                    done.add(did)
    todo = [i for i in ids if i not in done]
    print(f"{len(ids)} dialogues, {len(todo)} to annotate (temperature {temp}, max_user={max_user})", flush=True)
    cfg = types.GenerateContentConfig(
        temperature=temp, seed=SEED, system_instruction=INSTRUCTION, max_output_tokens=600,
        response_mime_type="application/json", response_schema=UserBehaviour,
        thinking_config=types.ThinkingConfig(thinking_budget=0))

    def run(did):
        err = None
        for attempt in range(12):
            try:
                turns = raw[did]["turns"] if not max_user else truncate(raw[did]["turns"], max_user)
                r = client.models.generate_content(model=MODEL, contents=conversation_text({"turns": turns}),
                                                   config=cfg)
                obj = UserBehaviour.model_validate_json(r.text)
                return dict(dialogue_id=did, model=MODEL, temperature=temp,
                            finish_reason=str(r.candidates[0].finish_reason), **json.loads(obj.model_dump_json()))
            except Exception as e:
                err = str(e)[:120]
                time.sleep(min(60, 2 ** attempt))
        return dict(dialogue_id=did, model=MODEL, temperature=temp, error=err)

    t0, n = time.time(), 0
    with open(out, "a") as f, ThreadPoolExecutor(max_workers=6) as ex:
        for rec in ex.map(run, todo):
            f.write(json.dumps(rec) + "\n")
            f.flush()
            n += 1
            if n % 100 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)} ({time.time() - t0:.0f}s)", flush=True)
    recs = [json.loads(l) for l in open(out) if l.strip()]
    print(f"saved {len(recs)} records; errors: {sum('error' in r for r in recs)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--retest", action="store_true")
    ap.add_argument("--max-user-msgs", type=int, default=0,
                    help="annotate only up to the M-th user message (agent reply after it excluded)")
    ap.add_argument("--pilot", type=int, default=0, help="annotate only the first N dialogues and print them")
    a = ap.parse_args()
    if a.pilot:
        OUT = os.path.join(WORK_DIR, "llm_user_annotations_pilot.jsonl")
        _ids = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv")).dialogue_id[:a.pilot]
        _orig = pd.read_csv
        pd.read_csv = lambda *x, **k: _orig(*x, **k).head(a.pilot)
        main()
        for l in open(OUT):
            print(l.strip())
    else:
        main(a.retest, a.max_user_msgs)
