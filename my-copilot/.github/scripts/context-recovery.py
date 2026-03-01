#!/usr/bin/env python3
"""Log recovery data on context window exhaustion errors."""
import json, os, sys

os.makedirs("logs", exist_ok=True)

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

err = d.get("error") or {}
msg = (err.get("message") or "").lower()

CONTEXT_KEYWORDS = ["context", "token", "limit", "capacity", "truncat", "window", "exceed"]
if not any(kw in msg for kw in CONTEXT_KEYWORDS):
    sys.exit(0)

from collections import deque

recent_tools = []
try:
    with open("logs/tools.jsonl", "r") as f:
        for line in deque(f, maxlen=10):
            try:
                recent_tools.append(json.loads(line.strip()))
            except Exception:
                pass
except FileNotFoundError:
    pass

active_agent = None
try:
    with open("logs/subagents.jsonl", "r") as f:
        for line in deque(f, maxlen=1):
            try:
                active_agent = json.loads(line.strip())
            except Exception:
                pass
except FileNotFoundError:
    pass

out = {
    "timestamp": d.get("timestamp"),
    "errorName": err.get("name"),
    "errorMessage": (err.get("message") or "")[:200],
    "recentTools": recent_tools,
    "activeAgent": active_agent,
}

with open("logs/context-recovery.jsonl", "a") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
