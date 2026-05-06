#!/usr/bin/env bash
# UserPromptSubmit hook — snapshots the task text and git HEAD so the
# Stop hook can diff against it. The hook receives the prompt text on stdin
# (Claude Code piping the user's message) plus a JSON envelope; we only need
# whichever the harness sends.
set -euo pipefail

# Recursion guard: when eval-run.sh shells out to `claude -p` for scoring,
# that nested session would otherwise re-fire these hooks and loop.
[[ "${ZL_EVAL_RUNNING:-0}" == "1" ]] && exit 0

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STATE_DIR="$REPO_ROOT/.claude/eval-state"
mkdir -p "$STATE_DIR"

# Read the JSON event from stdin. Claude Code sends a JSON object with the
# fields documented at https://docs.claude.com/en/docs/claude-code/hooks
EVENT_JSON="$(cat || true)"

# Pull the prompt text out. Different harness versions use different keys;
# try the documented ones, fall back to the raw stdin if it isn't JSON.
PROMPT=""
if command -v jq >/dev/null 2>&1 && [[ -n "$EVENT_JSON" ]]; then
    PROMPT="$(printf '%s' "$EVENT_JSON" | jq -r '.prompt // .user_message // .text // empty' 2>/dev/null || true)"
fi
if [[ -z "$PROMPT" ]]; then
    PROMPT="$EVENT_JSON"
fi

# Skip slash commands and tool messages — only score real human prompts.
case "$PROMPT" in
    /*|"")
        exit 0
        ;;
esac

GIT_HEAD="$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
BRANCH="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if command -v jq >/dev/null 2>&1; then
    jq -n \
        --arg prompt "$PROMPT" \
        --arg head   "$GIT_HEAD" \
        --arg branch "$BRANCH" \
        --arg ts     "$TS" \
        '{prompt: $prompt, git_head: $head, branch: $branch, captured_at: $ts}' \
        > "$STATE_DIR/last-task.json"
else
    # Fallback: write a minimal JSON without jq.
    {
        printf '{"prompt": '
        printf '%s' "$PROMPT" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))'
        printf ', "git_head": "%s", "branch": "%s", "captured_at": "%s"}\n' "$GIT_HEAD" "$BRANCH" "$TS"
    } > "$STATE_DIR/last-task.json"
fi

exit 0
