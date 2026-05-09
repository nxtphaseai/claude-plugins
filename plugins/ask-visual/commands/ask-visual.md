---
description: Ask the user a rich UI question (cards, sliders, color pickers, anything HTML) instead of AskUserQuestion or ASCII menus.
---

Use this when you would otherwise call `AskUserQuestion` but the choice is
visual, spatial, or needs interactive controls — picking from rendered
cards, choosing a color, dragging a slider, comparing layouts side by side,
or any combination. Plain-text Q&A is the wrong shape for those.

A one-shot localhost web server is started, the user picks/types/clicks in
their browser, the form is POSTed back, the script prints the result to
stdout as JSON, and the server exits. No persistent backend, nothing to
clean up.

## Make every choice informative AND creative

The whole point of going visual is that the user can actually compare
options instead of squinting at a one-line label. Treat each choice as a
small pitch:

- **Give it a memorable name or label** — never `Option A`, `Choice 1`,
  `Foo`. Pick a word or short phrase that is itself evocative or has a
  story behind it.
- **Add a short description** — 1-2 sentences explaining what that choice
  *means*, what tradeoff it represents, what it would feel like to live
  with. Show, don't enumerate.
- **Make the visual carry information** — if the choice is about layout,
  render the layout. If it is about color, show the color. If it is about
  copy, show the copy in context. The form is HTML; use it.
- **Avoid bland symmetry** — three nearly identical options with one word
  swapped is a worse experience than text Q&A. If you cannot make the
  options meaningfully different, fall back to `AskUserQuestion`.

When you generate the choices yourself, lean creative. The user can always
write a custom answer in a free-text field if none of yours land.

## Workflow

1. Write the **body** of the form to a temp file. Do not write `<html>`,
   `<head>`, `<form>`, the wrapper styles, or the submit JS — those are all
   injected. Just the controls. Every interactive element should have a
   `name` attribute so its value comes back keyed in the result.

   For multi-card "Pick this" patterns: each card just contains its own
   `<button name="choice" value="...">Pick this</button>`. The clicked
   button's name+value is added to the result automatically, so a single
   click both selects the card AND submits the form. Other inputs in the
   page (color, slider, etc.) get included in the same submission.

   Example body:

   ```html
   <h1>Pick a card design and an accent color</h1>
   <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">
     <div style="border:1px solid #ccc;border-radius:8px;padding:14px">
       <h3>Minimal</h3><p>Plain border, no shadow.</p>
       <button name="card" value="minimal">Pick this</button>
     </div>
     <div style="border:1px solid #ccc;border-radius:8px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.08)">
       <h3>Lifted</h3><p>Subtle drop shadow.</p>
       <button name="card" value="lifted">Pick this</button>
     </div>
     <div style="border:2px solid #1a1a1a;border-radius:8px;padding:14px">
       <h3>Bold</h3><p>Heavy outline.</p>
       <button name="card" value="bold">Pick this</button>
     </div>
   </div>
   <p><label>Accent color: <input type="color" name="accent" value="#1a1a1a"></label></p>
   ```

2. Locate and run the helper. The script lives in one of two places
   depending on install mode. Run this exact snippet:

   ```bash
   for cand in \
     "${CLAUDE_PLUGIN_ROOT:-}/bin/ask-visual.py" \
     "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/bin/ask-visual.py" \
     "$HOME/.claude/bin/ask-visual.py"; do
     if [ -f "$cand" ]; then
       python3 "$cand" /tmp/ask.html
       exit $?
     fi
   done
   echo "ask-visual: helper not found — is the plugin installed and Claude Code restarted?" >&2
   exit 1
   ```

3. The helper prints **a single JSON object** to stdout (the form data) and
   exits. Parse it. That is the user's answer. Continue the task.

   For the example above, a typical result looks like:

   ```json
   {"card": "lifted", "accent": "#2c5aa0"}
   ```

## When NOT to use this

- For yes/no or pick-one-of-2 questions where text is fine — keep using
  `AskUserQuestion`, it's faster.
- When the user is on a headless / SSH-only session — the browser open
  silently no-ops. Fall back to `AskUserQuestion`.
- When the answer is a long paragraph the user types — text Q&A is fine.

## Limits

- Default submission timeout is 600 seconds. Override with
  `ASK_VISUAL_TIMEOUT=<seconds>` in the env.
- Server binds to `127.0.0.1` only on a random free port. No auth, no CORS,
  one POST and out.
