# agent-eval

Self-grading harness for Claude Code. After every agent turn it diffs the
repo against the snapshot it took when the prompt arrived, asks a fresh
`claude -p` to score what actually shipped against the original ask, and
appends one styled card to `eval/eval.html` with red/green dots per
criterion and a 0–100 overall score.

You also get a `/eval` slash command for on-demand re-runs.

## Install

```bash
git clone <this-repo> agent-eval
cd agent-eval
bash install.sh             # installs into ./.claude/ of the current git repo
# or
bash install.sh --user      # installs user-wide into ~/.claude/
```

After install, **restart Claude Code** so the slash command and hooks load.

To remove:

```bash
bash install.sh --uninstall
```

The uninstaller deletes the three files and unmerges the hook entries from
`settings.json`, leaving any other hooks intact.

## What it installs

| Path                                  | Role                                                                 |
| ------------------------------------- | -------------------------------------------------------------------- |
| `<scope>/commands/eval.md`            | The `/eval` slash command for manual runs.                           |
| `<scope>/hooks/eval-capture-prompt.sh`| `UserPromptSubmit` hook — snapshots the prompt + git HEAD.           |
| `<scope>/hooks/eval-run.sh`           | `Stop` hook — diffs, scores, appends to `eval/eval.html`.            |
| `<scope>/settings.json`               | Hook registrations are merged in (existing entries preserved).       |

`<scope>` is the project root's `.claude/` for the default install, or
`~/.claude/` for `--user`.

The eval log lives in `eval/eval.html` at whichever **project root** the
agent is currently working in. User-wide install means every project picks
up the same hooks but writes its own per-project `eval/eval.html`.

## Output

`eval/eval.html` is a single self-contained file (no external CSS, no JS).
Each run appends one card:

```
┌────────────────────────────────────────────────────────────────────┐
│ 2026-05-06T07:18:00Z · branch parser-multi-format · base 876be279  │
│                                              90 [GREEN]            │
│ ┌──────────────────────────────────────────────────────────────┐   │
│ │ Hide handleiding link in the sidebar                         │   │
│ └──────────────────────────────────────────────────────────────┘   │
│  ●  Sidebar entry removed     diff drops the <a href="/help"> ...  │
│  ●  /help route still alive   no router change in cmd/server/...   │
│  ●  Version bumped            v0.10.1 → v0.10.2-multiformat ...    │
│  > raw                                                              │
└────────────────────────────────────────────────────────────────────┘
```

Verdicts:

- **GREEN** — every requirement landed; score ≥ 85.
- **AMBER** — most landed; 60–84.
- **RED** — significant gaps; < 60.

## Requirements

- `claude` CLI on PATH (the headless `claude -p` is the evaluator).
- `jq`.
- `git` (the project must be inside a git repo for the diff).

If `claude` or `jq` are missing the hooks log to stderr and exit 0 — they
never block your turn.

## Cost and performance

One `claude -p` call per agent stop, capped at 8 KB of diff so it stays
fast even after a huge refactor. Truncation is announced in the prompt
the evaluator sees. If the agent didn't change any files, the harness
short-circuits and writes a stub card without burning a Claude call.

## Recursion guard

The hooks set `ZL_EVAL_RUNNING=1` before invoking `claude -p` and bail
early if they see it. Without this, the evaluator's own session would
re-trigger the hooks and loop.

## Project rules — `eval/eval.md`

If you drop a markdown file at `eval/eval.md` in the project root, the
evaluator gets it as **additional criteria on top of** the original task.
It does not replace task scoring — both are weighed.

Two kinds of content, both optional:

```markdown
# Whatever you want — this is the rules document for the agent

- Functions stay under 50 lines.
- No `any` types in TypeScript files under `src/`.
- API errors must be 4-letter codes.
- New endpoints need a docstring describing auth requirements.

## Checks

- `npm run lint`
- `npm run typecheck`
- `pytest -x --tb=short`
```

**Free-form rules.** Anything you write outside the `## Checks` section is
passed verbatim to the evaluator as project-specific rules. Use it for
naming conventions, architectural guardrails, style preferences, "do not
introduce dependency X", anything an LLM can judge from the diff.

**Deterministic checks.** The `## Checks` section is a markdown list where
each item is a backtick-quoted shell command. Each command is executed in
the project root; its exit code and trimmed stdout/stderr go to the
evaluator. A non-zero exit is strong evidence that the rule it tests
failed. This is how you wire in linters, typecheckers, test suites, custom
shell scripts, anything with a meaningful exit code.

**Limits.** The rules text is capped at 4 KB, each check's output at 1 KB,
max 8 checks per run. Truncations are announced inline.

**Read-only by design.** The harness will not install or configure a
missing linter. If `npm run lint` isn't wired up yet, the check fails with
a useful exit code/output and the evaluator marks that criterion red. Set
up the tool in a separate turn.

## What counts as a "task"

A task starts at the **first** `UserPromptSubmit` after a `Stop`. Every
subsequent prompt while the agent is still working — plan-mode
confirmations, `AskUserQuestion` answers, mid-task corrections — is
appended as a follow-up to the same task. The evaluator receives the
original instruction PLUS every follow-up so nothing the user said is
lost in scoring. The state file is cleared on `Stop` so the next prompt
starts a fresh task.

## Troubleshooting

**`/eval` says nothing got appended / "no captured prompt at …"**

The capture hook never ran in this session. Two causes:

1. **You didn't restart Claude Code after `/plugin install`.** Hooks load
   only at session start. Quit and reopen.
2. **`/eval` was the first thing you ran.** The capture hook deliberately
   skips slash commands — there's no "task" to grade. Send a real prompt
   first; once the agent has done a turn, `/eval` will have something to
   score.

To verify hooks are wired (plugin install): the hooks are registered by
Claude Code itself from the plugin's `hooks/hooks.json` — you will **not**
see them in your project's `.claude/settings.json`. That's normal. To verify
the plugin is loaded, run `/plugin` and look for `agent-eval` in the list.

To verify hooks are wired (manual install via `bash install.sh`): grep
`.claude/settings.json` for `eval-capture-prompt.sh` — you should see one
entry under `hooks.UserPromptSubmit` and one under `hooks.Stop`.

## Toggling the auto-eval off

Don't want every prompt graded? Drop the two `agent-eval` entries from
`<scope>/settings.json` (or run `install.sh --uninstall` and reinstall
later). The `/eval` slash command keeps working either way for on-demand
runs.

## Plugin manifest

`.claude-plugin/plugin.json` lets this directory be loaded as a Claude
Code plugin if your team's setup supports `claude /plugin add <path>`.
For older versions or custom workflows, the `install.sh` route works
unchanged.

## What it does NOT do

- Doesn't modify your code.
- Doesn't read your secrets — only diffs and commit messages.
- Doesn't send anything to a third party. The `claude` CLI talks to
  Anthropic; everything else stays on disk.
- Doesn't fail your build or block your turn.
