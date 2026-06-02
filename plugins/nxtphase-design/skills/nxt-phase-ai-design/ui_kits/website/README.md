# Website UI Kit — nxtphase.ai

A high-fidelity recreation of the **Nxt Phase AI marketing site**, built from the brand guidelines and the presentation template's website/applications section. Dieter Rams / Braun aesthetic: warm cream canvas, near-black ink, one Signal Green accent, editorial serif headlines.

## Run
Open `index.html`. React + Babel (in-browser). Pulls tokens from `../../colors_and_type.css` and assets from `../../assets/`.

## Interactive flow
- **Nav** — sticky, links smooth-scroll to sections; "Start a conversation" jumps to the contact band and opens the form.
- **Contact** (CTA band) — "Plan a call" / "Send a message" reveals a contact form; submitting shows a confirmation state.

## Components
| File | Component | Notes |
|---|---|---|
| `Nav.jsx` | `Nav` | Sticky header, logo (Off Black), nav links, primary CTA |
| `Hero.jsx` | `Hero` | Headline + lead + dual CTA + editorial workspace image |
| `Content.jsx` | `Pillars` | Four pillars (Educate · Prioritise · Build · Run) with dot-icon tiles |
| | `Values` | 2×2 "why Nxt Phase" grid |
| | `Proof` | Client wordmarks (grayscale) + 3-up stats with italic-orange numerals |
| | `Cases` | Case-study cards (MCB, NHA) with photo + overline tag |
| `CTA.jsx` | `CTA` | Dark closing band with stateful inline contact form |
| `Footer.jsx` | `Footer` | Cream logo on off-black, meta line |

## Conventions
- Headlines: PP Editorial New (weight 400). Everything else: Switzer.
- Section structure: overline + serif `h2` + stone supporting line, then a hairline-bordered grid.
- One accent (green) for live/active; orange reserved for numerals/callouts.
- Buttons: `.btn-dark` (primary), `.btn-green`, `.btn-ghost`, `.btn-link`. Soft radius, never pills.
- All section styling in `site.css`; design tokens come from the root CSS.

## Not included / disclaimers
- Client wordmarks are **placeholder text marks** — replace with real grayscale client logos (the brand calls for grayscale for cohesion).
- Copy is in **English** here to match the website example in the guidelines; the brand is bilingual and client-facing decks are frequently in Dutch.
- No CMS/blog, pricing, or legal pages — only the surfaces evidenced in the brand materials.
