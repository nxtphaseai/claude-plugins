# De demopagina in de Demo Library

Na de video komt de pagina. De **NXT Phase AI - Demo Library** in Notion is een lijst met
demopagina's per afdeling; elke pagina is los deelbaar met een klant, die dan alleen die
pagina ziet en niet het overzicht.

Deze stap is optioneel en staat los van de video. Je kunt hem ook draaien voor een demo
die al bestaat en waarvan de opname ergens anders vandaan komt.

Bovenliggende pagina: `https://app.notion.com/p/365e4696d12d81aba638c718a777d73f`

---

## Nooit een bestaande demopagina verwijderen of overschrijven

Dit is de enige harde regel in dit document. Bestaande pagina's in de Demo Library zijn
klantmateriaal: ze zijn los gedeeld met prospects, dus er lopen links naar buiten die je
niet ziet. Een pagina die weg is of leeggemaakt, is voor die prospect een dode link.

- Verwijder nooit een pagina in de Demo Library, ook niet als hij verouderd, dubbel of
  verkeerd lijkt. Meld het en laat de keuze aan de mens.
- Draai `replace_content` uitsluitend op het duplicaat dat je zelf net hebt gemaakt, nooit
  op de bronpagina of op een andere bestaande pagina.
- Controleer vóór elke schrijfactie dat de `page_id` die van het verse duplicaat is en niet
  die van de bron. Die twee liggen in het gesprek vlak bij elkaar, en dat is precies hoe
  het misgaat.
- Ging het toch mis, zeg het dan meteen. Notion heeft versiegeschiedenis en een prullenbak,
  dus snel gemeld is te herstellen; stilzwijgend doorwerken niet.

Opruimen van testpagina's die je zelf hebt aangemaakt mag wel, maar vraag het eerst en noem
de pagina bij naam.

---

## Wat je nodig hebt voor je begint

| | |
|---|---|
| De opname | een `.mp4` uit `out/` van dit project, of een SharePoint-link |
| De projectmap | code en documentatie, waar de feiten vandaan komen |
| De Notion-projectpagina | staat meestal in de `README`, in een comment of in de docs |
| Sector en afdeling | uit het project of uit de Notion-pagina |
| Een bronpagina | een bestaande demopagina in dezelfde stijl, die je dupliceert |

**Zoek de Notion-link zelf op** voor je erom vraagt:

```bash
grep -rEio 'https?://(www\.)?notion\.(so|com)/[^ )"'"'"'>]+' . \
  --include='*.md' --include='*.ts' --include='*.tsx' --include='*.py' \
  --include='*.json' --include='*.yml' --include='*.yaml' 2>/dev/null | sort -u
```

Vind je er meer dan één, vraag dan welke de projectpagina is. Vind je er geen, vraag dan
om de link; ga niet gokken op basis van de projectnaam.

Lees daarna die pagina met `notion-fetch` en gebruik hem als bron voor de probleem- en
resultaatpunten. De projectpagina bevat vaak de oorspronkelijke situatie bij de klant, en
die is met terugwerkende kracht lastig te reconstrueren uit alleen de code.

---

## Vaste paginastructuur

Titel is de demonaam in het Nederlands, zonder het woord "demo" erin. Icon en banner
komen uit de bronpagina die je dupliceert, zie "De pagina aanmaken". Zet ze niet zelf:
via de MCP kun je alleen een emoji of een externe URL meegeven, en het huisicoon
`NXT_PHASE_-_AVATAR_8.jpg` is een geüploade afbeelding.

```
## Bekijk de Demo
<video src="…">
---
<columns>
  <column>                              <column>
    ## Wat laat deze demo zien?           ## Interesse?
    (twee alinea's lopende tekst)         (callout gray_bg, vaste CTA)
    ---                                   ---
    ## Het probleem                       ## Resultaat
    (callout red_bg, 4-5 bullets)         (callout green_bg, 3-6 bullets)
    ---                                   ---
    ## De oplossing                       ## Geschikt voor
    (callout blue_bg, 4-5 bullets)        (table, 3-4 rijen)
  </column>                             </column>
</columns>
---
---
## Watch the Demo
<video src="…">
---
<columns>… exact hetzelfde in het Engels …</columns>
```

