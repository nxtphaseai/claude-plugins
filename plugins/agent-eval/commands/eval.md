---
description: Score the most recent agent turn against the user's task and append a card to eval/eval.html
---

Run the project's evaluation harness on the latest agent turn.

Steps:

1. Run `bash .claude/hooks/eval-run.sh`. The script reads the most recent
   captured prompt from `.claude/eval-state/last-task.json`, diffs the repo
   against the head it snapshotted, calls `claude -p` to score the result,
   and appends one card to `eval/eval.html`.
2. After the script exits, read the **last `<article class="card">…</article>`
   block** from `eval/eval.html` and report the verdict and overall score
   to the user as a single short line, e.g. *"GREEN 92 — appended to
   eval/eval.html"*. Do not paste the full HTML.
3. If the script printed a warning to stderr (missing `claude` or `jq`,
   evaluator JSON parse failure), surface that warning verbatim instead of a
   verdict so the user knows the eval didn't actually run.

Do not modify code as part of `/eval`. The skill is read-only against the
working tree; it only writes to `eval/eval.html`.
