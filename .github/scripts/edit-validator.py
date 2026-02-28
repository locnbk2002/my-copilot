#!/usr/bin/env python3
"""Track edit/create results and detect failure patterns."""
import json, os, sys

os.makedirs("logs", exist_ok=True)

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_name = d.get("toolName", "")
if tool_name not in ("edit", "create"):
    sys.exit(0)

tool_args = d.get("toolArgs", {})
if isinstance(tool_args, str):
    try:
        tool_args = json.loads(tool_args)
    except Exception:
        tool_args = {}

result = d.get("toolResult") or {}
file_path = ""
if isinstance(tool_args, dict):
    file_path = tool_args.get("path", "") or tool_args.get("file_path", "")

line_count = 0
if tool_name == "create" and isinstance(tool_args, dict):
    content = tool_args.get("file_text", "")
    if content:
        line_count = content.count("\n") + 1

out = {
    "timestamp": d.get("timestamp"),
    "toolName": tool_name,
    "filePath": file_path,
    "resultType": result.get("resultType"),
}

if line_count > 0:
    out["lineCount"] = line_count
    out["oversized"] = line_count > 200

with open("logs/edit-health.jsonl", "a") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
