"""
Step 1 - Data quality audit, exclusions, golden/held-out partition, trajectory
embeddings and exploratory data analysis (public corpora only).

Outputs
  data/interim/frames_clean.csv, multiwoz_clean.csv     dialogue-level features
  data/interim/frames_emb.npy, multiwoz_emb.npy         384-d trajectory embeddings
  outputs/interim/tables/t_quality_audit.csv            missing/duplicate/outlier log
  outputs/interim/tables/t_corpus_descriptives.csv
  outputs/interim/tables/t_slot_completeness.csv
  outputs/interim/figures/fig_eda_turns.png, fig_eda_slots.png
"""

import json
import os
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split

from common import (FIG_DIR, MIN_TURNS, SBERT_MODEL, SEED, TABLE_DIR, TEST_FRACTION, WORK_DIR,
                    embed_dialogues, load_canonical, load_frames_raw)

TIER1 = ["origin_city", "destination_city", "departure_date", "return_date", "duration_nights",
         "traveler_count_adults", "traveler_count_children", "budget_amount", "accommodation_tier"]
TIER2 = ["visa_processing_window_days", "passport_expiry_months", "discount_applied_percentage"]

# Observed-annotation mapping from raw source fields to the canonical Tier-1 schema
FRAMES_MAP = {"origin_city": ["or_city"], "destination_city": ["dst_city"], "departure_date": ["str_date"],
              "return_date": ["end_date"], "duration_nights": ["duration", "max_duration", "min_duration"],
              "traveler_count_adults": ["n_adults"], "traveler_count_children": ["n_children"],
              "budget_amount": ["budget"], "accommodation_tier": ["category", "gst_rating"]}
MWOZ_MAP = {"origin_city": ["train-departure", "taxi-departure"],
            "destination_city": ["train-destination", "taxi-destination"],
            "departure_date": ["train-day", "hotel-bookday"], "return_date": [],
            "duration_nights": ["hotel-bookstay"],
            "traveler_count_adults": ["hotel-bookpeople", "train-bookpeople"], "traveler_count_children": [],
            "budget_amount": ["hotel-pricerange"], "accommodation_tier": ["hotel-stars"]}


def frames_observed_keys(raw):
    ks = set()
    for t in raw["turns"]:
        for a in t["labels"]["acts"]:
            for arg in a.get("args", []):
                if "val" in arg:
                    ks.add(arg["key"])
    return ks


def load_multiwoz_raw_keys():
    import glob
    from common import ROOT
    out = {}
    for fp in glob.glob(os.path.join(ROOT, "data", "raw", "multiwoz22", "**", "dialogues_*.json"), recursive=True):
        with open(fp) as f:
            for d in json.load(f):
                ks = set()
                for t in d["turns"]:
                    for fr in t.get("frames", []):
                        ks |= set((fr.get("state") or {}).get("slot_values", {}).keys())
                out["mwoz_" + d["dialogue_id"]] = ks
    return out

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                     "font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11})


def wizard_request_stats(raw_turns):
    """Count agent request acts and redundant requests (slot already informed by the user)."""
    informed, n_agent, n_req, n_redundant = set(), 0, 0, 0
    for t in raw_turns:
        acts = t["labels"]["acts"]
        if t["author"] == "user":
            for a in acts:
                if a["name"] in ("inform", "switch_frame"):
                    for arg in a.get("args", []):
                        if "val" in arg and arg.get("key") not in ("intent", "ref"):
                            informed.add(arg["key"])
        else:
            n_agent += 1
            req_keys = [arg["key"] for a in acts if a["name"] == "request" for arg in a.get("args", [])]
            if req_keys:
                n_req += 1
                if any(k in informed for k in req_keys):
                    n_redundant += 1
    return n_agent, n_req, n_redundant


