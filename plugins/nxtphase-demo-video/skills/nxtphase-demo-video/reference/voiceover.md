# Voice-over

## Toon

Uitleggend en concreet, alsof je het aan een collega vertelt. Begin bij de situatie van de
kijker, niet bij onszelf. Maak elke abstractie meteen waar met een voorbeeld. Korte vragen
mogen ("Maar waar begin je?"). Geen zinnen die alleen maar een overgang zijn.

**Vermijd het ritme van reclametekst.** Drie parallelle zinsdelen achter elkaar
("Altijd volledig, altijd dezelfde kwaliteit, ook als het druk is") klinkt als AI-tekst, hoe
waar het ook is. Eén gewone zin die hetzelfde zegt is beter: "Ook op een drukke dag ziet elke
offerte er zo uit." Als je een drieslag opschrijft, herschrijf hem.

Verder:

- Schrijf getallen voluit: "drie weken", niet "3 weken". Het stemmodel leest dat betrouwbaarder.
- Noem NxtPhase één keer, bij de introductie van de tool.
- Geen verzonnen cijfers of percentages.
- Reken op ongeveer 2,4 woorden per seconde als startpunt, en meet daarna.

**Benoem expliciet wat je niet automatiseert.** Dat wekt meer vertrouwen dan welke belofte
ook, en het is het enige moment waarop je over de grenzen van de tool praat.

**Zinnen die een werkwijze beschrijven werken beter dan zinnen die een resultaat beloven.**
Woorden als "grip", "proces" en "werkwijze" doen het werk. Bij "moeiteloos" botst de toon
met de rest.

## Regie-aanwijzingen

Tussen vierkante haakjes: `[calm]` zet de toon aan het begin van een scene, `[pause]` zet een
stilte. Ze worden niet uitgesproken en alleen `eleven_v3` volgt ze op; het generatiescript
weigert een ander model zolang ze in de tekst staan.

Spaarzaam gebruiken: één aanwijzing per zin maakt het juist onrustig. En zet geen `[pause]`
tussen een hoofdzin en een korte bijzin die erbij hoort, dan valt er een gat.

## De pijplijn

`assets/scripts/generate-voiceover.mts` genereert de hele voice-over als **één doorlopende
opname** en knipt die daarna op in één mp3 per scene. Dat is bewust: elke API-call is een
eigen performance, dus losse calls geven net iets verschillende stemmen. De knippunten
worden niet geraden, maar afgeleid uit de tijdstempels per teken die de API teruggeeft.

```bash
npm run voiceover                    # genereren en knippen
npm run voiceover -- --recut         # alleen opnieuw knippen, kost niets
npm run voiceover -- --dry-run       # alleen laten zien wat er zou gebeuren
```

| | |
|---|---|
| Stem | `ARIOBKJtltx2F7r1TMzI` (staat als standaard in het script) |
| Model | `eleven_v3` |
| Sleutel | `ELEVENLABS_API_KEY` in de `.env` van de repo |
| Stilte na elke zin | `TAIL_S` in `timeline.ts`, 0,45 s |
| Tempo | `--tempo`, bij het knippen. 1,04 tot 1,08 werkt prettig |

**Tempo hoort bij het knippen, niet bij het genereren.** `--recut --tempo=1.04` past de
snelheid aan met `atempo` zonder nieuwe API-kosten. Bewaar daarom altijd de onbewerkte
opname én de tijdstempels.

## Cues: het beeld aan de stem hangen

Wil je dat iets in beeld precies gebeurt op het moment dat de stem het noemt, geef de
scene dan `cues` mee: een lijst zinsdelen waarvan het beeld het inzetmoment moet weten.
Het generatiescript zoekt ze op in de karakter-tijdstempels en schrijft de seconden naar
`src/voiceover-cues.ts`. De animatie hangt dan aan de werkelijke opname in plaats van aan
een geschat frame.

Faal hard als een zinsdeel niet of meer dan eens voorkomt. Anders schuift het beeld stil
weg van de stem en merk je het pas in de eindrender.

## Scenelengtes

De tekst staat in `src/voiceover.ts`, één bron voor de audio en voor de documentatie. Elke
scene heeft in `timeline.ts` een `minScreen`: de lengte die de animatie zelf nodig heeft. Na
het genereren drukt het script een voorstel af waarin per scene staat of de animatie of de
stem de lengte bepaalt. Neem dat over.

**Bij de meeste scenes is de animatie de rem, niet de stem.** In een project van acht scenes
gold dat voor zeven ervan. Wie alleen op spreektijd stuurt, kapt scrolls en klikken
halverwege af. Daarom bestaat `minScreen`.

**Elke nieuwe generatie leest net iets anders,** ook bij dezelfde stem en dezelfde tekst. Dus
na elke tekstwijziging: opnieuw genereren, lengtes overnemen, opnieuw renderen. Wordt een
scene langer omdat de stem het vraagt, controleer dan of daar geen dood moment ontstaat.

De gezonde situatie is dat het beeld leidt en de stem erin past. Moet je een scene fors
oprekken voor een zin, kort dan de zin in.

## Tekst op het scherm

Met een voice-over staan de schermteksten uit: stem en tekst tegelijk leest dubbel. Houd ze
wel in de code staan achter een schakelaar, met de timing intact. Dan kun je later een
versie zonder geluid maken voor social media zonder de scenes te herbouwen.

Zonder schermteksten mag het appvenster verticaal gecentreerd; met schermteksten schuift het
omhoog om ruimte te maken.
