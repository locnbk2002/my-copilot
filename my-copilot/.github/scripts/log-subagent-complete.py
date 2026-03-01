#!/usr/bin/env python3
"""Log subagent completion events to logs/subagents.jsonl."""
import json, os, sys
from datetime import datetime, timezone

os.makedirs("logs", exist_ok=True)

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_name = data.get("toolName", "")
if tool_name != "task":
    sys.exit(0)

tool_args_raw = data.get("toolArgs", "{}")
try:
    tool_args = json.loads(tool_args_raw) if isinstance(tool_args_raw, str) else tool_args_raw
except Exception:
    tool_args = {}

tool_result = data.get("toolResult") or {}
entry = json.dumps({
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "event": "complete",
    "agent_type": tool_args.get("agent_type", "unknown"),
    "result_type": tool_result.get("resultType", "unknown"),
    "result_preview": (tool_result.get("textResultForLlm") or "")[:300],
}, separators=(",", ":"))

with open("logs/subagents.jsonl", "a") as f:
    f.write(entry + "\n")
