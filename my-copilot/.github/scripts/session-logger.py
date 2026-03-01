#!/usr/bin/env python3
"""Log session start/end events to sessions.jsonl."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_utils

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

if "source" in d:
    hook_utils.init_session()
    out = {"timestamp": d.get("timestamp"), "cwd": d.get("cwd"), "event": "sessionStart", "source": d.get("source"), "initialPrompt": d.get("initialPrompt")}
    hook_utils.append_log("sessions.jsonl", out)
else:
    out = {"timestamp": d.get("timestamp"), "cwd": d.get("cwd"), "event": "sessionEnd", "reason": d.get("reason")}
    hook_utils.append_log("sessions.jsonl", out)
    hook_utils.end_session()
