# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Claude Code plugin marketplace (`name: nxtphaseai`) plus the plugins it ships. Top-level `.claude-plugin/marketplace.json` is the registry; each plugin lives self-contained under `plugins/<name>/` with its own `.claude-plugin/plugin.json`. There is no build system — everything is bash + JSON, executed by Claude Code's hook runtime.

## Repo layout

```
.claude-plugin/marketplace.json   # marketplace registry (lists every plugin + versions)
plugins/<name>/
  .claude-plugin/plugin.json      # plugin manifest
  commands/*.md                   # slash commands
  hooks/hooks.json                # hook registrations (loaded by Claude when installed as a plugin)
  hooks/*.sh                      # hook scripts
  install.sh                      # manual installer for environments without /plugin
  README.md
```

## Two install paths must keep working

Every plugin ships **both** as a proper Claude Code plugin and as a manually-installable bundle:

1. **Plugin path** (`/plugin install <name>@nxtphaseai`): Claude reads `hooks/hooks.json` and resolves `${CLAUDE_PLUGIN_ROOT}` itself. Scripts are run from the plugin's install location.
2. **Manual path** (`bash install.sh`): the installer copies scripts into `<repo>/.claude/` (or `~/.claude/` with `--user`) and merges hook entries into `settings.json`. The shipped `hooks.json` template uses `${CLAUDE_PLUGIN_ROOT:-$CLAUDE_PROJECT_DIR/.claude}` so the same JSON works in both modes; `install.sh` substitutes the literal path before merging.

When changing hook command paths, update both `hooks/hooks.json` and the `sub("\\$\\{CLAUDE_PLUGIN_ROOT:-\\$CLAUDE_PROJECT_DIR/\\.claude\\}"; ...)` substitution in `install.sh`.

## Versioning rule

Three places hold versions and they need to move together when a plugin changes:

- `plugins/<name>/.claude-plugin/plugin.json` → `version`
- `.claude-plugin/marketplace.json` → the matching `plugins[].version`
- `.claude-plugin/marketplace.json` → `metadata.version` (so a marketplace re-subscribe sees *something* changed even if you only touched one plugin)

## Plugins overview

- `agent-eval` — see section below; auto-grades each agent turn.
- `ask-visual` — single-shot localhost HTTP server. Agent writes the body of an HTML form to a temp file and runs `python3 .claude/bin/ask-visual.py <file>`; script auto-opens the URL in the user's browser, blocks until POST, prints submission as JSON to stdout, exits. Stdlib-only Python. No persistent backend by design — every question spins up a fresh server, which dies on submit. Multi-button-per-card pattern works because the JS shim captures the clicked submitter's name+value alongside all named inputs.

## agent-eval architecture

Self-grading harness. Understand the pairing before editing:

- **`hooks/eval-capture-prompt.sh`** runs on `UserPromptSubmit`. Snapshots the user's prompt, current git HEAD, and branch into `<repo>/.claude/eval-state/last-task.json`.
- **`hooks/eval-run.sh`** runs on `Stop`. Diffs repo against the captured HEAD, sends prompt + diff (capped at 8 KB) to `claude -p` for scoring, appends a styled card to `<repo>/eval/eval.html`, then deletes the state file.

Four behaviors that aren't obvious from reading either script alone:

1. **Task = anchor + follow-ups.** A new task is the first `UserPromptSubmit` after a `Stop`. Subsequent prompts (plan-mode confirmations, `AskUserQuestion` answers, mid-task corrections) get appended to `follow_ups[]` in the same state file. The evaluator sees the original instruction *plus* every follow-up. Don't change capture to overwrite — that regresses 0.2.0.
2. **Recursion guard via `ZL_EVAL_RUNNING=1`.** Both hooks bail immediately if this env var is set. `eval-run.sh` exports it before invoking `claude -p`, otherwise the nested session re-fires the hooks and loops. Any new hook in this plugin must honor the same guard.
3. **Fail-soft is mandatory.** Missing `claude`, `jq`, or `git` must log to stderr and `exit 0` — never block the user's turn. The empty-diff path writes a stub card without burning a Claude call. State-missing in `eval-run.sh` is loud-on-stderr (0.2.1+), not silent.
4. **Optional project rubric at `eval/eval.md` (0.3.0+).** If present, its free-form prose is passed to the evaluator as additional criteria, and any markdown list items under `## Checks` of the form `- \`cmd\`` are executed in the project root and their exit code + trimmed output also goes to the evaluator. Augments task scoring, never replaces it. The grader is **read-only** — it never sets up a missing linter/typechecker; a missing tool fails its check loudly and the agent's next turn fixes it. This is deliberate: a grader that mutates the repo creates diffs that contaminate the next eval.

State file: `.claude/eval-state/last-task.json` (per-project, gitignored by virtue of being inside `.claude/`). Output: `eval/eval.html` (single self-contained file, no JS, appended-to per run).

## install.sh conventions (apply to any new plugin)

- Idempotent: re-running must not double-register hooks. The current `settings_merge` in agent-eval drops any existing entries whose `command` matches `eval-capture-prompt\.sh|eval-run\.sh` before appending. New plugins should dedupe on their own script names the same way.
- `--uninstall` removes installed files *and* unmerges hook entries via the inverse `jq` filter, leaving unrelated hooks intact.
- Validate `jq` is present (hard-fail) and warn (don't fail) if `claude` isn't on PATH.

## Adding a new plugin

1. Scaffold `plugins/<name>/` with `.claude-plugin/plugin.json`, `README.md`, and whatever combination of `commands/`, `hooks/`, `agents/` it needs.
2. Add an entry in `.claude-plugin/marketplace.json` and bump `metadata.version`.
3. If it uses hooks, mirror the `${CLAUDE_PLUGIN_ROOT:-$CLAUDE_PROJECT_DIR/.claude}` pattern and ship an `install.sh` that does dedupe-on-merge and supports `--uninstall`.
4. Add a row to the README's "Available plugins" table.

## Testing changes

There is no test suite. To exercise a change:

- For a plugin's install flow: `bash plugins/<name>/install.sh` inside a throwaway git repo, inspect the resulting `.claude/settings.json`, then `bash plugins/<name>/install.sh --uninstall` and confirm settings.json is clean.
- For agent-eval's runtime: from a repo where it's installed, send a prompt, let the agent finish, and check `eval/eval.html` for an appended card.

## Commit style

User's global rule: commit messages via `printf` to a tempfile + `git commit -F`, never via `-m "$(cat <<EOF ...)"` (the user's shell aliases `cat` to `pygmentize -g` which injects ANSI escapes). No "Co-Authored-By" trailers in this repo.
