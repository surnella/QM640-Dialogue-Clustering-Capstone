"""
Shared cached Gemini LLM harness for the final-report pipeline (`src/final_pipeline/`).

Features:
  - Reads GEMINI_API_KEY from `capstone/.env` or environment variables.
  - Supports `gemini-2.5-flash` (primary travel-agent model under test) and
    `gemini-2.5-pro` (independent second LLM judge for cross-model reliability).
  - Persists every response immediately to a JSONL cache keyed by `key_id` so interrupted
    runs resume with zero duplicate API calls.
  - Supports both plain-text generation and Pydantic-constrained structured JSON outputs.
"""

import json
import os
import threading
import time
from typing import Any, Dict, Optional, Type
from dotenv import dotenv_values
from pydantic import BaseModel

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FINAL_DATA_DIR = os.path.join(ROOT, "data", "final")
FINAL_OUT_DIR = os.path.join(ROOT, "outputs", "final")
FINAL_TABLE_DIR = os.path.join(FINAL_OUT_DIR, "tables")
FINAL_FIG_DIR = os.path.join(FINAL_OUT_DIR, "figures")

for _d in (FINAL_DATA_DIR, FINAL_OUT_DIR, FINAL_TABLE_DIR, FINAL_FIG_DIR):
    os.makedirs(_d, exist_ok=True)

SEED = 42
PRIMARY_AGENT_MODEL = "gemini-2.5-flash"
PRIMARY_JUDGE_MODEL = "gemini-2.5-flash"
SECOND_JUDGE_MODEL = "gemini-2.5-pro"


def load_gemini_api_key() -> str:
    """Load GEMINI_API_KEY from environment or capstone/.env."""
    key = os.environ.get("GEMINI_API_KEY")
    env_path = os.path.join(ROOT, ".env")
    if not key and os.path.exists(env_path):
        vals = dotenv_values(env_path)
        key = vals.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not found in environment or capstone/.env")
    return key.strip()


class CachedLLMClient:
    """Resumable JSONL-cached wrapper around `google.genai.Client`."""

    def __init__(self, cache_path: str):
        self.cache_path = cache_path
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(os.path.abspath(cache_path)), exist_ok=True)
        self.cache: Dict[str, Dict[str, Any]] = {}
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        if "key_id" in rec and rec.get("error") is None:
                            self.cache[str(rec["key_id"])] = rec
                    except json.JSONDecodeError:
                        continue
        self._local = threading.local()

    @property
    def client(self):
        if not hasattr(self._local, "client") or self._local.client is None:
            from google import genai
            self._local.client = genai.Client(api_key=load_gemini_api_key(), vertexai=False)
        return self._local.client

    def _append_record(self, rec: Dict[str, Any]) -> None:
        with self._lock:
            with open(self.cache_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
            if rec.get("error") is None:
                self.cache[str(rec["key_id"])] = rec

    def generate_text(
        self,
        key_id: str,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: str = PRIMARY_AGENT_MODEL,
        temperature: float = 0.2,
        max_output_tokens: int = 350,
        seed: int = SEED,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate a single text completion (or return from JSONL cache)."""
        if key_id in self.cache:
            return self.cache[key_id]

        from google.genai import types
        cfg_kwargs: Dict[str, Any] = dict(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            seed=seed,
        )
        if system_instruction:
            cfg_kwargs["system_instruction"] = system_instruction
        if "flash" in model:
            cfg_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=0)

        text, finish, err = None, None, None
        for attempt in range(6):
            try:
                resp = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(**cfg_kwargs),
                )
                text = (resp.text or "").strip()
                finish = str(resp.candidates[0].finish_reason) if resp.candidates else None
                if text:
                    err = None
                    break
                err = f"Empty response (finish={finish})"
            except Exception as e:
                err = str(e)
            time.sleep(min(30, (2 ** attempt) * 1.5))

        rec = dict(
            key_id=key_id,
            model=model,
            temperature=temperature,
            response=text,
            finish_reason=finish,
            error=err,
            **(metadata or {}),
        )
        self._append_record(rec)
        return rec

    def generate_json(
        self,
        key_id: str,
        prompt: str,
        schema_cls: Type[BaseModel],
        system_instruction: Optional[str] = None,
        model: str = PRIMARY_JUDGE_MODEL,
        temperature: float = 0.0,
        max_output_tokens: int = 600,
        seed: int = SEED,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate a structured JSON response conforming to `schema_cls` (or return from cache)."""
        if key_id in self.cache:
            return self.cache[key_id]

        from google.genai import types
        cfg_kwargs: Dict[str, Any] = dict(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            seed=seed,
            response_mime_type="application/json",
            response_schema=schema_cls,
        )
        if system_instruction:
            cfg_kwargs["system_instruction"] = system_instruction
        if "flash" in model:
            cfg_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
        elif "pro" in model:
            cfg_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=128)

        parsed_dict, err = None, None
        for attempt in range(6):
            try:
                resp = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(**cfg_kwargs),
                )
                raw_text = (resp.text or "").strip()
                if raw_text:
                    obj = schema_cls.model_validate_json(raw_text)
                    parsed_dict = obj.model_dump()
                    err = None
                    break
                err = "Empty JSON response"
            except Exception as e:
                err = str(e)
            time.sleep(min(30, (2 ** attempt) * 1.5))

        rec = dict(
            key_id=key_id,
            model=model,
            temperature=temperature,
            parsed=parsed_dict,
            error=err,
            **(metadata or {}),
        )
        self._append_record(rec)
        return rec

