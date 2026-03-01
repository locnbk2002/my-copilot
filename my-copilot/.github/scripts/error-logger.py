#!/usr/bin/env python3
"""Log error events to errors.jsonl."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_utils

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

hook_utils.append_log("errors.jsonl", out)
