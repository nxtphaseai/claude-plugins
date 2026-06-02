# Slides — Presentation Template

A recreation of the **Nxt Phase AI presentation template** (from `Nxt Phase AI - Template Guidelines.pptx`, theme "Nxt Phase AI"). Dieter Rams / Braun deck system: warm cream slides, Editorial serif headlines, one accent, section color-coding.

## Run
Open `index.html` — a navigable deck (`deck-stage.js`): ←/→ to move, click thumbnails, press `R` to reset. Authored at **1280×720** (16:9). Print → Save as PDF gives one page per slide.

## Slide types
Each type is also a standalone single-slide file (used for the Design System cards):

| File | Type | Notes |
|---|---|---|
| `01-title.html` | Title | Cream bg, logo, big Editorial headline + lead |
| `02-section-divider.html` | Section divider | **Signal Green** bg, oversized italic numeral |
| `03-transition.html` | Transition | Chapter break, italic-orange emphasis word |
| `04-problem.html` | Problem framing | 3 columns, **orange italic numerals** 01–03 |
| `05-journey.html` | Journey | Numbered phase pills, active pill = off-black |
| `06-value-grid.html` | Value grid | 2×2 traits, dot-icon tiles on pastels |
| `07-stats.html` | By the numbers | Three big numerals, orange accent glyphs |
| `08-cases.html` | Case studies | Photo cards + overline tags (MCB, NHA) |
| `09-quote.html` | Quote | Editorial italic pull quote + attribution |
| `10-closing.html` | Closing / CTA | Off-black band, mark + contact |

`index.html` holds the same slides as static `<section>` children of `<deck-stage>` — edit headings directly in place. The standalone files are generated from those sections; if you change the deck, re-derive them or edit both.

## System rules (from the guidelines)
- **Section color-coding:** each section maps to a signal color. Max **one** supporting color per section, **two** per full presentation.
- Title & body slides on cream; dividers on Signal Green; closing on Off-Black.
- Numerals in problem/stat contexts: Editorial **italic, Signal Orange**.
- Headlines PP Editorial New; everything else Switzer. Overlines uppercase 0.12em.

## Disclaimers
- Copy is shown in **English** (the source deck mixes Dutch client copy with English reference notes). Swap to Dutch for client-facing decks.
- Case-study photos use brand image-set stand-ins — replace the `.ph` images with real case visuals/screenshots.
- Client names in proof slides are real references from the source; verify before external use.
