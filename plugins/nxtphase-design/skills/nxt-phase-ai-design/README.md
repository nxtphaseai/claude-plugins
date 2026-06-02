# Nxt Phase AI — Design System

> **"Pragmatic by design. Built on the principles of Dieter Rams."**

This is the working design system for **Nxt Phase AI** — colors, type, fonts, logos, imagery, iconography, a website UI kit, and a presentation slide template. Use it to build well-branded interfaces, decks, and assets, for production or throwaway mocks.

---

## 1. Company & Product Context

**Nxt Phase AI** (stylized **nxt phase ai**) is a Netherlands-based **AI consultancy** for mid-market companies. A small senior team (≈11 practitioners) that helps businesses move AI *"van een onderwerp naar een werkend instrument"* — from a topic into a working instrument.

- **Mission:** *To make pragmatic AI work.* "Not the AI of keynote speeches and pitch decks, but the AI that runs in production, saves real money, and gives teams capabilities they didn't have yesterday."
- **Brand promise:** *"We never sell a vision we can't build. If we recommend it, we can deliver it. If we can't deliver it, we'll tell you."*
- **The Four Pillars:** **01 Educate · 02 Prioritise · 03 Build · 04 Run.**
- **Anchor:** Dieter Rams / Braun product design. *"Good design is as little design as possible."* Functional beauty, restrained color, systematic structure, **one intentional accent**.
- **Positioning shorthand:** *Braun, not Apple. Editorial, not startup.* Warm and human, confident and direct, minimal and purposeful, technically credible.
- **Market:** Mid-market, NL-focused, GDPR-compliant. Copy is frequently in **Dutch** (client-facing decks) with **English** for internal/reference material.

Real proof points referenced in materials: MCB Staalhandel (wholesale — AI in Outlook + SAP), NHA Opleidingen (education — automated exam assessment), "20+ clients in production", "15+ years experience".

### Products / surfaces represented here
1. **Marketing website** — `nxtphase.ai`. Hero, value props, journey/pillars, social proof, stats, case studies, CTA. → `ui_kits/website/`
2. **Presentation template** — a full reference + example deck ("Template / V4"). Title, transition, problem-framing, journey, social proof, value-prop grid, stats, case studies, closing. → `slides/`

There is **no application / SaaS product** in the provided materials — this is a consultancy brand and its go-to-market surfaces.

### Original sources (distilled into this kit)
This kit is the distilled, runtime-ready slice of the full brand package. The heavy source binaries (the 31-page brand-book PDF and the original template `.pptx`) are **not** bundled — everything needed to design on-brand lives in the files below. The originals derive from:
- **Brand book PDF** — strategy, logo, color, type, photography, iconography, applications. Distilled into this `README.md` + `colors_and_type.css`.
- **Template deck `.pptx`** — reference + example deck. Recreated as editable HTML in `slides/`.
- **Logo files** — Logo, Mark, Stacked × 6 colorways. The four most-used web SVGs ship in `assets/logos/`.
- **Fonts** — PP Editorial New + Switzer (OTF), in `fonts/`.
- **Image set** — brand photography, web-optimised in `assets/images/`.
- **Icon builder** referenced in the deck: `https://icon-builder-delta.vercel.app` (generates the dot-based icons).

---

## 2. Content Fundamentals

How Nxt Phase writes. The voice is **pragmatic, direct, senior, engineered, honest** — never theoretical, blunt, exclusive, decorated, or modest.

- **Plain language, not jargon.** "We talk about what works, not what could work." Say things plainly to be useful, not to sound smart. No "synergy", no "leverage", no neural-net mysticism.
- **Direct, warm in delivery.** Short declarative sentences. "We say what we mean without hedging." Directness ≠ coldness.
- **"We" and "you/jullie".** First-person plural for the team ("We helpen…", "Wij sluiten aan…"), second person for the client ("waar jullie staan"). Collaborative, not corporate-distant.
- **Bilingual.** English for reference/internal ("Use this slide for chapter breaks"). **Dutch** for client-facing copy ("AI zonder hype.", "Strategie en uitvoering.", "Klaar om de eerste stap te zetten?").
- **Casing.** Sentence case everywhere for headlines and body. **UPPERCASE only for overlines/labels** (e.g. `DE OBSTAKELS`, `SOCIAL PROOF`, `BY THE NUMBERS`) — 11px, medium, 0.12em tracking. Never uppercase for emphasis in running text.
- **Numerals as structure.** Pillars and steps numbered `01 02 03 04`. In problem/stat contexts numerals render in **Signal Orange, italic** (Editorial italic). Stats are blunt: "20+", "100%", "8 weken".
- **No hype, no false modesty.** "No hype. No black boxes." Confident about what they deliver, transparent about what they can't.
- **Emoji:** **none.** Not part of the brand. Iconography is the dot-icon system, never emoji.

