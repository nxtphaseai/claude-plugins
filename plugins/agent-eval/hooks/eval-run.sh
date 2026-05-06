#!/usr/bin/env bash
# Stop hook — runs once after the agent finishes its turn. Reads the snapshot
# from .claude/eval-state/last-task.json (created by eval-capture-prompt.sh),
# diffs the repo against the captured HEAD, sends the lot to claude -p for
# scoring, and appends one card to eval/eval.html.
set -euo pipefail

# Recursion guard: don't score the nested claude -p calls we make ourselves.
[[ "${ZL_EVAL_RUNNING:-0}" == "1" ]] && exit 0

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STATE_FILE="$REPO_ROOT/.claude/eval-state/last-task.json"
EVAL_DIR="$REPO_ROOT/eval"
HTML="$EVAL_DIR/eval.html"
TPL="$REPO_ROOT/.claude/hooks/eval-card.html.tpl"

# Bail (with a useful message) if there's nothing to score. Silent exit here
# was the #1 reported failure mode — the user has no way to tell whether the
# hooks are even installed.
if [[ ! -f "$STATE_FILE" ]]; then
    cat >&2 <<EOF
[eval] no captured prompt at $STATE_FILE
       Either:
         - no UserPromptSubmit has fired since the last Stop this session
           (e.g. /eval was the first thing you ran — capture hooks skip
           slash commands by design), or
         - the capture hook isn't loaded. With /plugin install, hooks
           auto-register but only after you restart Claude Code. With
           bash install.sh, check .claude/settings.json for an entry
           pointing at eval-capture-prompt.sh.
       Send a real prompt and try again.
EOF
    exit 0
fi
command -v claude >/dev/null 2>&1 || { echo "[eval] claude CLI not found, skipping" >&2; exit 0; }
command -v jq     >/dev/null 2>&1 || { echo "[eval] jq not found, skipping" >&2; exit 0; }

mkdir -p "$EVAL_DIR"

