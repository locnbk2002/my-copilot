#!/usr/bin/env python3
"""Detect stuck/looping sub-agents by tracking consecutive task calls."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_utils

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

recent = hook_utils.read_log_tail("subagents.jsonl", 5)
if not recent:
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

hook_utils.append_log("agent-health.jsonl", out)
