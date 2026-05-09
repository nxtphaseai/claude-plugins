# ask-visual

Visual `AskUserQuestion`. The agent writes a real HTML form (cards,
sliders, color pickers, drag-to-reorder, anything) instead of an ASCII
menu. The plugin spins up a tiny one-shot localhost web server, opens it
in the user's default browser, the user picks/types/drags/clicks, the
form is POSTed back, the script prints the result as JSON to stdout, and
the server exits. No daemon, no cleanup.

Stdlib Python only. Roughly 100 lines.

## Install

```bash
git clone <this-repo>
bash plugins/ask-visual/install.sh           # into ./.claude/ of the current git repo
# or
bash plugins/ask-visual/install.sh --user    # user-wide into ~/.claude/
```

After install, **restart Claude Code** so the `/ask-visual` slash command loads.

To remove:

```bash
bash plugins/ask-visual/install.sh --uninstall
```

## What it installs

| Path                              | Role                                                              |
| --------------------------------- | ----------------------------------------------------------------- |
| `<scope>/commands/ask-visual.md`  | The `/ask-visual` slash command (instructions for the agent).     |
| `<scope>/bin/ask-visual.py`       | The HTTP server / form runner. Python stdlib only.                |

`<scope>` is the project root's `.claude/` for the default install, or
`~/.claude/` for `--user`.

## How the agent uses it

The agent writes the *body* of a form to a temp file (no `<html>` /
`<form>` / submit JS — those are wrapped on for it). Then it runs:

```bash
python3 .claude/bin/ask-visual.py /tmp/ask.html
```

The script:

1. Binds a random free port on `127.0.0.1`.
2. Opens that URL in the user's default browser.
3. Blocks until a `POST /submit` arrives.
4. Prints the form data as a single JSON object to stdout.
5. Exits.

Inside the form:

- Every `name`-bearing element (`input`, `select`, `textarea`) is captured.
- The clicked button's `name`/`value` is included in the submission, so a
  card layout with one `<button name="choice" value="card-a">` per card
  works out of the box — clicking the button picks the card *and* submits.
- Multi-select dropdowns return arrays.

## Example

The agent wants to ask: *"pick a card design and an accent color"*. It
writes this to `/tmp/ask.html`:

```html
<h1>Pick a card design and accent color</h1>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">
  <div style="border:1px solid #ccc;border-radius:8px;padding:14px">
    <h3>Minimal</h3>
    <button name="card" value="minimal">Pick this</button>
  </div>
  <div style="border:1px solid #ccc;border-radius:8px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.08)">
    <h3>Lifted</h3>
    <button name="card" value="lifted">Pick this</button>
  </div>
  <div style="border:2px solid #1a1a1a;border-radius:8px;padding:14px">
    <h3>Bold</h3>
    <button name="card" value="bold">Pick this</button>
  </div>
</div>
<p><label>Accent color: <input type="color" name="accent" value="#1a1a1a"></label></p>
```

User clicks the "Lifted" card's button after picking a blue accent.
stdout receives:

```json
{"accent":"#2c5aa0","card":"lifted"}
```

Agent reads that, continues the task with the user's choice in hand.

## Limits and behavior

- **Localhost only.** Binds `127.0.0.1`, no exposure to the network.
- **One submission, then exit.** The form gets disabled after submit so
  refresh / double-click can't double-fire.
- **Default 10-minute timeout** waiting for submission. Override via
  `ASK_VISUAL_TIMEOUT=<seconds>` env var. On timeout the script exits 3.
- **No persistent backend.** No PIDs to track, no temp dirs to clean up,
  nothing left running between turns.

## When NOT to use it

- Headless / SSH-only environments — `webbrowser.open` no-ops silently
  there. Fall back to `AskUserQuestion`.
- Yes/no or one-of-two text questions — `AskUserQuestion` is faster.
- Anything where the user types a paragraph — text Q&A handles that fine.

## What it does NOT do

- Doesn't modify your code.
- Doesn't store anything between runs — the server is one-shot.
- Doesn't talk to any third party. Localhost only.
- Doesn't authenticate; assumes single-user local environment.
