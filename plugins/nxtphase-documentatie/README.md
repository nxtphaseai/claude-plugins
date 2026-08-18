# nxtphase-documentatie

The two documents we hand over at the end of a project, as a Claude Code skill.

Every NxtPhase delivery closes with a **Gebruikershandleiding** for the team that will
use the tool, and a **Technische documentatie** for the IT department that will run it.
This skill writes both from the project folder and builds them as editable Word documents
in our house style.

Built from four delivered documents: the user manual and the technical documentation for
one client's mail analysis and routing tools, and the delivery report and technical
documentation for another client's Outlook add-in and quote generator. The structure, the
recurring building blocks, and the house style come straight out of those.

## What it gives an agent

**A verification discipline, first.** The skill does not start writing. It explores the
repository (deployment workflows, infrastructure code, startup scripts, the environment
variables the code actually reads, the thresholds and limits baked into the code) and then
checks the real deployment with read-only `az` commands. Every claim in the finished
document traces back to a file and line, to the output of a command, or to an explicit
answer from the user. Anything that traces to none of those does not get written. Claims
about cost, security, availability, recovery, and privacy get the strictest treatment,
because those are the ones a reader will act on.

Findings go in `docs/oplevering/bronnen.md` alongside the drafts, so the documentation
stays checkable after the fact and the next round does not have to dig again.

**The questions it must ask instead of guess.** Do we hand over the source as a zip, or
transfer the repository, or neither? Through which channel do the credentials get shared?
Does the CI/CD pipeline stay on our GitHub? Who administers the tenant afterwards? Is
there a support arrangement, and may we say so? None of that is in the code, so the skill
asks. "I don't know" is a valid answer and lands the topic in the open-points list rather
than in a sentence that reads as a promise.

**The structure of both documents**, with the building blocks that recur across the real
deliveries: "Zo gebruik je ...", "Goed om te weten" for the boundaries, "Let op:" for
what is not finished yet, a table explaining the fields the user sees on screen, and a
chapter on correcting the tool and giving feedback. On the technical side: the resource
table, app settings per app, delivered artifacts, the secrets overview (names, never
values), the built-in limits read line by line out of the code, and the "wat je beter niet
doet" list.

**A writing-style guide** that keeps AI vocabulary and em-dashes out of client copy, and
that treats vagueness as no escape from the burden of proof: "roughly 50 per round" needs
a source just as much as "50 per round" does.

**A .docx generator** in `assets/build_docx.py`. Standard library only, so no pip install,
no pandoc, and no Word needed to build. It takes Markdown with front matter and produces
the cover page, the clickable table of contents, chapter page breaks, branded tables with
a repeating header row, code blocks, callouts, images with captions, and the footer with
the page number and the logo. All formatting runs through real Word styles, so the client
can genuinely edit the result: change one style and the whole document follows.

## Install

```bash
/plugin marketplace add nxtphaseai/claude-plugins
```

```bash
/plugin install nxtphase-documentatie@nxtphaseai
```

Or manually, from a clone of this repo:

```bash
bash plugins/nxtphase-documentatie/install.sh --user
```

`install.sh --uninstall` removes it again. The installer warns if Python 3.8+ or the Azure
CLI is missing.

## Use

Run it from the project folder of the client project:

```
Maak de opleverdocumentatie voor dit project.
```

The skill explores, verifies, asks its questions, proposes the table of contents of both
documents for approval, writes the Markdown sources to `docs/oplevering/`, and builds:

```
docs/oplevering/
  gebruikershandleiding.md
  technische-documentatie.md
  bronnen.md
  260804 Gebruikershandleiding.docx
  260804 Technische documentatie.docx
```

To update a document later, edit the Markdown source and rebuild. The `.docx` is output,
never the source.

## The fonts are not in here

The house style uses **PP Editorial New** for the cover and chapter headings and
**Switzer Medium** for everything else. Those are licensed fonts and this repository is
public, so they are not shipped and not embedded in the generated documents. On a machine
without them, Word substitutes. That is exactly what happens with the existing delivered
documents too.

If a document has to look precisely right, open and export it from a workstation that has
the brand fonts installed. The `nxtphase-design` plugin in this repo carries the *Tight*
variants for web and slides; they have different metrics and are not a drop-in replacement
here.

## What it deliberately does not do

- It never writes to Azure. Every command it runs is read-only. A missing permission is a
  finding it reports, not a reason to infer what is probably deployed.
- It never puts a secret, key, password, connection string, or publish profile in a
  document. Names and locations only.
- It does not invent an SLA, a support window, or a cost figure. Without an answer or a
  source, the topic goes in the open points.
