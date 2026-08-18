# Huisstijl van de opgeleverde documenten

Dit bestand legt vast hoe de twee .docx-bestanden eruitzien die je oplevert. Gebruik het
om het resultaat te controleren, en om `assets/build_docx.py` aan te passen zonder de
huisstijl te breken.

Je zet zelf **geen** opmaak in de Markdown. De builder maakt de voorpagina, de
inhoudsopgave, de kleuren, de lettertypes en de voettekst. Jij levert alleen inhoud plus
de front matter. Ga je toch iets aan de opmaak veranderen, verander het dan in
`build_docx.py` op één plek (de stijldefinitie), nooit per alinea.

## Kleuren

| Kleur | Hex | Waar hij staat |
|---|---|---|
| Signal Green | `#3E9B5D` | Hoofdstukkoppen (Kop 1), vulling van tabelkoprijen, links, en het documenttype op de voorpagina |
| Off-black | `#090909` | Alle gewone tekst, koppen niveau 2 en 3, de projectnaam op de voorpagina |
| Stone | `#9B9590` | Bijschriften onder afbeeldingen |
| Cream | `#F5F0E8` en `#FAF6F2` | Tekst op een groene ondergrond (de tekst in de tabelkoprij is `#FAF6F2`) |
| Lichtgrijs | `#D9D9D9` | Alle tabelranden |
| Diep groen | `#2A6B3F` | Alleen de letters van `code` in de lopende tekst |

Cream doet twee dingen: het is de tekstkleur op een groene ondergrond en de achtergrond
van codeblokken en van `code` in de lopende tekst (`#F5F0E8`).

Voeg geen zevende kleur toe. Wil je iets benadrukken, gebruik dan vet, niet een kleur.

## Lettertypes

Twee merkfonts, plus een monospace font voor code:

- **PP Editorial New**: de voorpagina en de hoofdstukkoppen (Kop 1).
- **Switzer Medium**: al het andere. Body, koppen niveau 2 en 3, tabellen, lijsten,
  bijschriften, voettekst.
- **Consolas**: alleen codeblokken en `code` in de lopende tekst. Geen merkfont maar een
  systeemfont, zodat een `az`-commando ook op een werkplek zonder de merkfonts in
  monospace blijft staan.

**De fonts worden niet in het document ingesloten en zitten niet in deze publieke repo.**
Op een machine zonder die fonts vervangt Word ze door iets anders. Dat is geaccepteerd:
dat geldt namelijk ook voor de bestaande opgeleverde documenten. De structuur, kleuren,
tabellen en inhoudsopgave blijven wel gewoon kloppen.

Moet het document er per se exact uitzien, bijvoorbeeld omdat de klant er een pdf van
wil hebben, open het dan op een werkplek waar de merkfonts geïnstalleerd zijn en
exporteer daarvandaan naar pdf. Meld dit aan de gebruiker als hij om een pdf vraagt.

## Pagina

- A4 staand, 11906 x 16838 twips.
- Marges 1417 twips (2,5 cm) rondom.

## De voorpagina

De builder bouwt de voorpagina uit de front matter (`klant`, `project`, `document`,
`datum`). Zet hem dus nooit zelf in de Markdown. Alles staat linksuitgelijnd bovenaan
pagina 1, in deze volgorde:

1. `<Klantnaam>`, PP Editorial New, 14 pt
2. lege regel
3. `<Projectnaam>` (PP Editorial New bold, 18 pt, `#090909`) + ` | ` + `<Documenttype>`
   (PP Editorial New, 18 pt, `#3E9B5D`)
4. lege regel
5. `Opgeleverd door Nxt Phase AI | <datum voluit in het Nederlands>`, Switzer Medium, 12 pt

Zo ziet dat er in de echte oplevering uit:

```
Voorbeeld Groep

Analyse tool en Routing tool | Technische documentatie

Opgeleverd door Nxt Phase AI | 4 augustus 2026
```

Regels:

- Schrijf de afzender altijd als `Nxt Phase AI`, met spaties. Een oudere oplevering zegt
  `NxtPhase AI`. Dat is de oude schrijfwijze, neem hem niet over.
- De datum voluit in het Nederlands: `4 augustus 2026`, niet `04-08-2026`.
- Het documenttype is `Gebruikershandleiding` of `Technische documentatie`. Heet het
  document anders, bijvoorbeeld `Opleverrapport en functionele beschrijving`, vraag dat
  dan expliciet aan de gebruiker en neem het letterlijk over.
