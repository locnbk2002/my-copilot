#!/usr/bin/env python3
"""Log subagent launch events to logs/subagents.jsonl."""
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

entry = json.dumps({
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "event": "launch",
    "agent_type": tool_args.get("agent_type", "unknown"),
    "model": tool_args.get("model", "default"),
    "prompt_preview": (tool_args.get("prompt") or "")[:200],
}, separators=(",", ":"))

with open("logs/subagents.jsonl", "a") as f:
    f.write(entry + "\n")