**Voice examples (verbatim):**
- *"AI that delivers results, not just promises."*
- *"We're a team of 11 senior AI practitioners who help mid-market companies build AI that actually works. No hype. No black boxes."*
- *"AI zonder hype. Strategie en uitvoering."*
- *"Pilots komen nooit in productie."* (problem framing)
- *"Klaar om de eerste stap te zetten? Vertel ons waar jullie staan."* (CTA)
- *"As little design as possible. But not less."* (closing — the Rams credo)

---

## 3. Visual Foundations

The whole system is **Dieter Rams / Braun**: warm neutral canvas, near-black ink, one green accent, systematic grid, generous negative space. "Editorial magazine feature, not corporate brochure."

### Color
- **Warm, layered light canvas** — never pure white. Page base `#F9F6F1`, surfaces step down to cream `#F5F0E8`. Ink is near-black `#090909`. Secondary text is **Stone** `#9B9590`.
- **One accent: Signal Green `#3E9B5D`.** Used for active/selected states, links, and a single deliberate highlight — *never* as decoration or in multiples.
- **Supporting colors** (Signal Orange `#E86B10`, Post-it Blue `#86C0D5`, Post-it Pink `#F7DFDE`) and **decorative pastels** (Soft Mint, Soft Peach) are rationed: **maximum one supporting color per slide/section, two per full presentation**. Orange is for key callouts / numerals; never as body text on cream (contrast too low).
- Imagery shadow/ink color is **Espresso `#3D2B1F`** (also the dot-icon ink).

### Type
- **Two families only.** **PP Editorial New** (high-contrast serif, angular details) for display + headlines; **Switzer** (geometric humanist sans) for body + UI. Never swap roles, never substitute system fonts.
- Headlines weight 400 only. Body uses Regular/Medium/Semibold. **Max 2 weights per page/slide.**
- **Italic = emphasis only** (pull quotes, one highlighted word) — never full paragraphs, never decoration.
- Overlines/labels: uppercase, 11px, medium, **0.12em** tracking — nothing else uppercase. Never letter-space Switzer body. Min body 16px web / 10pt print. Don't center body longer than 2 lines. Underline = links only.

### Backgrounds, depth & motion
- **Backgrounds:** flat warm solids (cream / surface tones) or full-bleed **editorial photography**. No blue gradients, no neural-net abstractions. A subtle warm gradient (espresso→amber) exists for special hero/divider moments only.
- **Photography:** warm, natural-to-slightly-desaturated, **Kodak Portra 400** feel, shadows in warm brown. Show real teams at whiteboards, hands-on technical work, workshops, architectural detail, Braun-style still life, and **dimensional glass/amber refraction** abstracts. Never: glowing brains, robots, blue-tinted tech close-ups, stock-photo tableaux, people excitedly pointing at screens.
- **Corner radii:** soft and generous, **not** pills. Cards/tiles ~16–24px (the icon grid uses a 24px corner radius). Buttons are softly rounded rectangles, not capsules.
- **Cards:** flat warm surface, hairline border `rgba(9,9,9,0.10)` and/or a very soft warm shadow (`rgba(61,43,31,…)`). Never a glossy or cool-gray shadow. No colored left-border-accent cards.
- **Borders:** thin warm-black hairlines for structure and grid lines. Structure is visible and systematic — Rams grid alignment.
- **Shadows:** restrained, warm-brown tinted, low opacity. Elevation is a whisper, not a pop.
- **Transparency/blur:** minimal. Used sparingly for image-overlay legibility (a soft espresso scrim under text on photos), not as a glassmorphism effect.
- **Motion:** calm and functional. Short (≈200ms) fades and small translate/opacity moves on a smooth ease (`cubic-bezier(0.22,0.61,0.36,1)`). **No bounce, no spring, no flashy transitions.** "Unobtrusive."
- **Hover states:** subtle — slightly darker fill or a hairline that deepens; green elements darken toward `#2A6B3F`. **Press:** a touch darker, optional 1px settle; no dramatic shrink.
- **Layout rules:** generous margins and negative space; consistent 8px spacing grid; one idea per section; numerals and overlines anchor structure. Every element must earn its place ("If something is there, it has a reason").