- Geen logo op de voorpagina. Het logo staat alleen in de voettekst.

## Inhoudsopgave

Na de voorpagina volgt het kopje `Inhoudsopgave` (PP Editorial New bold, `#3E9B5D`) en
daarna de inhoudsopgave zelf. Eigenschappen:

- **Zonder paginanummers.**
- **Klikbaar**: elke regel is een verwijzing naar de bijbehorende kop.
- **Tot en met niveau 2**: hoofdstukken (`#`) en paragrafen (`##`). Tussenkopjes (`###`)
  staan er niet in.
- **Hoofdstuk 1 begint op een nieuwe pagina.** Elke Kop 1 daarna ook.

Zo zag de inhoudsopgave van de technische documentatie in de ene oplevering eruit:

```
1. Inleiding
1.1 Wat we hebben gebouwd
1.2 Technisch overzicht
1.3 Ingebouwde begrenzingen van de routing
1.4 Automatiseringen
2. De Azure-omgeving
2.1 Resource-overzicht
...
```

De nummering staat in de koptekst zelf, niet in een Word-lijstnummering. Schrijf dus
`# 1. Inleiding` en `## 1.1 Wat we hebben gebouwd` in de Markdown, en houd de nummering
zelf bij.

## Koppen

| Niveau | Markdown | Font | Opmaak | In de inhoudsopgave |
|---|---|---|---|---|
| Kop 1 (hoofdstuk) | `#` | PP Editorial New | bold, `#3E9B5D`, 17 pt, begint op een nieuwe pagina | ja |
| Kop 2 (paragraaf) | `##` | Switzer Medium | bold, `#090909`, 12 pt | ja |
| Kop 3 (tussenkopje) | `###` | Switzer Medium | bold, `#090909`, 10,5 pt | nee |

De koppen zijn iets groter dan in de opgeleverde documenten van 2026, waar Kop 1 en Kop 2
allebei op de body-grootte stonden. De hiërarchie was daar alleen aan kleur en vet te zien.
Wil je precies dezelfde maten als toen, zet dan in `build_docx.py` de `w:sz` van `Kop1` op
24 en die van `Kop2` op 21. Verder verandert er niets.

Kop 1 is altijd genummerd (`1. Inleiding`), Kop 2 ook (`2.3 App settings`). Kop 3 is niet
genummerd en is een gewoon tussenkopje, bijvoorbeeld `Tech stack` of `Wat je beter niet
doet`. Ga niet dieper dan Kop 3. Heb je een vierde niveau nodig, dan is de indeling van
het hoofdstuk verkeerd.

## Body, lijsten, bijschriften en code

- **Standaard**: Switzer Medium, 10,5 pt (`w:sz` 21), `#090909`. Dit is de stijl voor
  elke gewone alinea.
- **Lijstalinea**: bullets en genummerde lijsten. Zelfde font en grootte als Standaard.
- **Bijschrift**: de regel onder een afbeelding, in stone `#9B9590`. De builder maakt die
  uit de alt-tekst van `![Bijschrift](pad.png)`.
- **Codeblok**: gefencede codeblokken, bijvoorbeeld de `az`-commando's in de technische
  documentatie. De builder zet de opmaak; verzin er geen eigen kleur of kader bij.
- **Aandachtsblok**: een blok dat in de Markdown met `>` begint, bijvoorbeeld een
  "Let op:"-regel. De builder zet er een groene streep links naast. Ook hier geen eigen
  kader, kleur of vet omheen.

## Tabellen

Tabellen dragen veel van de inhoud, zeker in de technische documentatie
(resource-overzicht, app settings, secrets-overzicht) en in de gebruikershandleiding
(uitleg van metrics, queues, velden). De opmaak:

- Randen: `#D9D9D9`, rondom en tussen alle cellen.
- Koprij: vulling `#3E9B5D`, tekst `#FAF6F2`, bold, verticaal gecentreerd.
- Overige cellen: Switzer Medium 10,5 pt, `#090909`.
- Uitlijning volgt de kolom: standaard links, en rechts als je in de scheidingsregel van
  de Markdown-tabel `---:` zet. De koprij volgt dezelfde uitlijning als de kolom, zodat een
  kolom met bedragen ook een rechts uitgelijnde kop krijgt.
