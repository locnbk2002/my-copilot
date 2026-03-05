#!/usr/bin/env python3
"""Block access to sensitive files. Outputs deny JSON to stdout if matched."""
import json, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_name = data.get("toolName", "")
if tool_name not in ("bash", "glob", "grep", "view", "edit", "create"):
    sys.exit(0)

tool_args = data.get("toolArgs", {})
if isinstance(tool_args, str):
    try:
        tool_args = json.loads(tool_args)
    except Exception:
        args_str = tool_args
else:
    args_str = None

if isinstance(tool_args, dict):
    args_str = " ".join(str(v) for v in tool_args.values())
elif args_str is None:
    args_str = str(tool_args)

SENSITIVE_PATTERNS = [
    ".env",
    ".env.",
    ".pem",
    ".key",
    ".cert",
    "id_rsa",
    "id_ed25519",
    "secret",
    "credential",
    "password",
    ".aws/credentials",
]

for pattern in SENSITIVE_PATTERNS:
    if pattern in args_str:
        print(json.dumps({
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Sensitive file detected: {pattern}",
        }))
        sys.exit(0)
