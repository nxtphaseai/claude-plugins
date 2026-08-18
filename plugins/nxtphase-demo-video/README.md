# nxtphase-demo-video

How we make demo and sales videos at Nxt Phase AI, as a Claude Code skill.

A demo video shows a tool we actually built, to someone who recognises the
problem. Short, calm, concrete. No advertising language, no stock footage, and
no redrawn screens.

Built from two delivered videos: one of 2:00 covering two web apps across eight
scenes, and one of 1:26 covering an email add-in and a generated document across
seven. Ask internally for the recordings.

## What it gives an agent

**Two hard rules.** Interfaces are *shown*, never redrawn: the CSS and markup
come straight out of the product's source, so the video changes when the app
does. And nothing traceable to the client goes in — no name, logo, product
names, real room or menu names, real data, or photos of existing places and
people. Brand colours get shifted too, because a house style is as recognisable
as a name.

**A working scaffold** in `assets/`: theme, timing model, animation helpers,
window and cursor components, a CSS extraction script, and an ElevenLabs
voice-over script that records one continuous take and cuts it on character
timestamps.

**The end card**, fixed. Wordmark, mesh gradient, and the "We make AI Work"
tagline, with the proportions between logo and tagline calculated from the logo
file and the font metrics rather than eyeballed. Copy it unchanged.

**An optional last step**: publishing the matching demo page in the Notion
**NXT Phase AI - Demo Library**. It finds the project's Notion page from the
codebase, pulls the facts from the project, writes the Dutch and English copy in
the house style of the existing pages, and creates the page under the Library.
It can also run standalone for a project that already has a recording. The
video-embedding part is the fiddly bit and the reference document covers it: the
Notion MCP tops out at 20 MiB per upload, and a SharePoint link will not play
inside a `<video>` block.

**Six reference documents**: showing interfaces exactly, anonymising, the
voice-over pipeline and tone, fonts and their licences, the pitfalls that cost
real time (shimmering scrolls, the tip of the mouse cursor, transparent cards,
layouts that jump), a delivery checklist built from actual client feedback, and
the Demo Library page template with its writing style.

## Install

```bash
git clone git@github.com:nxtphaseai/claude-plugins.git
bash claude-plugins/plugins/nxtphase-demo-video/install.sh           # into ./.claude/ of the current git repo
# or
bash claude-plugins/plugins/nxtphase-demo-video/install.sh --user    # user-wide into ~/.claude/
```

Or via the marketplace:

```bash
claude /plugin marketplace add nxtphaseai/claude-plugins
claude /plugin install nxtphase-demo-video@nxtphaseai
```

Restart Claude Code afterwards so the skill is picked up.

## One thing you have to supply yourself

**The end card font is not in this repo.** `PPEditorialNew-Italic.otf` comes
from Pangram Pangram and this repository is public, so shipping it here would be
redistribution. Get it internally and drop it in `public/fonts/` of your video
project.

Without it the tagline silently falls back to Georgia and the render still
succeeds, so check the end card with a still. The *Tight* cut shipped by the
`nxtphase-design` plugin is not a substitute: its letter widths differ, and the
tagline width in `Outro.tsx` is derived from the regular Italic.

Switzer, used for the framing text, is deliberately absent for the same reason —
its licence allows use but not redistribution. It is loaded from Fontshare during
the render and falls back to Inter without a network. See
`skills/nxtphase-demo-video/reference/fonts.md`.

## Notion access

The Demo Library step needs the Notion MCP connected, with access to the **Sales
Wiki** teamspace. Without it the rest of the skill works fine; that step just
cannot run.

## Related

`nxtphase-design` covers the brand and design system in general. This plugin is
about video and the demo page that goes with it.
