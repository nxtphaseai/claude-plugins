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
| [agent-eval](plugins/agent-eval/)         | Auto-grades the agent's last turn against your prompt (and optional project rules in `eval/eval.md`) and appends a card to `eval/eval.html`. |
| [ask-visual](plugins/ask-visual/)         | Visual `AskUserQuestion`: agent serves a one-shot HTML form (cards, sliders, color pickers, anything) on localhost and feeds the submission back as JSON. |
| [nxtphase-design](plugins/nxtphase-design/) | The Nxt Phase AI brand & design system as a skill — colors, type, fonts, logos, dot-icon rules, a website UI kit, and a 10-slide deck template. Dieter Rams / Braun-inspired. |
| [nxtphase-demo-video](plugins/nxtphase-demo-video/) | How we make demo and sales videos: Remotion scaffold, the fixed brand end card, the ElevenLabs voice-over pipeline, showing real interfaces instead of redrawing them, anonymisation rules, a writing-style guide that keeps AI vocabulary out of client copy, and an optional step that publishes the matching demo page in the Notion Demo Library. |
| [nxtphase-documentatie](plugins/nxtphase-documentatie/) | The two hand-over documents at the end of a project: a user manual for the team that uses the tool and a technical documentation for the IT department that runs it, as editable Word documents in the house style. Verifies every claim against the code and the live Azure deployment, asks what it cannot verify, and ships a standard-library-only docx generator. |
| [deploy-nxtphase-demo](plugins/deploy-nxtphase-demo/) | Puts any app on `<name>.demo.nxtphase.ai`: creates the Railway project, registers the domain, writes the Cloudflare DNS records, deploys, and verifies. Ships no credentials; it reads two tokens from a `.env` you create, and points you at the shared password manager where both live. |

More on the way.

### Listed here, built elsewhere

| Plugin | Upstream | What it does |
| --- | --- | --- |
| `claude-security` | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-security) | Deep vulnerability scanning of your own code inside your Claude Code session, every finding challenged before it is reported, survivors turned into patches you apply when you choose. |

We do not vendor a copy of these. The marketplace entry points straight at the
upstream repository with no `ref` and no `sha`, so every install resolves to
whatever is on their default branch at that moment. Anthropic ships an update,
you get it on your next `claude /plugin marketplace update nxtphaseai`, and we
change nothing here.

```bash
claude /plugin install claude-security@nxtphaseai
```

If you also have `claude-plugins-official` registered you will see the same
plugin twice. They are the same thing; the marketplace suffix picks one.
Upstream plugins keep their own license, which is not ours to state.

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

### Listing a plugin someone else maintains

A `source` does not have to be a path inside this repo. To re-list a plugin that
lives in another repository, point at it directly and leave `ref` and `sha` off,
so it always resolves to that repo's default branch:

```json
{
  "name": "claude-security",
  "description": "...",
  "author": { "name": "Anthropic" },
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/anthropics/claude-plugins-official.git",
    "path": "plugins/claude-security"
  },
  "homepage": "https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-security"
}
```

Use `git-subdir` when the plugin sits in a subdirectory of a bigger repo, and
`{"source": "github", "repo": "owner/repo"}` when the repo *is* the plugin.

No `version` field: the version comes from the upstream `plugin.json` and we
would only get it wrong. No `license` field either, for the same reason. Adding
a `sha` would freeze the plugin at one commit, which is the opposite of what we
want here.

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
