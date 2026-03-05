#!/usr/bin/env python3
"""Log tool usage events to tools.jsonl."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_utils

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

out = {
    "timestamp": d.get("timestamp"),
    "toolName": d.get("toolName"),
    "resultType": (d.get("toolResult") or {}).get("resultType"),
}

hook_utils.append_log("tools.jsonl", out)
