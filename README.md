# NxtPhase plugin marketplace

A single Claude Code plugin marketplace for the NxtPhase team. Subscribe
once, install whatever you need, get updates by re-subscribing.

## For users — installing plugins

```bash
# One-time: register this marketplace in Claude Code
claude /plugin marketplace add nxtphase/claude-plugins

# Browse and install
claude /plugin install agent-eval@nxtphase
```

After install, **restart your Claude Code session** so commands and hooks
load.

To upgrade a plugin to whatever's on `main`:

```bash
claude /plugin marketplace update nxtphase
claude /plugin install agent-eval@nxtphase
```

To remove:

```bash
claude /plugin uninstall agent-eval
```

If your version of Claude Code does not yet support the `/plugin` family
of commands, every plugin under `plugins/` also ships with a manual
installer. For example:

```bash
git clone git@github.com:nxtphase/claude-plugins.git
bash claude-plugins/plugins/agent-eval/install.sh
```

## Available plugins

| Plugin                              | What it does                                                                                  |
| ----------------------------------- | --------------------------------------------------------------------------------------------- |
| [agent-eval](plugins/agent-eval/)   | Auto-grades the agent's last turn against your prompt and appends a card to `eval/eval.html`. |

More on the way.

## For authors — adding a new plugin

1. Create `plugins/<name>/` with at minimum:

   ```
   plugins/<name>/
   ├── .claude-plugin/plugin.json     # plugin manifest (name, version, author)
   ├── README.md
   └── (commands/, hooks/, agents/, …)
   ```

2. Add an entry to `.claude-plugin/marketplace.json`:

   ```json
   {
     "name": "<name>",
     "description": "...",
     "version": "0.1.0",
     "source": "./plugins/<name>",
     "keywords": ["..."],
     "license": "MIT"
   }
   ```

3. Bump the marketplace `metadata.version`.

4. Open a PR against `main`. Once merged, teammates pick it up via
   `claude /plugin marketplace update nxtphase`.

## Versioning

Each plugin's `version` follows semver. The marketplace itself has its own
version in `metadata.version` so users can tell when *anything* in the
marketplace changed even if individual plugin versions didn't move.

## Conventions

- Hook scripts use `${CLAUDE_PLUGIN_ROOT}` so they keep working regardless
  of where the plugin gets installed on disk.
- Hooks set a recursion guard env var (e.g. `<PLUGIN>_RUNNING=1`) before
  any nested `claude` calls so they can't loop.
- Hooks fail soft — missing `claude` / `jq` / `git` should log to stderr
  and exit 0, never block the user's turn.
- Each plugin ships its own README explaining what it does, what it
  installs, and how to disable / uninstall.

## License

MIT. See `LICENSE`.
