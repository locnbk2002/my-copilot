#!/usr/bin/env python3
"""Log compaction reminder every 100 tool calls."""
import datetime, json, os, sys

os.makedirs("logs", exist_ok=True)

try:
    json.load(sys.stdin)
except Exception:
    sys.exit(0)

try:
    with open("logs/tools.jsonl", "r") as f:
        count = sum(1 for _ in f)
except FileNotFoundError:
    sys.exit(0)

if count == 0 or count % 100 != 0:
    sys.exit(0)

threshold = count

try:
    with open("logs/compact-reminders.jsonl", "r") as f:
        for line in f:
            try:
                if json.loads(line.strip()).get("threshold") == threshold:
                    sys.exit(0)
            except Exception:
                pass
except FileNotFoundError:
    pass

out = {
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "toolCount": count,
    "threshold": threshold,
    "message": f"Session has {count} tool calls. Consider compacting context.",
}

with open("logs/compact-reminders.jsonl", "a") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
