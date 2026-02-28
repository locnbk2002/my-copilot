#!/usr/bin/env python3
"""Block edit/create containing AI-generated comment anti-patterns."""
import json, re, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_name = data.get("toolName", "")
if tool_name not in ("edit", "create"):
    sys.exit(0)

tool_args = data.get("toolArgs", {})
if isinstance(tool_args, str):
    try:
        tool_args = json.loads(tool_args)
    except Exception:
        sys.exit(0)

if not isinstance(tool_args, dict):
    sys.exit(0)

file_path = tool_args.get("path", "") or tool_args.get("file_path", "")
CODE_EXTS = (".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".cs")
if not any(file_path.endswith(ext) for ext in CODE_EXTS):
    sys.exit(0)

content = ""
if tool_name == "edit":
    content = tool_args.get("new_str", "")
elif tool_name == "create":
    content = tool_args.get("file_text", "")

if not content:
    sys.exit(0)

ANTI_PATTERNS = [
    r"^\s*(?://|#)\s*This (?:function|method|class|module|component|hook)\b",
    r"^\s*(?://|#)\s*Helper (?:function|method|class) (?:to|for|that)\b",
    r"^\s*(?://|#)\s*Utility (?:function|method) (?:to|for|that)\b",
    r"^\s*(?://|#)\s*(?:Import|Define|Declare|Initialize|Set up) (?:the|a|an|necessary)\b",
    r"^\s*(?://|#)\s*(?:The )?(?:below|above|following) (?:code|function|method)\b",
]

for line in content.splitlines():
    for pattern in ANTI_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            print(json.dumps({
                "permissionDecision": "deny",
                "permissionDecisionReason":
                    f"AI-generated comment detected: {line.strip()[:80]}",
            }))
            sys.exit(0)
