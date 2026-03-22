#!/bin/bash

export PATH="$HOME/.local/bin:$PATH"

STATUS_JSON=$(cat)

# --- JSON fields ---
WORKSPACE_DIR=$(printf '%s' "$STATUS_JSON" | jq -r '.workspace.current_dir // .cwd // empty' 2>/dev/null)
CONTEXT_PERCENT=$(printf '%s' "$STATUS_JSON" | jq -r '.context_window.used_percentage // 0' 2>/dev/null)
INPUT_TOKENS=$(printf '%s' "$STATUS_JSON" | jq -r '.inputTokens // .input_tokens // 0' 2>/dev/null)
CTX_SIZE=$(printf '%s' "$STATUS_JSON" | jq -r '.contextWindowSize // .context_window_size // 0' 2>/dev/null)
PREMIUM_REQS=$(printf '%s' "$STATUS_JSON" | jq -r '.cost.total_premium_requests // 0' 2>/dev/null)
LINES_ADDED=$(printf '%s' "$STATUS_JSON" | jq -r '.cost.total_lines_added // 0' 2>/dev/null)
LINES_REMOVED=$(printf '%s' "$STATUS_JSON" | jq -r '.cost.total_lines_removed // 0' 2>/dev/null)
MODEL_RAW=$(printf '%s' "$STATUS_JSON" | jq -r '.model.id // empty' 2>/dev/null)

MODEL="$MODEL_RAW"

# --- Git info ---
GIT_DIR="${WORKSPACE_DIR:-.}"
GIT_BRANCH=$(git -C "$GIT_DIR" branch --show-current 2>/dev/null)
GIT_DIRTY=$(git -C "$GIT_DIR" status --short 2>/dev/null | wc -l | tr -d ' ')
GIT_DIRTY=${GIT_DIRTY:-0}
# Commits ahead of remote (to push) and behind (to pull)
GIT_AHEAD=$(git -C "$GIT_DIR" rev-list --count "@{u}..HEAD" 2>/dev/null || echo 0)
GIT_BEHIND=$(git -C "$GIT_DIR" rev-list --count "HEAD..@{u}" 2>/dev/null || echo 0)

# --- Session logs (mirrors hook_utils.py path logic) ---
LOG_BASE="$HOME/.local/share/.copilot/my-copilot/logs"
CWD="${WORKSPACE_DIR:-$(pwd)}"
PROJ_HASH=$(printf '%s' "$CWD" | sha256sum | cut -c1-12)
SESSION_ID=$(cat "$LOG_BASE/$PROJ_HASH/.sessions/$PPID" 2>/dev/null)
LOG_DIR="$LOG_BASE/$PROJ_HASH/$SESSION_ID"

# Tool call count from session log
TOOL_CALLS=0
if [ -n "$SESSION_ID" ] && [ -f "$LOG_DIR/tools.jsonl" ]; then
  TOOL_CALLS=$(wc -l < "$LOG_DIR/tools.jsonl" | tr -d ' ')
fi

# Session elapsed time from first sessionStart event
ELAPSED=""
if [ -n "$SESSION_ID" ] && [ -f "$LOG_DIR/sessions.jsonl" ]; then
  START_TS=$(grep '"sessionStart"' "$LOG_DIR/sessions.jsonl" 2>/dev/null | head -1 \
    | jq -r '.timestamp // empty' 2>/dev/null)
  if [ -n "$START_TS" ]; then
    START_SEC=$(date -d "$START_TS" +%s 2>/dev/null)
    NOW_SEC=$(date +%s)
    if [ -n "$START_SEC" ] && [ "$NOW_SEC" -gt "$START_SEC" ] 2>/dev/null; then
      ELAPSED_SEC=$(( NOW_SEC - START_SEC ))
      if [ "$ELAPSED_SEC" -ge 3600 ]; then
        ELAPSED="$(( ELAPSED_SEC / 3600 ))h$(( (ELAPSED_SEC % 3600) / 60 ))m"
      else
        ELAPSED="$(( ELAPSED_SEC / 60 ))m"
      fi
    fi
  fi
fi

# --- Context bar (10 segments) ---
build_bar() {
  local percent=${1:-0}
  local total=10
  local filled=$(( (percent * total + 99) / 100 ))  # ceiling division
  [ $filled -gt $total ] && filled=$total

  local bar=""
  for ((i=0; i<filled; i++)); do bar+="█"; done
  for ((i=filled; i<total; i++)); do bar+="░"; done

  if [ "$percent" -ge 80 ]; then
    echo "🔴 ${bar} ${percent}%"
  elif [ "$percent" -ge 50 ]; then
    echo "🟡 ${bar} ${percent}%"
  else
    echo "🟢 ${bar} ${percent}%"
  fi
}

# Optional token count annotation (e.g. "42K/200K")
TOKEN_STR=""
if [ "${INPUT_TOKENS:-0}" -gt 0 ] && [ "${CTX_SIZE:-0}" -gt 0 ] 2>/dev/null; then
  TOKEN_STR=" ($(( INPUT_TOKENS / 1000 ))K/$(( CTX_SIZE / 1000 ))K)"
fi

CONTEXT_BAR=$(build_bar "$CONTEXT_PERCENT")

# --- Assemble parts ---
PARTS=()

# Git branch + dirty marker
if [ -n "$GIT_BRANCH" ]; then
  GIT_INFO="🌿 $GIT_BRANCH"
  (( GIT_DIRTY > 0 )) && GIT_INFO="${GIT_INFO}*"
  PARTS+=("$GIT_INFO")
fi

# Git ahead/behind remote (only shown when non-zero)
if (( GIT_AHEAD > 0 || GIT_BEHIND > 0 )); then
  PARTS+=("⬆${GIT_AHEAD} ⬇${GIT_BEHIND}")
fi

[ -n "$MODEL" ] && PARTS+=("🤖 $MODEL")
PARTS+=("🪟 ${CONTEXT_BAR}${TOKEN_STR}")
PARTS+=("⚡ ${PREMIUM_REQS} req")
(( TOOL_CALLS > 0 )) && PARTS+=("🔧 ${TOOL_CALLS}")
[ -n "$ELAPSED" ] && PARTS+=("⏱ ${ELAPSED}")
if [ "$LINES_ADDED" != "0" ] || [ "$LINES_REMOVED" != "0" ]; then
  PARTS+=("📝 +${LINES_ADDED}/-${LINES_REMOVED}")
fi

# Join with ' | '
status=""
for part in "${PARTS[@]}"; do
  [ -n "$status" ] && status="$status | "
  status="$status$part"
done
echo "$status"
