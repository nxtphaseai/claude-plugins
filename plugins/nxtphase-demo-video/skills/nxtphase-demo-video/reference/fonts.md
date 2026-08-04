# Lettertypen

Twee fonts, met verschillende licentievoorwaarden. Lees dit voordat je een fontbestand in
een gedeelde repo zet.

| Font | Waarvoor | Zit in de skill? |
|---|---|---|
| Switzer | UI-teksten in het kader van de video | **Nee, mag niet** |
| PP Editorial New Italic | de tagline op de eindkaart | **Nee, zelf ophalen** |
| Inter, JetBrains Mono | vervangers, via npm | Ja, als afhankelijkheid |

## Switzer: niet meeleveren

Switzer staat op Fontshare onder de **ITF Free Font License**. Dat is te controleren bij de
bron zelf:

```bash
curl -s "https://api.fontshare.com/v2/fonts?limit=100" | grep -B4 '"slug":"switzer"'
# → "license_type":"itf_ffl"
```

Die licentie komt neer op *free to use, not free to redistribute*. Je mag het font
gebruiken in elk project, commercieel en op elke schaal, en je mag het laden via `@font-face`
of via de Fontshare-API. Wat niet mag: de fontbestanden doorgeven aan anderen, ze bundelen
in iets dat je deelt of verkoopt, of ze aangepast verspreiden.

Een skill die collega's clonen is precies dat doorgeven. **Zet de woff2-bestanden er dus
niet in.**

Twee manieren die wel kloppen:

1. **Laden via Fontshare tijdens de render.** Dat doet `assets/fonts.ts` al, met
   `delayRender` eromheen en een tijdslimiet van tien seconden. Lukt het laden niet, dan gaat
   de render gewoon door en valt de tekst terug op Inter: een mislukte render is erger dan
   een ander font. Dit is de standaard en vereist geen actie.
2. **Zelf downloaden per project.** Werk je zonder internet of achter een strikte proxy, haal
   Switzer dan zelf op bij [fontshare.com](https://www.fontshare.com/fonts/switzer), zet de
   bestanden in `public/fonts/` van dát project en laad ze met een eigen `@font-face`. Commit
   ze niet naar een repo die je breed deelt.

Merk op dat de eindkaart hier niet van afhangt: die gebruikt PP Editorial New.

## PP Editorial New: zelf ophalen

De eindkaart kan er niet zonder, maar het bestand zit **niet** in deze repo: die is openbaar,
en PP Editorial New komt van Pangram Pangram, dat naast een gratis variant voor persoonlijk
gebruik een betaalde commerciële licentie kent. Een licentiebestand in een publieke repo
zetten is herdistributie.

Haal `PPEditorialNew-Italic.otf` dus intern op en zet het in `public/fonts/` van je project.
Commit het niet naar een publieke repo.

**De Tight-variant is geen vervanger.** De `nxtphase-design`-plugin levert
`PPEditorialNewPPTTight-Italic.otf` mee. Die heeft andere letterbreedtes, terwijl
`TAGLINE_EM_WIDTH` in `Outro.tsx` uit de gewone Italic is gerekend. Gebruik je de Tight, dan
klopt de breedteverhouding tussen woordmerk en tagline niet meer.

Zonder het bestand valt de tagline stil terug op Georgia en slaagt de render gewoon.
Controleer de eindkaart daarom altijd met een still.

## Inter en JetBrains Mono

Die komen via `@remotion/google-fonts` uit npm en worden mee gebundeld door de bundler. Geen
netwerk tijdens de render, geen licentiekwestie: beide staan onder de SIL Open Font License.

## Een export die je niet aanroept, bestaat niet

Laadt een font via een `export const` die nergens gebruikt wordt, dan gooit de bundler hem
weg en valt de tekst stil terug op een systeemfont. De render slaagt gewoon, dus je ziet het
alleen als je erop let. Roep de loader daarom expliciet aan vanuit `Root.tsx`, zoals
`loadSwitzer()` en `loadEditorial()` daar staan.
