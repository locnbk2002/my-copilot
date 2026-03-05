#!/usr/bin/env python3
"""Log compaction reminder every 100 tool calls."""
import datetime, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_utils

try:
    json.load(sys.stdin)
except Exception:
    sys.exit(0)

count = hook_utils.count_log_lines("tools.jsonl")
if count == 0 or count % 100 != 0:
    sys.exit(0)

threshold = count

for entry in hook_utils.read_log_tail("compact-reminders.jsonl", n=1000):
    if entry.get("threshold") == threshold:
        sys.exit(0)

out = {
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "toolCount": count,
    "threshold": threshold,
    "message": f"Session has {count} tool calls. Consider compacting context.",
}

hook_utils.append_log("compact-reminders.jsonl", out)
