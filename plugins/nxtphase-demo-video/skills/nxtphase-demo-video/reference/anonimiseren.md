# Alles wat naar de klant verwijst eruit halen

Een demo-video is een sales-asset die breed gedeeld wordt. De klant heeft ons zijn systemen
laten zien, niet zijn naam uitgeleend. Ga er standaard van uit dat er niets herkenbaars in
mag, ook als er niet expliciet om gevraagd is.

## De lijst

| Wat | Waarom het opvalt | Wat je ervoor in de plaats zet |
|---|---|---|
| Bedrijfsnaam, ook afgekort | Vanzelfsprekend | "de organisatie", een soortnaam |
| Logo, beeldmerk, huisdier | Net zo herkenbaar als de naam | Een neutraal woordmerk dat je zelf tekent |
| Themakleur | Een kleurencombinatie is een handtekening | Verschuif de basiskleur naar een andere familie |
| Productnamen van leveranciers | Verraadt de branche en de klant | "de export", "de PDF" |
| Namen van zalen, afdelingen, vestigingen | Googlebaar | Verzonnen namen |
| Namen van restaurants, menu's, arrangementen | Vaak merkgebonden | Generieke omschrijvingen |
| Mailadressen en domeinen | Vanzelfsprekend | `sales@voorbeeld.nl` |
| Persoonsnamen van medewerkers | Ook intern gevoelig | "de medewerker", of een verzonnen naam |
| Foto's van de locatie of van personeel | Direct herleidbaar | AI-gegenereerde beelden, zie onderaan |
| Data uit een echte mailbox of database | Vertrouwelijk | Volledig verzonnen |

## Waar het in de praktijk misgaat

De naam zit vaak op meer plekken dan je denkt. Zoek erop in het hele videoproject én in de
gegenereerde bestanden, en draai daarna de generatiescripts opnieuw:

```bash
grep -rn "Klantnaam\|Zaalnaam\|Productnaam" src/ scripts/ content-generiek/
```

Let op deze vier:

1. **Schermteksten uit de app.** De app zelf kan de leveranciersnaam in beeld zetten. Dan
   moet je die in de app aanpassen, niet alleen in de video, anders lopen ze uit de pas.
2. **Gegenereerde HTML.** Verander de bron én genereer opnieuw.
3. **De voice-over.** Elke tekstwijziging vraagt een nieuwe opname.
4. **Dubbelingen na een vervanging.** Vervang je een item door een woord dat al in de lijst
   staat, dan krijg je het twee keer. Schrap het item dan liever.

## Twee regels over de data zelf

**Verander ook de vórm van de verdeling, niet alleen de namen.** In een eerder project had de
eerste synthetische set nog de percentageverdeling van de echte klant en was daarmee
herleidbaar. Namen vervangen is niet genoeg.

**Kies een andere sector dan die van de opdrachtgever** en houd de tekst vrij van jargon dat
maar bij één type bedrijf past. In een eerder project werd de context een verzonnen aanbieder
van een abonnementsdienst, zonder bedrijfsnaam of logo in beeld.

Zet alle cijfers op één plek (`src/data.ts`), met de kerngetallen in één object, zodat geen
enkele scene een getal hardcodeert.

## Wat wél mag blijven

De *logica* mag echt zijn en moet dat ook zijn. Capaciteiten, beslisregels, foutmeldingen en
berekende uitkomsten laat je precies zo zien als de tool ze produceert, inclusief de
letterlijke tekst uit de broncode. De video mag geen mooiere uitkomst tonen dan het systeem
werkelijk geeft. Zet in het databestand een commentaar waarin staat welke waarden echt zijn
en waartegen ze getoetst zijn.

## Beeldmateriaal

Foto's laten we genereren; we gebruiken nooit foto's van een bestaande locatie of van
bestaande mensen. Werkwijze:

1. Bepaal uit de CSS welke beelden er nodig zijn, in welke rol en met welke uitsnede. Vraag
   niet om formaten die het beeldmodel niet kan leveren: in de praktijk zijn dat liggend
   1536x1024, staand 1024x1536 en vierkant 1024x1024.
2. Schrijf één stijlblok en daarna losse prompts. Laat alles in één chatsessie genereren met
   "same location, same photographer, same lighting and season" erbij, anders krijg je net zoveel
   verschillende locaties als beelden.
3. Neem in het stijlblok én in elke losse prompt op: geen tekst, geen bordjes, geen logo's,
   geen bestaande personen. Beeldmodellen zetten uit zichzelf graag letters op gevels en
   flessen; reken op een paar herkansingen.
4. Beelden die smal worden uitgesneden hebben een gecentreerde, rustige compositie nodig.

Leg de prompts vast in een `BEELDEN-PROMPTS.md` bij het project, zodat een reeks later aan te
vullen is in dezelfde stijl.

## Beeldtaal

Warm en redactioneel. **Nooit abstracte AI-beelden, robots of blauwe tech-close-ups.**
