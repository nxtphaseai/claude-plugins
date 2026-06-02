# nxtphase-design

The Nxt Phase AI brand and design system as a Claude Code skill.

Bundles everything an agent needs to design on-brand for Nxt Phase AI:
color and type tokens, the two brand fonts, logos and dot-icon SVGs,
brand photography, design-system specimen pages, a website UI kit, and
a 10-slide presentation template. Dieter Rams / Braun-inspired — warm
cream canvas (never pure white), near-black ink, one Signal Green accent,
PP Editorial New over Switzer, calm motion, no decoration.

Invoke as `/nxtphase-design:nxt-phase-ai-design` (or whatever your client
exposes the skill as) when you want to design, build, or write anything
for Nxt Phase AI: production interfaces, marketing pages, mocks, decks,
or assets.

## Install

```bash
git clone git@github.com:nxtphaseai/claude-plugins.git
bash claude-plugins/plugins/nxtphase-design/install.sh           # into ./.claude/ of the current git repo
# or
bash claude-plugins/plugins/nxtphase-design/install.sh --user    # user-wide into ~/.claude/
```

Or via the marketplace:

```bash
claude /plugin marketplace add nxtphaseai/claude-plugins
claude /plugin install nxtphase-design@nxtphaseai
```

After install, **restart Claude Code** so the skill loads.

To remove:

```bash
bash plugins/nxtphase-design/install.sh --uninstall
```

## What it installs

| Path                                       | Role                                                             |
| ------------------------------------------ | ---------------------------------------------------------------- |
| `<scope>/skills/nxt-phase-ai-design/SKILL.md`            | Skill manifest with brand voice, tone, and core rules.           |
| `<scope>/skills/nxt-phase-ai-design/README.md`           | Full design-system reference (color, type, motion, logos, etc.). |
| `<scope>/skills/nxt-phase-ai-design/colors_and_type.css` | CSS variables and `@font-face` rules — link this in every artifact. |
| `<scope>/skills/nxt-phase-ai-design/fonts/`              | PP Editorial New + Switzer (OTF).                                |
| `<scope>/skills/nxt-phase-ai-design/assets/`             | Logos (4 colorways), dot-icon examples, brand photography.       |
| `<scope>/skills/nxt-phase-ai-design/preview/`            | Specimen cards (open in a browser to eyeball the system).        |
| `<scope>/skills/nxt-phase-ai-design/slides/`             | 10-slide deck template (`index.html` + per-slide HTML).          |
| `<scope>/skills/nxt-phase-ai-design/ui_kits/website/`    | Marketing-site recreation (`index.html` + JSX components).       |

`<scope>` is the project root's `.claude/` for the default install, or
`~/.claude/` for `--user`.

## How the agent uses it

When the skill is invoked, the agent reads `SKILL.md` (manifest + core
rules), then `README.md` for the full system, then explores
`colors_and_type.css`, `assets/`, `slides/`, `ui_kits/website/`, and
`preview/` as needed.

For throwaway HTML artifacts the agent copies assets out and always
links `colors_and_type.css`, so tokens stay correct. For production
code the agent imports the same CSS and follows the rules in
`README.md`.

## Core rules (the short version)

- Warm cream canvas, near-black ink, **one** Signal Green accent.
- PP Editorial New for headlines, Switzer everywhere else. Two weights max.
- One supporting color per section, at most.
- Soft generous radii (never pills). Warm restrained shadows.
- Calm ~200ms motion. No bounce, no spring.
- Dot-based icons (espresso on light, green when active). **Never emoji.**
- *Braun, not Apple. Editorial, not startup.*

## When NOT to use it

Anything outside Nxt Phase AI — this skill encodes one specific brand
system. For generic UI styling, use a different skill or write
unstyled HTML.

## What it does NOT do

- Doesn't modify your code.
- Doesn't pull from any remote source — everything is bundled.
- Doesn't ship the 31-page brand-book PDF or the original `.pptx` —
  every rule needed at runtime is distilled into `README.md` and
  `colors_and_type.css`.
- Doesn't ship a full dot-icon library — only four example glyphs. New
  icons are generated on demand via the brand's icon builder.
