# Interfaces exact tonen

Het verschil tussen een demo die vertrouwen wekt en een animatie die er ongeveer uitziet.
Er zijn drie routes, in volgorde van voorkeur.

## Route 1: de CSS uit de bron trekken

Voor een app met een eigen stylesheet of een `<style>`-blok. `assets/scripts/extract-styles.mjs`
leest die letterlijk uit de bron en schrijft hem gescopet naar `src/styles/`.

```js
const SOURCES = [
  { kind: "html", file: join(REPO, "app", "taskpane.html"), scope: "app-addin", out: "addin.css" },
  { kind: "css",  file: join(REPO, "app", "css", "quote.css"), scope: "app-quote", out: "quote.css" },
];
```

Waarom scopen: meerdere apps in één document delen `:root`-variabelen en klassenamen. Elke
selector krijgt er een scope-klasse voor, de regels zelf blijven ongewijzigd. Het script
controleert achteraf of elke regel gescopet is en faalt als er één doorheen glipt.

Draai het opnieuw zodra de app verandert. Zet dat in `package.json` als `npm run styles`.

**Let op deze drie dingen:**

- `url()`-verwijzingen in de CSS worden door de bundler tijdens het bouwen opgelost, vanaf
  de map van de stylesheet. Herschrijf ze naar een relatief pad naar `public/`, niet naar
  een absoluut pad: dat bestaat op schijf niet en de bundel faalt.
- Regels die aan `body` hangen komen op je scope-element terecht. Krijgt de wrapper twee
  klassen (`.app-quote.quote`), dan moet je dat in je JSX ook zo zetten.
- Fonts die de app via een `<link>` laadt zitten niet in de CSS. Laad ze apart, anders valt
  de tekst terug op een systeem-serif en klopt de typografie niet meer. Roep de loader
  expliciet aan vanuit `Root.tsx`; een ongebruikte export wordt weggeoptimaliseerd.

## Route 2: de markup porten

Voor de interactieve delen. Neem de DOM-structuur, klassenamen en volgorde letterlijk over
in een React-component, met een verwijzing in commentaar naar de functie in de bron die je
port. Losse bouwstenen die snel uit de pas lopen (iconen, labelmappen, statuslijsten) haal
je met een script uit de bron, zoals `extract-addin-parts.mjs` doet: dan blijft er één bron
van waarheid.

De video mag alleen *timing* toevoegen. In de echte app verschijnt alles tegelijk; in de
video mogen onderdelen na elkaar opkomen zodat de kijker ze kan volgen. De elementen zelf
blijven identiek.

## Route 3: de echte renderer aanroepen

Het mooiste, als de app zijn HTML in JavaScript opbouwt. Controleer of die code vrij is van
`document` en `window`; is dat zo, dan kun je hem in een Node-script in een sandbox laden en
de renderfunctie aanroepen. De uitvoer schrijf je als string naar `src/generated/`.

```bash
grep -c "document\.\|window\." app/js/render.js   # 0 = geschikt
```

Zo is het documentgedeelte van een van onze video's gemaakt: geen nabouw, maar de echte uitvoer van
`renderOfferte()`, met alleen de foto's en de namen vervangen.

Twee valkuilen: een `const` op topniveau in een sandbox komt niet op het global object, dus
die kun je niet via `globalThis` aanpassen (doe dat dan op de gegenereerde HTML). En de
hoogte van gegenereerde inhoud moet je meten in plaats van gokken: gebruik `delayRender()`,
wacht tot de afbeeldingen geladen zijn, meet `scrollHeight` en geef de render dan vrij.

## Wat je wél mag natekenen

Interfaces van derden: Outlook, een browser, een besturingssysteem. Bouw die na op de
verhoudingen van een screenshot, maar **neem geen enkel gegeven uit dat screenshot over**.
Geen namen, geen onderwerpen, geen mapnamen, geen tellers. Alles verzinnen.

## Animaties uitzetten

Overgenomen CSS bevat vaak `transition` en `@keyframes`. Remotion rendert frame voor frame
terwijl die op wandkloktijd lopen, dus het beeld gaat haperen. Zet ze uit in `index.css`:

```css
.app-addin *, .app-addin *::before, .app-addin *::after { transition: none !important; animation: none !important; }
```

Moet er toch iets draaien, zoals een laadspinner, dan stuur je dat met een transform uit
`useCurrentFrame()`.
