#!/usr/bin/env python3
"""
ask-visual: spin up a one-shot localhost HTTP server, serve a custom HTML
form (whatever the agent wrote), wait for the user to submit, print the
form data as a JSON object to stdout, and exit.

Usage:
    python3 ask-visual.py <html-file>

The HTML file should contain only the *body* of the form. Wrapper page,
<form> tag, and submit JS are injected. Any element with a `name` attribute
ends up in the result. The clicked submit button's name/value is also
included, so multiple "Pick this" buttons in different cards work.

Stdlib only. ~100 lines. The script exits as soon as one submission lands;
no daemon, no cleanup.
"""

import http.server
import os
import socketserver
import sys
import threading
import time
import webbrowser
from pathlib import Path

WRAPPER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Claude is asking...</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
         max-width: 760px; margin: 40px auto; padding: 0 20px; color: #1a1a1a;
         background: #f7f6f2; line-height: 1.5; }
  h1, h2, h3 { letter-spacing: -.01em; }
  input, select, textarea, button { font-family: inherit; font-size: 14px; }
  input[type="text"], input[type="number"], input[type="email"], textarea, select {
    border: 1px solid rgba(17,17,16,.18); border-radius: 6px; padding: 8px 10px;
    background: #fff; }
  input[type="range"] { width: 100%; }
  textarea { width: 100%; min-height: 80px; }
  button { background: #1a1a1a; color: #fff; border: 0; padding: 9px 18px;
           border-radius: 6px; cursor: pointer; transition: background .15s; }
  button:hover { background: #333; }
  button:disabled { background: #999; cursor: wait; }
  .ask-fallback-submit { margin-top: 24px; }
  .done { padding: 80px 20px; text-align: center; color: #555; font-size: 16px; }
  .meta { color: #6a6862; font-size: 12px; margin-bottom: 18px; }
</style>
</head>
<body>
<div class="meta">ask-visual &middot; localhost form, single-shot</div>
<form id="ask-form">
__USER_HTML__
__FALLBACK_SUBMIT__
</form>
<script>
  const form = document.getElementById('ask-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {};
    for (const el of form.elements) {
      if (!el.name) continue;
      if (el.type === 'submit' || el.type === 'button') continue;
      if (el.type === 'checkbox') {
        data[el.name] = el.checked;
      } else if (el.type === 'radio') {
        if (el.checked) data[el.name] = el.value;
      } else if (el.tagName === 'SELECT' && el.multiple) {
        data[el.name] = Array.from(el.selectedOptions).map(o => o.value);
      } else {
        data[el.name] = el.value;
      }
    }
    const sub = e.submitter;
    if (sub && sub.name) {
      data[sub.name] = sub.value !== '' ? sub.value : (sub.textContent || '').trim();
    }
    for (const el of form.elements) el.disabled = true;
    try {
      await fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
    } catch (err) { /* server may have shut down between fetch and response */ }
    const done = document.createElement('div');
    done.className = 'done';
    done.textContent = 'Submitted. You can close this tab.';
    document.body.replaceChildren(done);
  });
</script>
</body>
</html>"""


def main():
    if len(sys.argv) != 2:
        print("usage: ask-visual.py <html-file>", file=sys.stderr)
        sys.exit(2)
    src = Path(sys.argv[1])
    if not src.is_file():
        print(f"ask-visual: file not found: {src}", file=sys.stderr)
        sys.exit(2)
    user_html = src.read_text(encoding="utf-8")

    # Auto-add a "Submit" button if the agent's HTML contains no <button>.
    has_button = "<button" in user_html.lower()
    fallback = "" if has_button else (
        '<button type="submit" class="ask-fallback-submit">Submit</button>'
    )
    page = (
        WRAPPER
        .replace("__USER_HTML__", user_html)
        .replace("__FALLBACK_SUBMIT__", fallback)
    )

    state = {"body": None}
    done = threading.Event()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))

        def do_POST(self):
            if self.path != "/submit":
                self.send_response(404)
                self.end_headers()
                return
            length = int(self.headers.get("Content-Length", "0") or "0")
            body = self.rfile.read(length).decode("utf-8", "replace")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
            state["body"] = body
            done.set()

        def log_message(self, *_a, **_kw):
            pass  # silence access log

    with socketserver.TCPServer(("127.0.0.1", 0), Handler) as httpd:
        port = httpd.server_address[1]
        url = f"http://127.0.0.1:{port}/"
        print(f"[ask-visual] form at {url}", file=sys.stderr)
        print("[ask-visual] waiting for submission (Ctrl-C to abort)", file=sys.stderr)
        try:
            webbrowser.open(url)
        except Exception:
            pass

        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()

        timeout_s = int(os.environ.get("ASK_VISUAL_TIMEOUT", "600"))
        if not done.wait(timeout=timeout_s):
            print(f"[ask-visual] timeout after {timeout_s}s", file=sys.stderr)
            httpd.shutdown()
            sys.exit(3)

        # Tiny grace period so the 200 response flushes before we tear down.
        time.sleep(0.1)
        httpd.shutdown()

    sys.stdout.write(state["body"] or "{}")
    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[ask-visual] aborted", file=sys.stderr)
        sys.exit(130)