---

## 4. Iconography

**Dot-based icon system — "Reduced to Essentials."** Icons are drawn as evenly-spaced dots tracing a shape, matching the chevron/dot language of the logo.

- **Grid:** 24 × 24px, 2px padding. **Corner radius 24px** on tiles. **Terminals:** flat / square.
- **Dot sizing:** 16px icon → 1px dots (inline w/ body); 24px → 1px dots (default UI, nav); 32px → 1.5px dots (feature cards); 48px → 1.5px dots (section markers, pillars).
- **Color rules:** Default **Espresso `#3D2B1F` on light**; inverted **Cream on dark**; **Signal Green for active/selected states only**. **Never multi-color, never gradient.**
- **Generation:** icons are produced with the brand's icon builder (`https://icon-builder-delta.vercel.app`) — any glyph rendered in the dot style. The four example icons shipped in the deck (`assets/icons/icon-a…d.svg`) are dot renderings (airplane, ambulance, beanie, binary) demonstrating the system, **not** fixed pillar marks.
- **SVGs** are the delivery format (espresso-filled `<circle>` dots). Copied into `assets/icons/`.
- **No emoji. No Unicode glyphs as icons.** The dot system is the only icon vocabulary.

> ⚠️ **Substitution note:** because brand icons are *generated on demand* in the dot style, this kit can only ship the four example dot-SVGs. For new icons, regenerate via the icon builder. Where a functional UI needed a glyph not available as a dot icon, the kit keeps iconography minimal (logo mark, chevrons, simple hairline glyphs) rather than introducing an off-brand icon set. **Flag for the user:** if you need a working dot-icon library, point me at an export from the builder.

---

## 5. Logos — "The Shift"

Two overlapping chevrons: *where you are, where we take you, and the work done together — a phase shift made visual.*

- **Variants:** Primary (mark + wordmark), Stacked, Logotype (wordmark only), Mark only.
- **Colorways:** Off Black, Cream, Signal Green, Stone, Black, White.
- **Clear space:** minimum = height of the "N" in the wordmark, all sides.
- **Minimum sizes (digital):** Primary 140px · Stacked 80px · Mark only 24px.
- **Usage:** Off-Black on light backgrounds, Cream on dark. Mark may stand alone where space is tight. The four most-used colorways (Off Black, Cream, Signal Green, Stone) ship as web SVGs in `assets/logos/` — logo + mark + stacked. The full set (all six colorways, PNG/SVG, print/web) lives in the original brand package; recolor an existing SVG if you need Black or White.

---

## 6. Index / Manifest

Root files:
- **`README.md`** — this document.
- **`colors_and_type.css`** — CSS variables (colors, surfaces, type scale, radii, spacing, shadows, motion) + semantic type classes + `@font-face`. **Import this in every artifact.**
- **`SKILL.md`** — Agent Skill manifest (for use in Claude Code).
- **`fonts/`** — PP Editorial New (Regular, Italic) + Switzer (Regular, Medium, Semibold), OTF.
- **`assets/logos/`** — logo + mark + stacked, in Off Black / Cream / Signal Green / Stone (web SVG).
- **`assets/icons/`** — dot-icon example SVGs.
- **`assets/images/`** — brand photography (web-optimised JPG): warm workspace/collaboration, a dimensional amber-glass abstract, Braun still life.
- **`preview/`** — Design System specimen cards (colors, type, components, spacing, etc.) — open in a browser to eyeball the system.

UI kits & slides:
- **`ui_kits/website/`** — `nxtphase.ai` marketing site recreation (`index.html` + JSX components).
- **`slides/`** — presentation template recreation (`index.html` + per-type slide JSX).

---

## 7. Quick rules of thumb (the Rams Test)

When in doubt, ask: **Is it useful? Understandable? Unobtrusive? Honest? As little design as possible?** If any answer is no — redesign.

- Warm cream canvas, near-black ink, **one** green accent.
- Editorial serif headlines, Switzer everything-else. Two weights max.
- One supporting color per section, at most.
- Generous space. Visible grid. No hype, no decoration, no emoji.
- *Braun, not Apple. Editorial, not startup.*