PROMPT="$(jq -r '.prompt'      "$STATE_FILE")"
HEAD0="$(jq -r '.git_head'     "$STATE_FILE")"
BRANCH="$(jq -r '.branch'      "$STATE_FILE")"
CAPTURED_AT="$(jq -r '.captured_at' "$STATE_FILE")"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Follow-ups: every UserPromptSubmit since the original anchor (plan-mode
# confirmations, AskUserQuestion answers, mid-task corrections). Joined into
# a numbered list so the evaluator sees the whole conversation.
FOLLOW_UPS_BLOCK="$(jq -r '
  if (.follow_ups // [] | length) == 0 then ""
  else
    "=== FOLLOW-UPS / CLARIFICATIONS ===\n" +
    ((.follow_ups | to_entries | map("[" + ((.key + 1) | tostring) + "] " + .value.prompt) | join("\n\n")))
  end
' "$STATE_FILE")"

# Build the diff bundle. Cap to 8 KB so the evaluator runs fast even after a
# huge refactor; the evaluator is told the diff is truncated when relevant.
DIFF="$(git -C "$REPO_ROOT" diff "$HEAD0"...HEAD 2>/dev/null || true)"
DIFF_LEN=${#DIFF}
TRUNCATED="false"
if (( DIFF_LEN > 8192 )); then
    DIFF="${DIFF:0:8192}"
    TRUNCATED="true"
fi
LOG="$(git -C "$REPO_ROOT" log "$HEAD0"..HEAD --oneline 2>/dev/null || true)"

# If literally nothing changed, don't burn a Claude call — write a stub card
# saying the agent was a no-op for this prompt.
if [[ -z "$DIFF" && -z "$LOG" ]]; then
    JSON='{"task_summary":"(no code change)","overall_score":0,"verdict":"AMBER","criteria":[{"name":"Anything shipped?","status":"AMBER","evidence":"git diff and git log are both empty.","notes":"Agent may have answered without writing code."}],"missing":[],"extras":[]}'
else
    EVAL_PROMPT=$(cat <<EOF
You are an impartial code reviewer. Evaluate whether the agent delivered the task below.

Output a SINGLE JSON object — no prose, no markdown fences. Schema:
{
  "task_summary": "one-line restatement of the task",
  "overall_score": 0-100,
  "verdict": "GREEN" | "AMBER" | "RED",
  "criteria": [
    {"name": "...", "status": "GREEN|AMBER|RED", "evidence": "...", "notes": "..."}
  ],
  "missing": ["asks that didn't land"],
  "extras":  ["things shipped beyond the ask"]
}

Score guide: GREEN >= 85, AMBER 60-84, RED < 60. List 3-7 concrete criteria
specific to the task (not generic). Evidence must reference the diff/log.

=== ORIGINAL TASK ===
$PROMPT

$FOLLOW_UPS_BLOCK

=== BRANCH / HEAD ===
branch=$BRANCH  start_head=$HEAD0  truncated_diff=$TRUNCATED

=== git log ===
$LOG

=== git diff ===
$DIFF
EOF
)
    JSON="$(printf '%s' "$EVAL_PROMPT" | ZL_EVAL_RUNNING=1 claude -p --output-format text 2>/dev/null || true)"
    # Strip any accidental ```json fences.
    JSON="$(printf '%s' "$JSON" | sed -e 's/^```json//' -e 's/^```$//' | tr -d '\r')"
    # Validate; on failure, write a RED stub.
    if ! printf '%s' "$JSON" | jq -e . >/dev/null 2>&1; then
        JSON='{"task_summary":"(eval failed)","overall_score":0,"verdict":"RED","criteria":[{"name":"Evaluator output","status":"RED","evidence":"claude -p did not return valid JSON.","notes":"See .claude/eval-state/last-task.json"}],"missing":[],"extras":[]}'
    fi
fi

# Header on first run.
if [[ ! -s "$HTML" ]]; then
    cat > "$HTML" <<'HTMLHEAD'
<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>Agent eval log</title>
<style>
  body{font-family:-apple-system,Inter,system-ui,sans-serif;background:#f7f6f2;color:#111;margin:0;padding:32px;max-width:980px;margin-inline:auto}
  h1{font-size:20px;letter-spacing:-.01em;margin:0 0 24px}
  .card{background:#fff;border:1px solid rgba(17,17,16,.08);border-radius:10px;padding:18px 20px;margin-bottom:16px;box-shadow:0 1px 2px rgba(17,17,16,.04)}
  .card header{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:12px}
  .meta{font-size:12px;color:#6a6862;line-height:1.5}
  .score{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex-shrink:0}
  .score .num{font-size:28px;font-weight:600;line-height:1;font-variant-numeric:tabular-nums}
  .verdict{font-size:11px;font-weight:600;letter-spacing:.06em;padding:3px 8px;border-radius:999px}
  .v-GREEN{background:#eaf3de;color:#2f6b18}
  .v-AMBER{background:#faeeda;color:#7a4a0a}
  .v-RED{background:#f9e6e6;color:#8f2424}
  .task{font-size:14px;line-height:1.5;color:#1a1a1a;background:#fbfaf7;border-left:3px solid #2c3e6b;padding:10px 14px;border-radius:4px;white-space:pre-wrap;font-family:-apple-system,Inter,system-ui,sans-serif;margin:10px 0 12px}
  .crit{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-top:1px solid rgba(17,17,16,.06);font-size:13px}
  .crit:first-of-type{border-top:0}
  .dot{width:9px;height:9px;border-radius:50%;margin-top:6px;flex-shrink:0}
  .d-GREEN{background:#2f6b18}.d-AMBER{background:#c98a1a}.d-RED{background:#8f2424}
  .crit .body{flex:1}
  .crit .name{font-weight:600;color:#111}
  .crit .ev{color:#6a6862;font-size:12px;margin-top:2px}
  details{margin-top:10px;font-size:12px;color:#6a6862}
  details pre{background:#fbfaf7;padding:10px;border-radius:6px;overflow-x:auto;font-size:11px;line-height:1.5}
  ul.tags{list-style:none;padding:0;margin:8px 0 0;display:flex;flex-wrap:wrap;gap:6px}
  ul.tags li{background:#f1f0ec;padding:2px 8px;border-radius:999px;font-size:11px;color:#3a3935}
  .missing li{background:#f9e6e6;color:#8f2424}
  .extras  li{background:#eef1f7;color:#1a2649}
  hr.sep{border:0;border-top:1px solid rgba(17,17,16,.1);margin:24px 0}
</style>
<h1>Agent eval log</h1>
HTMLHEAD
fi

# Build a single card with jq + printf and append. We use jq for everything
# string-y so we don't have to think about HTML-escaping ourselves: the
# `@html` filter in jq does it for us.
CARD="$(printf '%s' "$JSON" | jq -r --arg now "$NOW" --arg captured "$CAPTURED_AT" --arg branch "$BRANCH" --arg head0 "$HEAD0" --arg task "$PROMPT" --arg raw "$JSON" '
  def dot(s): "d-" + s;
  def vcls(s): "v-" + s;
  "<article class=\"card\">"
  + "<header>"
  + "<div class=\"meta\">"
  + ($now | @html) + " · branch <code>" + ($branch | @html) + "</code>"
  + " · base " + ($head0[0:8] | @html)
  + "</div>"
  + "<div class=\"score\">"
  + "<span class=\"num\">" + (.overall_score|tostring) + "</span>"
  + "<span class=\"verdict " + vcls(.verdict) + "\">" + (.verdict|@html) + "</span>"
  + "</div>"
  + "</header>"
  + "<div class=\"task\">" + ($task | @html) + "</div>"
  + (.criteria // [] | map(
      "<div class=\"crit\"><div class=\"dot " + dot(.status) + "\"></div>"
      + "<div class=\"body\"><div class=\"name\">" + (.name | @html) + "</div>"
      + "<div class=\"ev\">" + (.evidence | @html) + "</div>"
      + (if (.notes // "") == "" then "" else "<div class=\"ev\">" + (.notes | @html) + "</div>" end)
      + "</div></div>"
    ) | join(""))
  + (if ((.missing // []) | length) > 0 then
       "<ul class=\"tags missing\">" + (.missing | map("<li>missing: " + (@html) + "</li>") | join("")) + "</ul>"
     else "" end)
  + (if ((.extras // []) | length) > 0 then
       "<ul class=\"tags extras\">"  + (.extras  | map("<li>+ " + (@html) + "</li>") | join("")) + "</ul>"
     else "" end)
  + "<details><summary>raw</summary><pre>" + ($raw | @html) + "</pre></details>"
  + "</article>"
')"

printf '%s\n' "$CARD" >> "$HTML"

echo "[eval] appended $(printf '%s' "$JSON" | jq -r '.verdict + " " + (.overall_score|tostring)') to $HTML" >&2

# End-of-task: clear the state file so the next UserPromptSubmit starts a
# fresh task instead of being treated as a follow-up to this one.
rm -f "$STATE_FILE"
exit 0