De kleuren zijn semantisch en liggen vast: `red_bg` voor het probleem, `blue_bg` voor de
oplossing, `green_bg` voor het resultaat, `gray_bg` voor de CTA. Nooit iets anders.

De CTA-callout is op elke pagina letterlijk gelijk. Overnemen, niet herschrijven:

```
<callout color="gray_bg">
	**Wil je dit ook voor jouw organisatie?**
	[Plan een afspraak](https://calendly.com/jan-nxtphase/30min)
	[nxtphase.ai](http://nxtphase.ai)
	[info@nxtphase.ai](mailto:info@nxtphase.ai)
</callout>
```

Engels: `**Want this for your organization?**` en `[Schedule a meeting]`, verder identiek.

De tabel "Geschikt voor" heeft een lege header-rij en dan **Sector**, **Afdeling**,
**Integraties**. Bij een tooldemo heet de derde rij **Tool**. Zijn er compliance-eisen, dan
komt daar **Randvoorwaarden** bij ("Verwerking volledig binnen de EER, geen klantdata voor
modeltraining"). Vul Integraties uit wat er werkelijk in de code zit, niet uit wat
aannemelijk klinkt.

---

## De twee alinea's

Dit is het enige echt geschreven stuk: samen 60 tot 110 woorden.

**Alinea 1 zet de uitgangssituatie neer**, vanuit het werk van een mens en niet vanuit de
techniek. Twee openingen zijn in gebruik:

- Anonieme klantcasus, verleden tijd: *"Een productiebedrijf stelde de wekelijkse
  productieplanning volledig handmatig op in losse Excel-bestanden."*
- Generieke beroepsgroep, tegenwoordige tijd, als er geen concrete klant achter zit:
  *"Ziekenhuizen plannen dagelijks tientallen artsen, patiënten en kostbare middelen."*

De anonimiseerregels van deze skill gelden onverkort, zie `anonimiseren.md`. Standaard dus
"een productiebedrijf", "een fabrikant van premium producten". Alleen bij expliciete
toestemming een naam, zoals bij Elastofirm.

Concrete getallen mogen mee als het project ze levert ("meer dan 14.000 rubberprofielen").
Verzinnen mag niet, ook hier niet.

**Alinea 2 introduceert de oplossing** met een van deze twee formules:

- *"In deze demo zie je hoe **NXT Phase AI** een [X] heeft gebouwd die [Y]."*
- *"In deze demo zie je een [X] die [Y]."*

Zitten er twee varianten in één pagina, dan komt er een derde regel: *"Twee varianten: een
demo voor A en een demo voor B."*

---

## De bullets

Alle drie de callouts werken hetzelfde: geen punt aan het eind, geen "wij" of "onze" als
onderwerp, één gedachte per bullet, 6 tot 16 woorden.

**Het probleem**, 4 tot 5 bullets. Constateringen over de oude situatie, feitelijk en niet
dramatisch. Bouw op van operationeel naar organisatorisch.

> - Productieplanning 100% handmatig in Excel
> - Forecasts van meerdere retailers in losse bestanden
> - Geen real-time inzicht in beschikbare capaciteit per lijn
> - Planners hadden uren nodig voor een weekplanning

**De oplossing**, 4 tot 5 bullets. Wat het systeem doet, tegenwoordige tijd. Zijn er
instelbare varianten, dan genest met een bold label:

> - Drie instelbare algoritmes afhankelijk van de prioriteit:
>   1. **Optimaliseer artsplanning** - maximale bezetting per arts

Sluit waar het kan af met een bullet over aansluiting op de bestaande omgeving ("Volledig
vanuit de bestaande Microsoft-omgeving, geen nieuwe tools nodig").

**Resultaat**, 3 tot 6 bullets. Uitkomst voor de gebruiker, niet voor de techniek. Bold
alleen op de kernwinst:

> - Weekplanning die uren kostte, klaar in **minuten**
> - Zoektijd teruggebracht van minuten naar **seconden**

Geen percentages, geen euro's, geen ROI. Tijdsvergelijkingen alleen als de demo ze
aantoonbaar laat zien. De laatste bullet gaat vaak over een tweede-orde-effect: minder
afhankelijkheid van seniorkennis, een herbruikbare fundering, meer tijd voor zorg.

---

## Toon

Zakelijk Nederlands, kort. De pagina's verkopen door precies te zijn, niet door
enthousiast te zijn. Geen superlatieven, geen uitleg over hoe het model werkt, geen jargon
zonder ontkoppeling. Waar techniek nodig is staat de functie erbij: "visuele similarity
search: upload een schets of foto en het systeem vindt de meest gelijkende profielen".

**Lees `schrijfstijl.md` voor je begint te schrijven.** Daar staan de verboden woorden en
zinsconstructies, en de harde regel dat er nooit een em-dash in de tekst staat. Let op: de
bestaande pagina's in de library houden zich daar niet aan, dus kopieer hun formuleringen
niet.

De lezer wordt alleen in de CTA met "je" aangesproken, in de rest van de pagina derde
persoon.

**Er zijn twee generaties stijl in de library.** De pagina's tot juni 2026 zijn strak en
feitelijk. De nieuwste, Klantmail Categoriseren en Routeren, opent met een beeld in plaats
van een situatieschets en gaat over de mensen aan beide kanten:

> Achter elke mail zit iemand die iets wil weten: of de technicus nog komt, of het bedrag
> klopt, hoe het abonnement meeverhuist. En aan de andere kant zit een medewerker die elke
> ochtend een volle inbox opent en eerst moet uitzoeken wat waar hoort.

Vraag welke van de twee je gebruikt. Vuistregel: narratief voor demo's waar mensen in het
proces zitten (klantenservice, HR, onderwijs), zakelijk voor operations- en data-demo's.

---

## Engels

Geen letterlijke vertaling, wel dezelfde inhoud en hetzelfde aantal bullets. De kop is
`## Watch the Demo`. Een paar oudere pagina's gebruiken in plaats daarvan een `#`-kop met
de Engelse demonaam; volg dat niet na, want het is inconsistent.

Spelling: Amerikaans. De vaste CTA bevat "organization", dus dat is de goedkoopste keuze.
De nieuwste pagina staat op Brits ("standardised", "catalogue") en wijkt daarmee af.

---

## De video in de pagina krijgen

Dit is het lastigste deel van de stap, dus lees het voor je begint.

**De bestaande pagina's hebben de video als geüploade `.mp4` in Notion zelf**, niet als
externe link. Dat is de vorm om aan te houden: hij speelt inline af, ook voor iemand
buiten onze tenant, en hij blijft werken als een sharing-instelling verandert.

Drie routes, in volgorde van voorkeur:

**1. Upload via de MCP, als het bestand onder de 20 MiB blijft.** `notion-create-file-upload`
geeft een `upload_url` terug; POST daar het bestand als multipart form-data naar toe met de
meegegeven headers, en gebruik de `suggested_markdown` uit het antwoord als `src` van het
`<video>`-blok.

```bash
ls -lh out/<naam>.mp4   # controleer eerst de grootte
```

De MCP kent alleen de single-part upload en die stopt bij 20 MiB. Een render van 100
seconden op 1080p zit daar vaak net boven. Kom je eroverheen, dan is een tweede export met
een hogere CRF vaak genoeg; dat is voor een demopagina prima kwaliteit.

**2. Zit hij er structureel boven, laat de mp4 dan met de hand in de pagina slepen.** Maak
de pagina met een `<empty-block/>` op de plek van de video en zeg er expliciet bij dat die
nog gevuld moet worden. Notion's eigen upload-limiet in de UI ligt veel hoger dan die van
de API.

**3. Alleen als er echt geen bestand is, een SharePoint-link.** Zet die dan **niet** in een
`<video>`-blok. SharePoint en Stream leiden om naar een inlogpagina, en dan zie je in
Notion een leeg vlak of een foutmelding in plaats van een speler. Gebruik een gewone link
onder de kop:

```
## Bekijk de Demo
[▶ Bekijk de demo-opname](<sharepoint-url>)
```

Bij deze route moet je twee dingen controleren voor je de pagina deelt, en dat kan alleen
de mens die de sessie draait:

- Het deellink-type in SharePoint staat op **"Iedereen met de link"**, niet op "Personen in
  NXT Phase AI". Zonder dat ziet de klant een inlogscherm.
- Open de link in een privévenster waar je niet met een NXT Phase-account bent ingelogd, en
  kijk of de video daadwerkelijk speelt.

Vraag dit expliciet en ga niet door zolang het niet bevestigd is. Een demopagina die je
naar een prospect stuurt en waar de video op een inlogscherm uitkomt is erger dan geen
pagina.

---

## De pagina aanmaken

**Maak de pagina niet met `notion-create-pages`.** Dan komt hij zonder icoon en zonder
banner binnen, en valt hij meteen op tussen de andere pagina's. Het icoon is een geüploade
afbeelding en de MCP kan alleen een emoji of een externe URL zetten, dus dat is achteraf
niet te repareren zonder de UI.

Dupliceer in plaats daarvan een bestaande demopagina en overschrijf de inhoud. Icoon,
banner en de plek onder de Demo Library komen dan gratis mee.

**Kies de bronpagina op stijl.** Het duplicaat erft de opmaak, dus neem een pagina uit
dezelfde stijlgeneratie als degene die je gaat schrijven: narratief of zakelijk, zie
"Toon". Klantmail Categoriseren en Routeren is de narratieve; Productie Planning de
zakelijke.

De volgorde luistert, want tussen stap 1 en 4 staat er een pagina in de Library met de
video van een andere klant erin:

**1. Upload eerst de video** volgens "De video in de pagina krijgen" en houd de
`suggested_markdown` bij de hand. Doe dit vóór het dupliceren, dan is het venster waarin de
kopie nog de oude demo toont zo klein mogelijk.

**2. `notion-duplicate-page`** met de `page_id` van de bronpagina. Je krijgt direct een
`page_id` en `page_url` terug, maar het vullen gebeurt asynchroon: haal de nieuwe pagina
één keer op met `notion-fetch` en controleer dat de inhoud er staat voor je verdergaat. Het
duplicaat landt onder dezelfde ouder als het origineel, dus als de bronpagina goed hangt
staat de kopie meteen onder de Demo Library. De titel is dan nog `<bronnaam> (1)`.

**3. `notion-update-page`** met `command: "update_properties"` en `properties: {"title": "…"}`
voor de nieuwe demonaam. Doe dit meteen na het dupliceren, want in het overzicht staat nu
een pagina die "Productie Planning (1)" heet.

**4. `notion-update-page`** met `command: "replace_content"` en de volledige nieuwe pagina
in `new_str`, Nederlands en Engels in één keer, inclusief het nieuwe `<video>`-blok. Icoon
en banner blijven daarbij staan; die zitten niet in de content. `allow_deleting_content` is
niet nodig zolang de bronpagina geen subpagina's of databases bevat, en dat hebben de
demopagina's niet. De oude video is een bijlage, geen subpagina, en verdwijnt gewoon mee.

De content is Notion-flavored Markdown; lees `notion://docs/enhanced-markdown-spec` via
`notion-fetch` als je twijfelt over de syntax van `<columns>`, `<callout>` of `<table>`.
Gebruik tabs voor de indentatie binnen die blokken, geen spaties.

**Toon de teksten eerst.** Print de Nederlandse en Engelse versie in het gesprek en laat ze
goedkeuren voor je stap 4 draait. Dit is klantmateriaal en het gaat vaak ongewijzigd naar
een prospect.

Na het aanmaken doe je zelf twee dingen niet, en zeg je dat er ook bij:

- De pagina toevoegen aan de juiste sectiekop op de Library-overzichtspagina
- De pagina publiceren of delen

---

## Nakijklijst

- [ ] Video speelt af, getest zonder NXT Phase-account
- [ ] Bij een SharePoint-link: sharing staat op "Iedereen met de link", bevestigd door de gebruiker
- [ ] Klantnaam geanonimiseerd, tenzij er toestemming is; zie `anonimiseren.md`
- [ ] Geen cijfer op de pagina dat niet uit het project of de demo komt
- [ ] Geen interne systeemnamen, repo-paden, branchnamen of medewerkersnamen overgenomen
- [ ] Callout-kleuren kloppen: rood, blauw, groen, grijs
- [ ] CTA-blok letterlijk overgenomen, beide talen
- [ ] Nederlandse en Engelse versie hebben hetzelfde aantal bullets
- [ ] Pagina staat onder de Demo Library en niet ergens los in de workspace
- [ ] Titel is de nieuwe demonaam, niet `<bronnaam> (1)`
- [ ] Geen tekst, bullet, tabelrij of video van de bronpagina blijven staan
- [ ] Icoon en banner staan er, overgenomen uit de bronpagina
- [ ] De pagina nog onder de juiste sectiekop hangen
