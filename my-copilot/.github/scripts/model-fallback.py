#!/usr/bin/env python3
"""Detect rate-limit errors and suggest model fallback."""
import json, os, sys, datetime, re

os.makedirs("logs", exist_ok=True)

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

err = d.get("error") or {}
msg = (err.get("message") or "") + " " + (err.get("name") or "")

# Detect rate-limit / provider errors
RATE_PATTERNS = [r'\b429\b', r'\b503\b', r'\b529\b',
                 r'rate.?limit', r'overloaded', r'capacity',
                 r'too many requests', r'service unavailable']
hit = any(re.search(p, msg, re.IGNORECASE) for p in RATE_PATTERNS)
if not hit:
    sys.exit(0)

# Extract model from error context if available
model = d.get("model") or d.get("context", {}).get("model") or "unknown"

FALLBACK_MAP = {
    "claude-opus-4.6": "claude-sonnet-4.6",
    "claude-opus-4.5": "claude-sonnet-4.5",
    "claude-sonnet-4.6": "claude-haiku-4.5",
    "claude-sonnet-4.5": "claude-haiku-4.5",
    "gpt-5.3-codex": "gpt-5.2-codex",
    "gpt-5.2-codex": "gpt-5.1-codex",
    "gemini-3-pro-preview": "gpt-5.1-codex",
}

suggestion = FALLBACK_MAP.get(model, "claude-sonnet-4.6")

out = {
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "originalModel": model,
    "suggestedFallback": suggestion,
    "errorSnippet": msg[:200].strip(),
}

with open("logs/model-fallback.jsonl", "a") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")

print(f"⚠️ Rate limit hit on {model}. Try: --model {suggestion}")
