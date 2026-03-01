#!/usr/bin/env python3
"""Log error events to logs/errors.jsonl."""
import json, os, sys

os.makedirs("logs", exist_ok=True)

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

err = d.get("error") or {}
out = {
    "timestamp": d.get("timestamp"),
    "errorName": err.get("name"),
    "errorMessage": (err.get("message") or "")[:200],
}

with open("logs/errors.jsonl", "a") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
