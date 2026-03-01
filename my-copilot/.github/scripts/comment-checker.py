#!/usr/bin/env python3
"""Block edit/create containing code comments. Uses @code-yeongyu/comment-checker
binary (tree-sitter AST) when available, falls back to regex anti-patterns."""
import json, re, shutil, subprocess, sys

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
old_str = ""
if tool_name == "edit":
    content = tool_args.get("new_str", "")
    old_str = tool_args.get("old_str", "")
elif tool_name == "create":
    content = tool_args.get("file_text", "")

if not content:
    sys.exit(0)


def deny(reason):
    print(json.dumps({
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }))
    sys.exit(0)


def try_binary_check():
    """Run @code-yeongyu/comment-checker binary. Returns True if handled."""
    binary = shutil.which("comment-checker")
    if not binary:
        return False

    # Translate Copilot CLI protocol → Claude Code protocol
    translated = {"tool_input": {"file_path": file_path}}
    if tool_name == "create":
        translated["tool_name"] = "Write"
        translated["tool_input"]["content"] = content
    else:
        translated["tool_name"] = "Edit"
        translated["tool_input"]["old_string"] = old_str
        translated["tool_input"]["new_string"] = content

    try:
        proc = subprocess.run(
            [binary, "check"],
            input=json.dumps(translated),
            capture_output=True, text=True, timeout=4,
        )
    except (subprocess.TimeoutExpired, OSError):
        return False

    if proc.returncode == 2:
        msg = (proc.stderr.strip() or "Code comments detected")[:200]
        deny(msg)

    return True


def fallback_regex_check():
    """Regex fallback when binary is not installed."""
    patterns = [
        r"^\s*(?://|#)\s*This (?:function|method|class|module|component|hook)\b",
        r"^\s*(?://|#)\s*Helper (?:function|method|class) (?:to|for|that)\b",
        r"^\s*(?://|#)\s*Utility (?:function|method) (?:to|for|that)\b",
        r"^\s*(?://|#)\s*(?:Import|Define|Declare|Initialize|Set up) (?:the|a|an|necessary)\b",
        r"^\s*(?://|#)\s*(?:The )?(?:below|above|following) (?:code|function|method)\b",
    ]
    for line in content.splitlines():
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                deny(f"AI-generated comment detected: {line.strip()[:80]}")


if not try_binary_check():
    fallback_regex_check()
