#!/usr/bin/env python3
"""Log tool usage events to logs/tools.jsonl."""
import json, os, sys

os.makedirs("logs", exist_ok=True)

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

out = {
    "timestamp": d.get("timestamp"),
    "toolName": d.get("toolName"),
    "resultType": (d.get("toolResult") or {}).get("resultType"),
}

with open("logs/tools.jsonl", "a") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