def dialogue_frame(dialogues, frames_raw=None, mwoz_keys=None):
    rows = []
    for d in dialogues:
        turns = d.get("turns", [])
        u_len = [len(t["utterance"].split()) for t in turns if t["speaker"] == "user"]
        a_len = [len(t["utterance"].split()) for t in turns if t["speaker"] != "user"]
        row = dict(dialogue_id=d["dialogue_id"], source=d["source_dataset"], total_turns=len(turns),
                   user_turns=sum(t["speaker"] == "user" for t in turns),
                   agent_turns=sum(t["speaker"] != "user" for t in turns),
                   empty_utterances=sum(1 for t in turns if not str(t.get("utterance", "")).strip()),
                   mean_user_words=np.mean(u_len) if u_len else np.nan,
                   mean_agent_words=np.mean(a_len) if a_len else np.nan,
                   revisions=d.get("revisions_count", 0), hesitations=d.get("hesitation_markers_count", 0),
                   budget_specified=bool(d.get("budget_specified", False)),
                   text_hash=hash(" || ".join(t["utterance"].strip().lower() for t in turns)))
        if frames_raw is not None and d["dialogue_id"] in frames_raw:
            keys, mapping = frames_observed_keys(frames_raw[d["dialogue_id"]]), FRAMES_MAP
        else:
            keys, mapping = (mwoz_keys or {}).get(d["dialogue_id"].replace(".json", "") + ".json", set()), MWOZ_MAP
            if not keys:
                keys = (mwoz_keys or {}).get(d["dialogue_id"], set())
        for s in TIER1:
            row[f"has_{s}"] = any(k in keys for k in mapping[s])
        for s in TIER2:
            row[f"has_{s}"] = False  # not annotated in either public corpus
        if frames_raw is not None and d["dialogue_id"] in frames_raw:
            r = frames_raw[d["dialogue_id"]]
            lab = r.get("labels", {})
            row["task_success"] = lab.get("wizardSurveyTaskSuccessful")
            row["user_rating"] = lab.get("userSurveyRating")
            n_agent, n_req, n_red = wizard_request_stats(r["turns"])
            row.update(agent_request_turns=n_req, redundant_requests=n_red,
                       rer_proxy=(n_red / n_agent) if n_agent else np.nan,
                       offers=sum(1 for t in r["turns"] if t["author"] == "wizard"
                                  for a in t["labels"]["acts"] if a["name"] == "offer"))
        rows.append(row)
    return pd.DataFrame(rows)


def audit(df, name):
    q = df["total_turns"].quantile([0.25, 0.75]).values
    iqr = q[1] - q[0]
    hi = q[1] + 1.5 * iqr
    rec = dict(corpus=name, n_raw=len(df),
               duplicate_ids=int(df["dialogue_id"].duplicated().sum()),
               duplicate_text=int(df["text_hash"].duplicated().sum()),
               dialogues_with_empty_utterance=int((df["empty_utterances"] > 0).sum()),
               excluded_lt_min_turns=int((df["total_turns"] < MIN_TURNS).sum()),
               turn_outliers_iqr=int((df["total_turns"] > hi).sum()), outlier_threshold=float(hi))
    if "task_success" in df:
        rec["missing_task_success_label"] = int(df["task_success"].isna().sum())
        rec["missing_user_rating"] = int(df["user_rating"].isna().sum())
    return rec


