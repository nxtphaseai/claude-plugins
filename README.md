# NxtPhase plugin marketplace

A single Claude Code plugin marketplace for the NxtPhase team. Subscribe
once, install whatever you need, get updates by re-subscribing.

## For users — installing plugins

```bash
# One-time: register this marketplace in Claude Code
claude /plugin marketplace add nxtphaseai/claude-plugins

# Browse and install
claude /plugin install agent-eval@nxtphaseai
```

After install, **restart your Claude Code session** so commands and hooks
load.

To upgrade a plugin to whatever's on `main`:

```bash
claude /plugin marketplace update nxtphaseai
claude /plugin install agent-eval@nxtphaseai
```

To remove:

```bash
claude /plugin uninstall agent-eval
```

If your version of Claude Code does not yet support the `/plugin` family
of commands, every plugin under `plugins/` also ships with a manual
installer. For example:

```bash
git clone git@github.com:nxtphaseai/claude-plugins.git
bash claude-plugins/plugins/agent-eval/install.sh
```

## Available plugins

| Plugin                              | What it does                                                                                  |
| ----------------------------------- | --------------------------------------------------------------------------------------------- |
| [agent-eval](plugins/agent-eval/)   | Auto-grades the agent's last turn against your prompt (and optional project rules in `eval/eval.md`) and appends a card to `eval/eval.html`. |
| [ask-visual](plugins/ask-visual/)   | Visual `AskUserQuestion`: agent serves a one-shot HTML form (cards, sliders, color pickers, anything) on localhost and feeds the submission back as JSON. |

More on the way.

## Claude Desktop App?

These plugins are **Claude Code only**. They will not load into the Claude
Desktop app, because they rely on Claude Code-specific surfaces that Desktop
doesn't have:

- Hook events (`UserPromptSubmit`, `Stop`, ...) that fire around each agent turn.
- Shell execution for hook scripts (`bash`, `git`, `jq`, the `claude` CLI).
- File-based slash commands under `commands/*.md`.
- A working directory / git repo to diff against.

If you want to extend Claude Desktop, the supported extension model there is
[MCP servers](https://modelcontextprotocol.io). Nothing in this marketplace
ships as an MCP server today.

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
   `claude /plugin marketplace update nxtphaseai`.

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
