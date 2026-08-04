---
name: nxtphase-demo-video
description: Maak een demo- of sales-video van een NxtPhase-project met Remotion. Gebruik deze skill bij elk verzoek om een demovideo, salesvideo, productvideo of screencast van een tool die we hebben gebouwd, en bij het aanpassen van een bestaande demo-video. Bevat de huisstijl, de vaste eindkaart, de voice-overpijplijn met ElevenLabs en de werkwijze om interfaces exact te tonen in plaats van na te tekenen.
metadata:
  tags: remotion, video, demo, sales, voice-over, elevenlabs, nxtphase
---

# Demo-video's van NxtPhase

Onze demo-video's laten een tool zien die we echt gebouwd hebben, aan iemand die het
probleem herkent. Ze zijn kort, rustig en concreet. Geen reclame, geen stockbeelden,
geen nagetekende schermen.

Voor generieke Remotion-vragen (API's, transitions, fonts): gebruik de `remotion`-skill.
Deze skill gaat over *hoe wij het doen*.

---

## De twee harde regels

**1. De interface wordt getoond, niet nagetekend.** Als een scherm van ons is, komt de
CSS en de markup letterlijk uit de broncode. Verandert de app, dan verandert de video
mee. Hoe: zie `reference/exactheid.md`. Dit is het verschil tussen een video die
vertrouwen wekt en een animatie die er ongeveer uitziet.

**2. Er staat niets in wat naar de klant of naar echte mensen te herleiden is.** Geen
bedrijfsnaam, geen afkorting daarvan, geen logo of beeldmerk, geen productnamen van
leveranciers, geen echte zaal-, afdelings- of menunamen, geen echte klantdata, geen
foto's van bestaande locaties of personen. Ook de themakleur verschuiven, want een
huisstijl is net zo herkenbaar als een naam. Zie `reference/anonimiseren.md`.

---

## Werkwijze

### Stap 1: eerst de storyline, dan pas scenes

Bouw nooit meteen. **Vraag eerst deze vier dingen**, want ze bepalen al het werk erna:

1. Doelgroep: nieuwe prospects, intern draagvlak, of oplevering aan de klant?
2. Lengte en verhouding (standaard: 1920x1080, 30 fps, 80 tot 120 seconden)
3. Draagt de stem de tekst, of tekst op het scherm?
4. Mag de klant genoemd worden? Standaard is nee, zie `reference/anonimiseren.md`.

Lever daarna een beat sheet: per scene de tijd, wat je ziet, wat de boodschap is en een
woordbudget. Laat die goedkeuren voor je scenes bouwt.

Een goede boog: probleem, slimheid, snelheid, resultaat, vertrouwen. Zet de mooiste shot
achteraan. Geef de kernscene ruim de meeste tijd; de rest is aanloop.

### Stap 2: scaffolden

```bash
npx create-video@latest --yes --blank --no-tailwind video/<naam>
```

Neem daarna uit `assets/` over, met deze bestemmingen:

| Uit `assets/` | Naar |
|---|---|
| `theme.ts`, `anim.ts`, `timeline.ts`, `fonts.ts` | `src/` |
| `Frame.tsx`, `Cursor.tsx`, `Logo.tsx`, `Outro.tsx` | `src/components/` |
| `scripts/*` | `scripts/` |
| `remotion.config.ts` | projectroot |

**Het lettertype van de eindkaart zit niet in deze repo.** Deze repo is openbaar en
PP Editorial New mag niet zomaar herverspreid worden. Haal `PPEditorialNew-Italic.otf`
intern op en zet het in **`public/fonts/`** van je project.

Dat pad is geen keuze: `fonts.ts` laadt het bestand via
`staticFile("fonts/PPEditorialNew-Italic.otf")`. Ontbreekt het, dan valt de tagline op de
eindkaart stil terug op Georgia en klopt de kaart niet meer. De render slaagt gewoon, dus
controleer het met een still. Let op: de *Tight*-variant uit de `nxtphase-design`-plugin is
geen vervanger, die heeft andere letterbreedtes en dan klopt de verhouding tussen logo en
tagline niet meer.

`timeline.ts` bevat een sjabloon met vier scenes; die vervang je door de scenes van dit
project.

Pin alle Remotion-pakketten op exact dezelfde versie, ook `@remotion/transitions` en
`@remotion/google-fonts`; een `^` levert een versiemismatch en een onduidelijke bundelfout
op.

### Stap 3: scenes bouwen

Per scene een bestand in `src/scenes/`. Timing in frames, altijd afgeleid van
`useCurrentFrame()`. Zet CSS-transitions en keyframe-animaties uit voor alles wat uit een
app komt (zie `reference/exactheid.md`): die lopen op wandkloktijd en gaan haperen.

### Stap 4: voice-over

Schrijf de tekst in `src/voiceover.ts`, genereer met `npm run voiceover`, neem de
voorgestelde scenelengtes over. Zie `reference/voiceover.md`.

### Stap 5: nakijken

Loop `reference/checklist.md` af voor je oplevert. Die lijst is opgebouwd uit echte
feedback en vangt precies de dingen die anders alsnog terugkomen.

---

## Huisstijl

| | |
|---|---|
| Formaat | 1920x1080, 30 fps |
| Achtergrond | Cream `#F5F0E8` |
| Tekst | Off-black `#090909`, zachter `#6E6862` |
| Accent | Signal Green `#3E9B5D` |
| Font kader | Switzer, tijdens de render geladen bij Fontshare; Inter als terugval |
| Font eindkaart | PP Editorial New Italic, lokaal in `public/fonts/` |
| Overgang | `fade()` van 12 frames; harde cut bij een wissel van tool |

De volledige waarden staan in `assets/theme.ts`.

**Switzer zit bewust niet in deze skill.** Het staat onder een licentie die gebruiken wel
toestaat maar doorgeven niet, dus meeleveren mag niet. Het wordt tijdens de render bij
Fontshare geladen en valt zonder internet terug op Inter. Zie `reference/fonts.md`; daar
staat ook een waarschuwing over het font van de eindkaart.

**Vensters.** Een app staat in een venster met afgeronde hoeken en een zachte schaduw,
gecentreerd op het cream vlak. Een browserapp krijgt een adresbalkje, een add-in of
desktopapp niet. Render op de logische maten van de app zelf en schaal het geheel; zo
kloppen alle marges en fontgroottes. Zie `assets/Frame.tsx`.

Kies die logische maat bewust net boven een breakpoint van de app, zodat de brede
desktop-indeling geldt. Gebruikte combinaties: 1440x700 op schaal 1,2, en 1440x940 op
schaal 1,0.

**Muisaanwijzer.** Alleen tonen waar de kijker een klik moet zien. Zie `assets/Cursor.tsx`.

---

## De eindkaart

**Elke demo-video eindigt met dezelfde kaart.** Neem `assets/Outro.tsx` en `assets/Logo.tsx`
ongewijzigd over, inclusief het lettertypebestand. De meshgradient, het woordmerk, de
tagline "We make AI Work" met Work in Signal Green, en de maatverhoudingen tussen logo en
tagline liggen vast en zijn uit het logobestand gerekend, niet geschat. Verzin hier niets
nieuws.

Twee dingen die je per video afstemt:

- **Wanneer het logo opkomt.** Standaard rond frame 60, zodat de laatste gesproken zin
  bijna klaar is. Komt het logo te vroeg, dan praat de stem er te lang overheen.
- **De lengte van de kaart.** Volgt uit de slotzin, minimaal ongeveer 8 seconden.

**Over de woorden boven het logo.** In één video stonden daar drie woorden die op cue
oplichtten terwijl de stem ze noemde, en die de pijlers van dát traject benoemden. In een
andere zijn ze weggelaten en dat oogde rustiger. Behandel ze dus als projectspecifiek en
optioneel, niet als deel van de vaste kaart. Gebruik je ze wel, laat ze dan vanaf het begin gedempt staan (`opacity 0.16`)
en op cue oplichten, anders verspringt de compositie.

---

## Wat de video vertelt

Begin bij de situatie van de kijker, niet bij onszelf. Noem NxtPhase één keer, op het
moment dat de tool geïntroduceerd wordt, en verder niet. Eindig met wat het oplevert.

**Verzin nooit cijfers.** Geen percentages, geen bespaarde uren, geen "70% sneller". Wil
de klant een getal, dan moet dat van de klant komen. Eén echt cijfer is meer waard dan
drie mooie.

**Toon ook wat er misgaat.** Een scene waarin het systeem iets afkeurt of signaleert
overtuigt meer dan drie scenes waarin alles goed gaat: het laat zien dat er logica onder
zit en niet alleen tekstgeneratie.

**Laat het gevolg van een handeling zien.** Wie op een knop drukt, wil het resultaat zien
in de omringende applicatie. Een concept invoegen betekent: het concept verschijnt in de
mailclient, en daarna gaat het de deur uit.

---

## Referentie

- `reference/valkuilen.md` — fouten die echt gemaakt zijn: trillende scrolls, de punt van
  de muisaanwijzer, transparante kaarten, verspringende composities
- `reference/exactheid.md` — interfaces exact tonen: CSS extraheren, markup porten, de
  echte renderer aanroepen
- `reference/anonimiseren.md` — alles wat naar de klant verwijst eruit halen
- `reference/voiceover.md` — toon, ElevenLabs-pijplijn, stem, scenelengtes
- `reference/fonts.md` — welk font waarvandaan komt, en wat je wel en niet mag meeleveren
- `reference/checklist.md` — nakijklijst voor oplevering
- `assets/` — kant-en-klare bestanden, inclusief de eindkaart
