#!/usr/bin/env python3
"""Log recovery data on context window exhaustion errors."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_utils

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

err = d.get("error") or {}
msg = (err.get("message") or "").lower()

CONTEXT_KEYWORDS = ["context", "token", "limit", "capacity", "truncat", "window", "exceed"]
if not any(kw in msg for kw in CONTEXT_KEYWORDS):
    sys.exit(0)

recent_tools = hook_utils.read_log_tail("tools.jsonl", 10)

_agent_list = hook_utils.read_log_tail("subagents.jsonl", 1)
active_agent = _agent_list[0] if _agent_list else None

out = {
    "timestamp": d.get("timestamp"),
    "errorName": err.get("name"),
    "errorMessage": (err.get("message") or "")[:200],
    "recentTools": recent_tools,
    "activeAgent": active_agent,
}

hook_utils.append_log("context-recovery.jsonl", out)
