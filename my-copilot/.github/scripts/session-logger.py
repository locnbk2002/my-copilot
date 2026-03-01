#!/usr/bin/env python3
"""Log session start/end events to logs/sessions.jsonl."""
import json, os, sys

os.makedirs("logs", exist_ok=True)

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

if "source" in d:
    out = {"timestamp": d.get("timestamp"), "cwd": d.get("cwd"), "event": "sessionStart", "source": d.get("source"), "initialPrompt": d.get("initialPrompt")}
else:
    out = {"timestamp": d.get("timestamp"), "cwd": d.get("cwd"), "event": "sessionEnd", "reason": d.get("reason")}

with open("logs/sessions.jsonl", "a") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