def main():
    frames_raw = load_frames_raw()
    can = load_canonical(("frames", "multiwoz"))
    fr = [d for d in can if d["source_dataset"] == "frames"]
    mw = [d for d in can if d["source_dataset"] == "multiwoz"]
    df_fr, df_mw = dialogue_frame(fr, frames_raw), dialogue_frame(mw, mwoz_keys=load_multiwoz_raw_keys())

    audits = [audit(df_fr, "Microsoft Frames"), audit(df_mw, "MultiWOZ 2.2 (travel-service sample)")]

    def clean(df, dialogues):
        keep = (df["total_turns"] >= MIN_TURNS) & (~df["text_hash"].duplicated()) & (~df["dialogue_id"].duplicated())
        df2 = df[keep].reset_index(drop=True)
        ids = set(df2["dialogue_id"])
        return df2, [d for d in dialogues if d["dialogue_id"] in ids]

    df_fr, fr = clean(df_fr, fr)
    df_mw, mw = clean(df_mw, mw)
    for a, df in zip(audits, (df_fr, df_mw)):
        a["n_analytic"] = len(df)
    pd.DataFrame(audits).to_csv(os.path.join(TABLE_DIR, "t_quality_audit.csv"), index=False)

    # Golden / held-out partition of Frames, stratified on the task-success label
    strat = df_fr["task_success"].fillna("unknown").astype(str)
    idx_gold, idx_test = train_test_split(np.arange(len(df_fr)), test_size=TEST_FRACTION,
                                          random_state=SEED, stratify=strat)
    df_fr["partition"] = "test"
    df_fr.loc[idx_gold, "partition"] = "gold"
    df_fr["retrieval_pool"] = (df_fr["partition"] == "gold") & (df_fr["task_success"] == True)

    # Embeddings (de-lexicalised, corpus-neutral speaker tags)
    model = SentenceTransformer(SBERT_MODEL)
    order_fr = {d["dialogue_id"]: d for d in fr}
    order_mw = {d["dialogue_id"]: d for d in mw}
    X_fr = embed_dialogues(model, [order_fr[i] for i in df_fr["dialogue_id"]], frames_raw)
    X_mw = embed_dialogues(model, [order_mw[i] for i in df_mw["dialogue_id"]])
    np.save(os.path.join(WORK_DIR, "frames_emb.npy"), X_fr)
    np.save(os.path.join(WORK_DIR, "multiwoz_emb.npy"), X_mw)
    df_fr.drop(columns=["text_hash"]).to_csv(os.path.join(WORK_DIR, "frames_clean.csv"), index=False)
    df_mw.drop(columns=["text_hash"]).to_csv(os.path.join(WORK_DIR, "multiwoz_clean.csv"), index=False)

    # Descriptives
    def desc(df, name):
        return dict(corpus=name, N=len(df), turns_M=df.total_turns.mean(), turns_SD=df.total_turns.std(),
                    turns_Mdn=df.total_turns.median(), turns_min=df.total_turns.min(), turns_max=df.total_turns.max(),
                    user_words_M=df.mean_user_words.mean(), agent_words_M=df.mean_agent_words.mean(),
                    budget_pct=100 * df.budget_specified.mean(),
                    success_pct=100 * df["task_success"].eq(True).mean() if "task_success" in df else np.nan)
    descs = [desc(df_fr, "Microsoft Frames"), desc(df_mw, "MultiWOZ 2.2")]
    descs.append(desc(df_fr[df_fr.partition == "gold"], "Frames golden partition (D_gold)"))
    descs.append(desc(df_fr[df_fr.partition == "test"], "Frames held-out partition (D_test)"))
    pd.DataFrame(descs).to_csv(os.path.join(TABLE_DIR, "t_corpus_descriptives.csv"), index=False)

    comp = []
    for s in TIER1 + TIER2:
        comp.append(dict(slot=s, tier="Tier 1" if s in TIER1 else "Tier 2",
                         frames_pct=100 * df_fr[f"has_{s}"].mean(), multiwoz_pct=100 * df_mw[f"has_{s}"].mean()))
    df_comp = pd.DataFrame(comp)
    df_comp.to_csv(os.path.join(TABLE_DIR, "t_slot_completeness.csv"), index=False)

    # Figure: turn-length distributions
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)
    bins = np.arange(0, 50, 2)
    axes[0].hist(df_fr.total_turns, bins=bins, alpha=0.75, label="Microsoft Frames", color="#4c72b0")
    axes[0].hist(df_mw.total_turns, bins=bins, alpha=0.6, label="MultiWOZ 2.2", color="#dd8452")
    axes[0].set_xlabel("Turns per dialogue")
    axes[0].set_ylabel("Number of dialogues")
    axes[0].set_title("A. Dialogue length")
    axes[0].legend(frameon=False)
    axes[1].boxplot([df_fr.mean_user_words.dropna(), df_fr.mean_agent_words.dropna(),
                     df_mw.mean_user_words.dropna(), df_mw.mean_agent_words.dropna()],
                    labels=["Frames\nuser", "Frames\nagent", "MultiWOZ\nuser", "MultiWOZ\nagent"],
                    showfliers=False)
    axes[1].set_ylabel("Mean words per utterance")
    axes[1].set_title("B. Utterance length by speaker")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_eda_turns.png"))
    plt.close(fig)

    # Figure: slot completeness
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    x = np.arange(len(df_comp))
    ax.bar(x - 0.2, df_comp.frames_pct, 0.4, label="Microsoft Frames", color="#4c72b0")
    ax.bar(x + 0.2, df_comp.multiwoz_pct, 0.4, label="MultiWOZ 2.2", color="#dd8452")
    ax.set_xticks(x)
    ax.set_xticklabels([s.replace("_", "\n") for s in df_comp.slot], fontsize=8)
    ax.set_ylabel("Dialogues with slot populated (%)")
    ax.set_ylim(0, 105)
    ax.axvline(len(TIER1) - 0.5, color="grey", ls="--", lw=1)
    ax.text(len(TIER1) - 0.4, 98, "Tier 2 (policy) slots", fontsize=9, va="top")
    ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1.0, 0.88))
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_eda_slots.png"))
    plt.close(fig)

    summary = dict(audits=audits, n_gold=int((df_fr.partition == "gold").sum()),
                   n_test=int((df_fr.partition == "test").sum()),
                   n_retrieval_pool=int(df_fr.retrieval_pool.sum()))
    with open(os.path.join(WORK_DIR, "step1_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=float)
    print(json.dumps(summary, indent=2, default=float))
    print(pd.DataFrame(descs).round(2).to_string(index=False))
    print(df_comp.round(1).to_string(index=False))


if __name__ == "__main__":
    main()
