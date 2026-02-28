#!/usr/bin/env python3
"""Block git commit/push when plans have pending phases."""
import glob as g, json, os, re, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

if data.get("toolName", "") != "bash":
    sys.exit(0)

tool_args = data.get("toolArgs", {})
if isinstance(tool_args, str):
    try:
        tool_args = json.loads(tool_args)
    except Exception:
        tool_args = {"command": tool_args}

if not isinstance(tool_args, dict):
    sys.exit(0)

command = tool_args.get("command", "")
if not re.search(r"\bgit\s+(commit|push)\b", command):
    sys.exit(0)

pending_plans = []
for plan_file in g.glob("plans/*/plan.md"):
    try:
        with open(plan_file, "r") as f:
            content = f.read()
    except Exception:
        continue

    if re.search(r"^status:\s*(completed|cancelled)", content, re.MULTILINE):
        continue

    pending = len(re.findall(r"\|\s*Pending\s*\|", content))
    if pending > 0:
        plan_name = os.path.basename(os.path.dirname(plan_file))
        pending_plans.append(f"{plan_name} ({pending} pending)")

if pending_plans:
    print(json.dumps({
        "permissionDecision": "deny",
        "permissionDecisionReason":
            f"Plans with pending phases: {', '.join(pending_plans)}",
    }))
    sys.exit(0)
