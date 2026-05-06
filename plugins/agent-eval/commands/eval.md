---
description: Score the most recent agent turn against the user's task and append a card to eval/eval.html
---

Run the project's evaluation harness on the latest agent turn.

Steps:

1. Locate and run the eval script. It lives in one of two places depending on
   how the plugin was installed. Run this exact shell snippet:

   ```bash
   if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -f "${CLAUDE_PLUGIN_ROOT}/hooks/eval-run.sh" ]; then
     bash "${CLAUDE_PLUGIN_ROOT}/hooks/eval-run.sh"
   elif [ -f .claude/hooks/eval-run.sh ]; then
     bash .claude/hooks/eval-run.sh
   else
     echo "agent-eval: cannot find eval-run.sh — is the plugin installed and Claude Code restarted?" >&2
     exit 1
   fi
   ```

   The script reads the most recent captured prompt from
   `.claude/eval-state/last-task.json` (relative to the project root), diffs
   the repo against the head it snapshotted, calls `claude -p` to score the
   result, and appends one card to `eval/eval.html`.

2. After the script exits, read the **last `<article class="card">…</article>`
   block** from `eval/eval.html` and report the verdict and overall score
   to the user as a single short line, e.g. *"GREEN 92 — appended to
   eval/eval.html"*. Do not paste the full HTML.

3. If the script printed a warning to stderr, surface it verbatim instead of
   inventing a diagnosis. Common warnings and what they actually mean:
   - **`no captured prompt at …`** — the capture hook hasn't run yet this
     session. Either Claude Code wasn't restarted after install, or `/eval`
     was the first thing the user ran (slash commands are skipped by the
     capture hook). Tell the user to send a real prompt first.
   - **`claude CLI not found` / `jq not found`** — install the missing tool.

Do not modify code as part of `/eval`. The skill is read-only against the
working tree; it only writes to `eval/eval.html`.