- **De koprij herhaalt op elke pagina.** Dit is niet optioneel. Lange tabellen zoals de
  bijlage met de categorie-indeling uit de ene oplevering
  (`| Subcategorie | Vraag | Omschrijving |`, tientallen rijen) lopen over meerdere
  pagina's door, en zonder herhalende koprij is de tweede pagina onleesbaar.

Houd het aantal kolommen laag. De echte documenten gebruiken twee tot vijf kolommen,
bijvoorbeeld `| Resource | Naam | Configuratie | Functie |` en
`| Metric | Wat het meet en hoe het wordt berekend | Goed om te weten |`. Meer kolommen
past niet binnen de marges van een A4.

## Voettekst

Op elke pagina, in de voettekst:

- Links: het paginanummer.
- Rechts: het zwarte "nxt phase ai"-logo
  (`assets/brand/nxt-phase-ai-logo-black.png`).

Geen klantlogo, geen datum, geen bestandsnaam in de voettekst.

## Alles loopt via Word-stijlen

Dit is de belangrijkste regel van dit bestand. Alle uiterlijke opmaak zit in benoemde
Word-stijlen, niet in de alinea's zelf:

`Kop 1`, `Kop 2`, `Kop 3`, `Standaard`, `Lijstalinea`, `Bijschrift`, `Codeblok`,
`Aandachtsblok`, `Voettekst`, plus de tabelstijl `Nxt Phase tabel` en de tekenstijlen
`Hyperlink` en `Codetekst`.

Dit is niet cosmetisch. De klant krijgt een bewerkbaar document en gaat het aanpassen. Zet
je de kleur of grootte rechtstreeks op de alinea, dan moet hij elke kop apart aanpassen en
gaat het document na de eerste bewerkronde door elkaar lopen. Via stijlen past hij `Kop 1`
één keer aan en verandert het hele document mee.

Wat de builder wel direct zet, omdat het geen uiterlijk is maar structuur: vet en cursief
in de lopende tekst, de lijstnummering en de inspringing per lijstniveau, de kolombreedtes
en de uitlijning per tabelkolom, en de twee kleuren van de titelregel op de voorpagina.
Verder niets. Kleur, grootte en lettertype komen altijd uit een stijl.

Let op bij het aanpassen van `build_docx.py`: de stijl `Standaard` zet bewust géén kleur en
géén uitlijning. Een alineastijl wint in Word van een tabelstijl, dus zodra `Standaard` een
kleur krijgt, wordt de tekst in de groene tabelkoprij weer zwart. De body-kleur staat
daarom in `docDefaults`.

Bij het aanpassen van `build_docx.py`: verander de stijldefinitie, niet de plek waar de
alinea wordt weggeschreven. Ziet een deel van het document er anders uit dan de rest, dan
is er ergens directe opmaak toegepast. Haal die weg.

## Het resultaat controleren

Doe dit na elke build, voordat je het document oplevert. Loop deze vier punten af in Word.

Kun je zelf geen Word openen, doe dan de controle op het bestand zelf. Een .docx is een
zipbestand: `word/document.xml`, `word/styles.xml` en `word/footer1.xml` zijn gewoon uit te
pakken en te lezen. Daar staat of de voorpaginaregels er zijn, of de inhoudsopgave
verwijzingen naar bookmarks bevat en geen paginanummers, of `tblHeader` op elke koprij
staat, en of de voettekst het paginanummerveld en het logo heeft. Wat je alleen visueel
kunt beoordelen, leg je aan de gebruiker voor met de vraag wat hij ziet. Schrijf nooit op
dat je het document in Word hebt bekeken als je dat niet hebt gedaan.

1. **Voorpagina.** Staan klantnaam, projectnaam, documenttype en datum er, in die
   volgorde, en is het documenttype groen? Staat er `Opgeleverd door Nxt Phase AI` met
   de datum voluit in het Nederlands?
2. **Inhoudsopgave.** Klik een regel aan. Springt hij naar de juiste kop? Staan er geen
   paginanummers, en staan tussenkopjes (`###`) er terecht niet in? Begint hoofdstuk 1 op
   een nieuwe pagina?
3. **Tabellen.** Zoek een tabel die over de paginagrens heen loopt en controleer of de
   groene koprij bovenaan de tweede pagina herhaalt.
4. **Voettekst.** Staat het paginanummer links en het zwarte logo rechts, op elke pagina?

Klopt een van de vier niet, los het op in `build_docx.py` en bouw opnieuw. Repareer het
nooit met de hand in Word: de volgende build gooit die correctie weg.
