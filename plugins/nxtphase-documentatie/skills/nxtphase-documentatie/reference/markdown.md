# Het Markdown-dialect van build_docx.py

`assets/build_docx.py` zet een Markdown-bestand om naar een .docx in de huisstijl.
Alleen de standaardbibliotheek van Python, dus geen pip install, geen pandoc en geen Word
nodig om te bouwen.

```bash
python assets/build_docx.py bron.md -o "Technische documentatie.docx"
```

Opties:

| Optie | Wat het doet |
|---|---|
| `-o`, `--output` | Pad van het .docx-bestand. Standaard hetzelfde pad als de bron, met `.docx`. |
| `--assets-dir` | Map waarin relatieve afbeeldingspaden gezocht worden. Standaard de map van het bronbestand. |
| `--logo` | Ander logo voor de voettekst. Standaard `assets/brand/nxt-phase-ai-logo-black.png`. |
| `--geen-logo` | Voettekst met alleen een paginanummer. |

Exitcodes: `0` alles goed, `1` het document is geschreven maar er ontbrak iets
(bijvoorbeeld een afbeelding), `2` de invoer klopt niet (ontbrekende front matter,
bronbestand niet gevonden). Controleer de exitcode altijd; bij `1` staat op stderr welke
afbeelding niet gevonden is.

## Front matter

Verplicht, en het bestand moet ermee beginnen:

```markdown
---
klant: Voorbeeld Groep
project: Analyse tool en Routing tool
document: Technische documentatie
datum: 4 augustus 2026
---
```

- `klant`, `project` en `document` zijn verplicht. Ontbreekt er een, dan stopt het script
  met exitcode 2 en schrijft het welke velden missen.
- `datum` is optioneel. Zonder datum vult het script de dag van vandaag in, in het
  Nederlands. Schrijf de datum voluit, dus `4 augustus 2026`, niet `04-08-2026`.
- `afzender` is optioneel en staat standaard op `Nxt Phase AI`.

Uit deze velden bouwt het script de voorpagina en de kop van de inhoudsopgave.
**Zet de voorpagina en de inhoudsopgave dus niet zelf in de Markdown.**

## Koppen

| Markdown | Word-stijl | In de inhoudsopgave | Nieuwe pagina |
|---|---|---|---|
| `# 1. Inleiding` | Kop 1 | ja | ja |
| `## 1.1 Wat we hebben gebouwd` | Kop 2 | ja | nee |
| `### Tech stack` | Kop 3 | nee | nee |

Nummer de koppen zelf (`1.`, `1.1`), net als in de bestaande opgeleverde documenten. Het
script nummert niet automatisch, zodat je in de tekst naar een paragraafnummer kunt
verwijzen zonder dat er iets kan verschuiven.

Vier of meer hekjes wordt behandeld als `###`.

## Alinea's en inline opmaak

Een alinea is een blok regels tot aan een lege regel. Regelafbrekingen binnen een alinea
worden samengevoegd, precies zoals in gewone Markdown.

- `**vet**`
- `*cursief*` of `_cursief_`
- `` `code` `` wordt de tekenstijl Codetekst: monospace, groen, lichte achtergrond
- `[tekst](https://url)` wordt een klikbare link in Signal Green
- `[tekst](#bookmarknaam)` verwijst naar een bookmark binnen het document

Opmaak mag genest: `**vet met een [link](https://example.com) erin**` werkt.

`<`, `>`, `&` en aanhalingstekens hoef je niet te ontsnappen, het script doet dat zelf.

## Lijsten

```markdown
- eerste punt
- tweede punt
  - subpunt op niveau 2
    - subpunt op niveau 3

1. eerste stap
2. tweede stap
3. derde stap
```

Inspringen met twee spaties per niveau, tot drie niveaus diep. Elke genummerde lijst
begint weer bij 1; dat regelt het script met een eigen nummering per lijst.

Een regel die verder inspringt zonder streepje of cijfer wordt aan het vorige punt
geplakt. Zo kun je een lang punt over meerdere regels schrijven.

## Tabellen

```markdown
| Resource | Naam | Functie |
|---|---|---|
| Web App | app-klantcontact-routing | De Routing tool |
```

- De scheidingsregel is verplicht, anders wordt het geen tabel maar een gewone alinea.
- Uitlijning per kolom met `:---` (links), `---:` (rechts) en `:---:` (gecentreerd).
  Gebruik rechts voor kolommen met bedragen of aantallen.
- De koprij krijgt de merkkleur en herhaalt automatisch bovenaan elke volgende pagina.
- De kolombreedtes rekent het script uit op basis van de langste cel per kolom, gedempt
  zodat één lange kolom niet alle ruimte opslokt. Je hoeft niets in te stellen.
- Inline opmaak werkt gewoon in cellen.
- Een lege cel laat je leeg: `| a |  | c |`.

Een tabel mag niet direct tegen de volgende tabel aan staan zonder lege regel ertussen,
anders wordt het één tabel.

## Codeblokken

````markdown
```bash
az webapp list -g rg-klantcontact -o table
```
````

Het blok krijgt een lichte achtergrond met een groene lijn links. De taalaanduiding
achter de fence wordt niet gebruikt voor kleuring, maar schrijf hem wel op: dan blijft de
Markdown-bron zelf goed leesbaar.

Breek lange commando's af met `\` aan het eind van de regel, zoals je ze ook op een
terminal zou typen. Word breekt niet zelf af binnen een codeblok, dus een te lange regel
loopt buiten de marge.

## Aandachtsblokken

```markdown
> Let op: op het moment van schrijven staan deze velden nog niet op de schermen waar
> medewerkers werken.
```

Wordt een alinea met een groene lijn ernaast. Gebruik dit spaarzaam, voor de dingen die
de lezer echt niet mag missen.

## Afbeeldingen

```markdown
![Het zijpaneel van de add-in met het conceptantwoord](screenshots/addin.png)
```

- Moet op een eigen regel staan.
- De tekst tussen de blokhaken wordt het bijschrift onder de afbeelding, in de
  bijschriftstijl. Laat hem leeg (`![](pad.png)`) als je geen bijschrift wilt.
- Ondersteund: png, jpg, jpeg, gif.
- Te brede afbeeldingen worden op de tekstbreedte geschaald, met behoud van de verhouding.
- Ontbreekt het bestand, dan komt er `[Afbeelding ontbreekt: pad]` in het document, gaat
  er een regel naar stderr en is de exitcode 1. Het document wordt dus wel geschreven,
  maar je ziet direct dat er iets mist.

Een afbeelding midden in een alinea wordt vervangen door de alt-tekst. Zet afbeeldingen
dus altijd op een eigen regel.

## Scheidingslijn

Drie of meer streepjes op een eigen regel (`---`) worden een dunne grijze lijn. Let op:
aan het begin van het bestand is `---` de front matter, niet een scheidingslijn.

## Wat er niet in zit

Bewust weggelaten, omdat het in dit soort documenten niet voorkomt en de omzetting
onvoorspelbaar zou maken: voetnoten, definitielijsten, taakvakjes, geneste tabellen,
tabellen zonder koprij, HTML-fragmenten, en automatische hoofdstuknummering. Heb je iets
daarvan nodig, schrijf het dan uit in gewone Markdown of pas het document na het bouwen
in Word aan.

## Controleren na het bouwen

Het script controleert zelf of elk XML-onderdeel van het pakket geldig is en stopt met een
foutmelding als dat niet zo is. Dat vangt een kapot document af, maar zegt niets over de
opmaak. Open het document daarna in Word en loop de controlelijst uit `huisstijl.md` na.
