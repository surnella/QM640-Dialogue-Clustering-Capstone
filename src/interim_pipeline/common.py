"""
Shared utilities for the interim-report analysis pipeline.

All steps in ``src/interim_pipeline`` use only the two public corpora
(Microsoft Frames and MultiWOZ 2.2). No enterprise or proprietary data is read.
"""

import json
import os
import re
from typing import Dict, List

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANONICAL_JSON = os.path.join(ROOT, "data", "canonical", "canonical_dialogues.json")
FRAMES_RAW_JSON = os.path.join(ROOT, "data", "raw", "frames", "Frames-dataset", "frames.json")
OUT_DIR = os.path.join(ROOT, "outputs", "interim")
TABLE_DIR = os.path.join(OUT_DIR, "tables")
FIG_DIR = os.path.join(OUT_DIR, "figures")
WORK_DIR = os.path.join(ROOT, "data", "interim")

SEED = 42
DECAY_LAMBDA = 0.15          # w_t = exp(-lambda (T - t)) / sum_j exp(-lambda (T - j))
MIN_TURNS = 3                # inclusion criterion: at least three turns
TEST_FRACTION = 0.30         # 70 / 30 golden / held-out partition
SBERT_MODEL = "all-MiniLM-L6-v2"

ARCHETYPE_ORDER: List[str] = []  # populated by step 2 (see archetypes.json)

for _d in (TABLE_DIR, FIG_DIR, WORK_DIR):
    os.makedirs(_d, exist_ok=True)


def load_canonical(sources=("frames", "multiwoz")) -> List[Dict]:
    """Load canonical dialogues for the requested public sources only."""
    with open(CANONICAL_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [d for d in data if d.get("source_dataset") in sources]


def load_frames_raw() -> Dict[str, Dict]:
    """Return raw Frames records keyed by canonical dialogue id (``frames_<id>``)."""
    with open(FRAMES_RAW_JSON, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {f"frames_{r['id']}": r for r in raw}


def decay_weights(n_turns: int, lam: float = DECAY_LAMBDA) -> np.ndarray:
    """Exponential recency weights that emphasise later (negotiation-closing) turns."""
    if n_turns <= 1:
        return np.ones(1)
    t = np.arange(1, n_turns + 1)
    w = np.exp(-lam * (n_turns - t))
    return w / w.sum()


_NUM_RE = re.compile(r"\b\d[\d,.:/]*\b")


def _collect_values(obj, key_hint="SLOT", out=None):
    """Recursively collect (value, key) pairs from nested slot structures."""
    if out is None:
        out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            _collect_values(v, k, out)
    elif isinstance(obj, list):
        for v in obj:
            _collect_values(v, key_hint, out)
    elif isinstance(obj, (str, int, float)) and not isinstance(obj, bool):
        s = str(obj).strip()
        if len(s) >= 3 and not s.lower() in {"true", "false", "none", "yes", "no", "dontcare"}:
            out.append((s, str(key_hint)))
    return out


def dialogue_slot_values(dialogue: Dict, frames_raw: Dict[str, Dict] = None) -> List[tuple]:
    """All entity values mentioned in a dialogue (canonical slots plus raw Frames act args)."""
    vals = []
    for t in dialogue.get("turns", []):
        vals.extend(_collect_values(t.get("slots_mentioned", {})))
    if frames_raw is not None and dialogue["dialogue_id"] in frames_raw:
        for rt in frames_raw[dialogue["dialogue_id"]]["turns"]:
            for act in rt["labels"]["acts"]:
                for a in act.get("args", []):
                    if "val" in a and a.get("key") not in ("intent", "action", "ref", "read", "write"):
                        vals.extend(_collect_values(a["val"], a.get("key", "SLOT")))
    # longest first so that multi-word values are replaced before sub-strings
    uniq = {}
    for v, k in vals:
        uniq.setdefault(v, k)
    return sorted(uniq.items(), key=lambda x: -len(x[0]))


def delexicalize(text: str, slot_values: List[tuple]) -> str:
    """Replace entity values with canonical slot tokens and numbers with [NUM]."""
    out = text
    for val, key in slot_values:
        if _NUM_RE.fullmatch(val):
            continue
        out = re.sub(re.escape(val), f"[{key.upper()}]", out, flags=re.IGNORECASE)
    out = _NUM_RE.sub("[NUM]", out)
    return out


def speaker_tag(speaker: str) -> str:
    """Corpus-neutral speaker tag (Frames 'wizard' and MultiWOZ 'system' both become AGENT)."""
    return "USER" if str(speaker).lower() == "user" else "AGENT"


def turn_texts(dialogue: Dict, slot_values: List[tuple], max_turns: int = None) -> List[str]:
    turns = dialogue.get("turns", [])
    if max_turns is not None:
        turns = turns[:max_turns]
    return [f"{speaker_tag(t.get('speaker'))}: {delexicalize(t.get('utterance', ''), slot_values)}"
            for t in turns]


def embed_dialogues(model, dialogues: List[Dict], frames_raw=None, max_turns: int = None,
                    batch_size: int = 64) -> np.ndarray:
    """Decay-weighted mean of S-BERT turn embeddings, L2-normalised (384-d)."""
    all_texts, spans = [], []
    for d in dialogues:
        sv = dialogue_slot_values(d, frames_raw)
        tx = turn_texts(d, sv, max_turns=max_turns)
        spans.append((len(all_texts), len(tx)))
        all_texts.extend(tx)
    embs = model.encode(all_texts, batch_size=batch_size, show_progress_bar=False,
                        convert_to_numpy=True, normalize_embeddings=False)
    out = np.zeros((len(dialogues), embs.shape[1]), dtype=np.float32)
    for i, (s, n) in enumerate(spans):
        w = decay_weights(n)
        v = (embs[s:s + n] * w[:, None]).sum(axis=0)
        out[i] = v / (np.linalg.norm(v) + 1e-12)
    return out


def apa_num(x: float, digits: int = 2, leading_zero: bool = True) -> str:
    """APA numeric formatting; drop the leading zero for statistics bounded by 1."""
    s = f"{x:.{digits}f}"
    if not leading_zero:
        if s.startswith("0."):
            s = s[1:]
        elif s.startswith("-0."):
            s = "-" + s[2:]
    return s


def apa_p(p: float) -> str:
    return "< .001" if p < 0.001 else "= " + apa_num(p, 3, leading_zero=False)
