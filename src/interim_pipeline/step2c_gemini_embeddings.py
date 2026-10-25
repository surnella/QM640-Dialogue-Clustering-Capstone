"""
Step 2c - Gemini embeddings (gemini-embedding-001, task_type = CLUSTERING) for Frames.

Embeds, with the same de-lexicalised, speaker-tagged text used for MiniLM:
  * every individual turn                    -> pooled later exactly like the MiniLM vectors
  * every whole conversation as one document (user + agent, and user turns only)
  * whole-conversation prefixes of N = 3, 5, 7, 10 turns (both versions) for early-routing tests

Results are cached in data/embeddings/ (git-ignored) so the paid API is called only once;
the script resumes from the cache if interrupted.

The client is created explicitly in Gemini API mode with the key from capstone/.env, so
shell-level Google Cloud / Vertex settings are never used.
"""

import hashlib
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from dotenv import dotenv_values

from common import ROOT, WORK_DIR, delexicalize, dialogue_slot_values, load_canonical, load_frames_raw, speaker_tag

MODEL = "gemini-embedding-001"
TASK = "CLUSTERING"
BATCH = 100
DOC_N = (3, 5, 7, 10)
EMB_DIR = os.path.join(ROOT, "data", "embeddings", "gemini")
CACHE = os.path.join(EMB_DIR, "cache")
os.makedirs(CACHE, exist_ok=True)


def h(t):
    return hashlib.sha1(t.encode("utf-8")).hexdigest()


def build_texts():
    df = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    raw = load_frames_raw()
    can = {d["dialogue_id"]: d for d in load_canonical(("frames",))}
    turns, docs = [], {}
    for did in df.dialogue_id:
        d = can[did]
        sv = dialogue_slot_values(d, raw)
        tx = [f"{speaker_tag(t.get('speaker'))}: {delexicalize(t.get('utterance', ''), sv)}" for t in d["turns"]]
        turns.append(tx)
        docs[("full", None, did)] = "\n".join(tx)
        docs[("user", None, did)] = "\n".join(x for x in tx if x.startswith("USER:")) or tx[0]
        for n in DOC_N:
            docs[("full", n, did)] = "\n".join(tx[:n])
            docs[("user", n, did)] = "\n".join(x for x in tx[:n] if x.startswith("USER:")) or tx[0]
    return df, turns, docs


def main():
    from google import genai
    from google.genai import types
    key = dotenv_values(os.path.join(ROOT, ".env")).get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY missing from capstone/.env")
    client = genai.Client(api_key=key, vertexai=False)
    cfg = types.EmbedContentConfig(task_type=TASK)

    df, turns, docs = build_texts()
    uniq = sorted({t for tx in turns for t in tx} | set(docs.values()))
    batches = [uniq[i:i + BATCH] for i in range(0, len(uniq), BATCH)]
    todo = [i for i in range(len(batches)) if not os.path.exists(os.path.join(CACHE, f"b{i:05d}.npy"))]
    n_chars = sum(len(t) for t in uniq)
    print(f"{len(uniq)} unique texts, {len(batches)} batches ({len(todo)} to do), ~{n_chars / 4 / 1e6:.2f}M tokens",
          flush=True)

    def run(i):
        for attempt in range(15):
            try:
                r = client.models.embed_content(model=MODEL, contents=batches[i], config=cfg)
                E = np.array([e.values for e in r.embeddings], dtype=np.float32)
                assert E.shape[0] == len(batches[i])
                np.save(os.path.join(CACHE, f"b{i:05d}.npy"), E)
                with open(os.path.join(CACHE, f"b{i:05d}.json"), "w") as f:
                    json.dump([h(t) for t in batches[i]], f)
                return i
            except Exception as e:
                wait = min(60, 2 ** attempt)
                print(f"batch {i} attempt {attempt + 1} failed ({str(e)[:90]}); retry in {wait}s", flush=True)
                time.sleep(wait)
        raise RuntimeError(f"batch {i} failed permanently")

    t0, done = time.time(), 0
    with ThreadPoolExecutor(max_workers=2) as ex:
        for _ in ex.map(run, todo):
            done += 1
            if done % 20 == 0 or done == len(todo):
                print(f"  {done}/{len(todo)} batches ({time.time() - t0:.0f}s)", flush=True)

    # ---- assemble -------------------------------------------------------------------------
    lookup = {}
    for i in range(len(batches)):
        E = np.load(os.path.join(CACHE, f"b{i:05d}.npy"))
        for t, v in zip(batches[i], E):
            lookup[t] = v
    dim = len(next(iter(lookup.values())))
    flat = np.array([lookup[t] for tx in turns for t in tx], dtype=np.float32)
    offsets = np.cumsum([0] + [len(tx) for tx in turns])
    np.save(os.path.join(EMB_DIR, "turn_emb.npy"), flat)
    np.save(os.path.join(EMB_DIR, "turn_offsets.npy"), offsets)
    for kind in ("full", "user"):
        for n in (None,) + DOC_N:
            M = np.array([lookup[docs[(kind, n, did)]] for did in df.dialogue_id], dtype=np.float32)
            np.save(os.path.join(EMB_DIR, f"doc_{kind}_{'all' if n is None else n}.npy"), M)
    meta = dict(model=MODEL, task_type=TASK, dim=dim, n_dialogues=len(df), n_turns=int(offsets[-1]),
                n_unique_texts=len(uniq), n_batches=len(batches), approx_tokens=int(n_chars / 4),
                dialogue_order="data/interim/frames_clean.csv")
    with open(os.path.join(EMB_DIR, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
