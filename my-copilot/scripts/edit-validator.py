#!/usr/bin/env python3
"""Track edit/create results and detect failure patterns."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_utils

def count_loc(content: str) -> int:
    """Count lines of code, excluding blanks, comments, and prompt string bodies."""
    lines = content.split("\n")
    loc = 0
    in_multiline_str = False
    for line in lines:
        stripped = line.strip()
        if in_multiline_str:
            if '"""' in stripped or "'''" in stripped:
                in_multiline_str = False
                loc += 1
            continue
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("//"):
            continue
        if re.match(r'^[a-zA-Z_]\w*\s*=\s*("""|\'\'\')', stripped) and not stripped.endswith('"""') and not stripped.endswith("'''"):
            in_multiline_str = True
            loc += 1
            continue
        loc += 1
    return loc

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
loc_count = 0
if tool_name == "create" and isinstance(tool_args, dict):
    content = tool_args.get("file_text", "")
    if content:
        line_count = content.count("\n") + 1
        loc_count = count_loc(content)

out = {
    "timestamp": d.get("timestamp"),
    "toolName": tool_name,
    "filePath": file_path,
    "resultType": result.get("resultType"),
}

if line_count > 0:
    out["lineCount"] = line_count
    out["locCount"] = loc_count
    out["oversized"] = loc_count > 200

hook_utils.append_log("edit-health.jsonl", out)
