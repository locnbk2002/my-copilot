#!/usr/bin/env python3
"""Detect stuck/looping sub-agents by tracking consecutive task calls."""
import json, os, sys

os.makedirs("logs", exist_ok=True)

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

if d.get("toolName", "") != "task":
    sys.exit(0)

tool_args = d.get("toolArgs", {})
if isinstance(tool_args, str):
    try:
        tool_args = json.loads(tool_args)
    except Exception:
        sys.exit(0)

if not isinstance(tool_args, dict):
    sys.exit(0)

agent_type = tool_args.get("agent_type", "")
prompt = (tool_args.get("prompt", "") or "")[:100]

from collections import deque

recent = []
try:
    with open("logs/subagents.jsonl", "r") as f:
        for line in deque(f, maxlen=5):
            try:
                recent.append(json.loads(line.strip()))
            except Exception:
                pass
except FileNotFoundError:
    sys.exit(0)

consecutive = 0
for entry in reversed(recent):
    if entry.get("agent_type") == agent_type:
        consecutive += 1
    else:
        break

if consecutive < 3:
    sys.exit(0)

similar = 0
for entry in reversed(recent):
    entry_prompt = (entry.get("prompt_preview") or "")[:100]
    if entry.get("agent_type") == agent_type and entry_prompt == prompt:
        similar += 1
    else:
        break

if similar < 3:
    sys.exit(0)

out = {
    "timestamp": d.get("timestamp"),
    "severity": "warning",
    "agentType": agent_type,
    "promptPreview": prompt,
    "loopCount": similar,
    "message": f"Possible agent loop: {similar}x consecutive {agent_type}",
}

with open("logs/agent-health.jsonl", "a") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
