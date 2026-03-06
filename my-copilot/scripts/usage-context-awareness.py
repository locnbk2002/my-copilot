#!/usr/bin/env python3
"""
PostToolUse hook — injects <usage-awareness> into AI context.
Tracks session context window usage as proxy for context % consumed.
Throttled: runs at most every 5 minutes per session.
"""
import datetime, json, os, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_utils

THROTTLE_SEC = 300        # 5 minutes between injections
CONTEXT_MAX_CALLS = 400   # tool calls considered ~100% context


def _cache_path() -> Path:
    return Path(f"/tmp/ck-usage-awareness-{os.getppid()}.json")


def is_throttled() -> bool:
    """Return True if last run was within THROTTLE_SEC."""
    p = _cache_path()
    if not p.exists():
        return False
    try:
        data = json.loads(p.read_text())
        last = datetime.datetime.fromisoformat(data["last_run"])
        elapsed = (datetime.datetime.now(datetime.timezone.utc) - last).total_seconds()
        return elapsed < THROTTLE_SEC
    except Exception:
        return False


def update_throttle() -> None:
    """Write current timestamp to cache file."""
    _cache_path().write_text(
        json.dumps({"last_run": datetime.datetime.now(datetime.timezone.utc).isoformat()})
    )


def get_context_percent(payload: dict) -> tuple[int, str]:
    """
    Return (percent, detail_str).
    Checks payload for real token fields; falls back to tool-call proxy.
    """
    # Scenario A: real token data from hook payload
    input_tokens = payload.get("inputTokens") or payload.get("input_tokens")
    context_window = payload.get("contextWindowSize") or payload.get("context_window_size")
    if input_tokens and context_window:
        pct = min(100, int((input_tokens / context_window) * 100))
        used_k = input_tokens // 1000
        total_k = context_window // 1000
        return pct, f"{used_k}K / {total_k}K tokens"

    # Scenario B: tool-call proxy
    tool_calls = hook_utils.count_log_lines("tools.jsonl")
    pct = min(100, int((tool_calls / CONTEXT_MAX_CALLS) * 100))
    return pct, f"{tool_calls} tool calls"


def format_awareness(percent: int, detail: str) -> str:
    """Build <usage-awareness> XML string with threshold markers."""
    if percent >= 90:
        label = f"Context: {percent}% [CRITICAL] ({detail}) — start fresh session"
    elif percent >= 70:
        label = f"Context: {percent}% [WARNING] ({detail}) — consider /compact"
    else:
        label = f"Context: {percent}% ({detail})"
    return f"<usage-awareness>\n{label}\n</usage-awareness>"


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if is_throttled():
        sys.exit(0)

    percent, detail = get_context_percent(payload)
    print(format_awareness(percent, detail))
    update_throttle()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
