# Schrijfstijl

Deze regels gelden voor alle tekst die in de twee opgeleverde documenten komt: de
gebruikershandleiding en de technische documentatie. De klant leest deze tekst. Behandel
elke regel hieronder als bindend, niet als advies.

## 1. Nooit een em-dash of en-dash

Gebruik nooit `—` of `–` als leesteken. Ook niet in tabelcellen, bijschriften, kopteksten
of codeblokken die je zelf schrijft. Een gewone hyphen in een samenstelling (`e-mailassistent`,
`AI-velden`, `pay-as-you-go`) is gewoon goed.

| Fout | Goed |
|---|---|
| `E-mailassistent (/emails) — Outlook add-in die aanvraagmails herkent` | `E-mailassistent (/emails): Outlook add-in die aanvraagmails herkent` |
| `ACR Basic ± € 4–5` | `ACR Basic: ongeveer 4 tot 5 euro` |
| `Aanvraag/Offerte — Zakelijk` | `Aanvraag/offerte, zakelijk` |
| `De poller is licht — hij moet dezelfde state lezen` | `De poller is licht en moet dezelfde state lezen.` |
| `Incassostatus controleren - een statusvraag zonder geschil` | `Incassostatus controleren: een statusvraag zonder geschil` |
| `Storing / technische vraag — geen voorbeelden` | `Storing of technische vraag: geen voorbeelden` |

Volgorde van oplossen: herschrijf de zin eerst. Lukt dat niet, gebruik een dubbele punt
(uitleg volgt), een komma (bijzin) of een punt (twee zinnen). Bij bereiken schrijf je
`45 tot 55 euro` of `100 tot 200`.

## 2. Verboden woorden en constructies

Deze woorden staan nooit in de documenten. Vervang ze door wat er feitelijk gebeurt.

| Nooit | In plaats daarvan |
|---|---|
| naadloos | laat weg, of noem het mechanisme: "beide apps gebruiken dezelfde twee model-deployments" |
| krachtig | laat weg, of noem de capaciteit: "100.000 tokens per minuut per deployment" |
| moeiteloos, in een handomdraai | noem de handeling en de tijd: "de wijziging werkt binnen een minuut, zonder herstart" |
| revolutionair, baanbrekend, next-level | laat weg |
| geavanceerd, intelligent, slim | noem het model of de regel: "gpt-5, versie 2025-08-07" |
| robuust, betrouwbaar | noem de rem: "een ontbrekend schakelbestand telt als uit" |
| duik in, ontdek, verken de mogelijkheden | "open het tabblad Routing-mapping" |
| ontgrendel, unlock | "zet de schakelaar op Queue-routing aan" |
| optimaliseren, stroomlijnen | noem het effect: "het werk wordt verdeeld op inhoud in plaats van op kanaal" |
| "het is niet alleen X, het is Y" | één zin met wat het is |
| "of het nu een aanvraag of een offerte is" | "voor aanvragen, offertes en combinaties daarvan" |
| "sneller, slimmer en beter" (drieslag zonder inhoud) | noem één ding dat meetbaar is |
| "Kortom", "Samengevat", "Al met al" aan het begin van een zin | schrap de zin, of vat echt samen in een eigen alinea met nieuwe informatie |
| "in het huidige digitale landschap", "in een wereld waarin" | schrap de hele aanloop, begin bij het probleem |
| uitroeptekens | punt |

Twee extra verboden vormen:

- **Lege drieslagen.** `Snel, veilig en schaalbaar` zegt niets. Schrijf wat waar is:
  "Alleen meldingen met precies één e-mail worden beoordeeld."
- **Retorische vragen als kop of opening.** Geen "Hoe werkt dat dan?". Schrijf de kop
  als een handeling ("Zo pas je de routing aan") of als een onderwerp ("De routing-queues").

## 3. Register per document

**Gebruikershandleiding: je-vorm, gewone taal, handelingen.** De lezer is een medewerker,
geen beheerder. Vermijd resource-namen, environment variables en CLI-commando's; noem de
knop, het tabblad of het veld dat op het scherm staat.

Zo klinkt het goed:

> De Routing tool is beschikbaar op app-klantcontact-routing.azurewebsites.net. Je logt in
> met je Microsoft-account van Voorbeeld Groep.

> Verplaats de melding gewoon handmatig naar de juiste queue, zoals je ook zou doen met een
> mail die in de algemene queue binnenkomt. De tool raakt een eenmaal verplaatste melding
> nooit meer aan, dus je correctie blijft staan.

Terugkerende bouwstenen in dit document: "Zo gebruik je ...", "Zo pas je ... aan",
"Goed om te weten" (bulletlijst met grenzen), "Let op:" (iets werkt nog niet), "Tip om als
team af te spreken:".

**Technische documentatie: zakelijk-neutraal, derde persoon, precies.** Geen je-vorm in
lopende tekst. Wel de gebiedende wijs in instructies ("Voer dit uit direct na het
opschalen", "Voeg deze mappen dus nooit aan het pakket toe"). Noem resources, app settings
en commando's exact zoals ze heten.

Zo klinkt het goed:

> Alle resources draaien in de Azure-tenant van Voorbeeld Groep, in West Europe, in
> resourcegroep rg-klantcontact (subscription voorbeeld-dev). De onderstaande
> stand is geverifieerd op 30 juli 2026.

Terugkerende bouwstenen: uitvoerbare `az`-commando's in een codeblok, "Herkennen als het
vergeten is:" bij een valkuil, "Wat je beter niet doet" als bulletlijst, links naar
Microsoft Learn achter een beschrijvende linktekst.

## 4. Stellige beweringen hebben een bron

Elk getal, elke naam en elke gedragsbewering staat er alleen als je hem hebt gezien in de
code, in de uitvoer van een read-only commando, of in een expliciet antwoord van de
gebruiker.

- `De poller verwerkt maximaal 50 meldingen per ronde` mag alleen als je de default van
  `--max-batch` of `ROUTING_MAX_BATCH` in de code hebt gelezen.
- `gpt-5, versie 2025-08-07, 100.000 tokens per minuut` mag alleen na
  `az cognitiveservices account deployment list`. Neem `sku.capacity` daarbij niet
  ongewijzigd over: die telt in eenheden van 1.000 tokens per minuut, dus capaciteit 100 is
  100.000 tokens per minuut.
- `De add-in kijkt elke 60 seconden of er nieuwe mail is` mag alleen als
  `POLL_INTERVAL_SECONDS=60` in de app settings of de code staat. `Binnen 60 seconden
  verwerkt` volgt daar niet uit: de wachttijd tot de volgende ronde komt bovenop de
  verwerkingstijd.

Vaagheid is geen ontsnapping. Heb je de bron niet, dan schrijf je het ook niet als
"ongeveer 50", "doorgaans binnen een minuut" of "in de regel". Je hebt dan drie opties, in
deze volgorde:

1. Zoek de bron alsnog op.
2. Stel de vraag aan de gebruiker en gebruik zijn antwoord.
3. Laat de bewering weg. Een document zonder die zin is beter dan een document met een
   zin die niet klopt.

Beloof nooit iets over kosten, veiligheid, prestaties of beschikbaarheid dat je niet kunt
aanwijzen. Geen "de tool is veilig", wel "beide web-apps staan volledig achter de
Microsoft-login (Entra); er zijn geen uitgezonderde paden".

## 5. Onzekerheid opschrijven als hij echt bestaat

Bestaat de onzekerheid wel, benoem hem dan expliciet en met een houdbaarheidsdatum. Deze
formuleringen zijn toegestaan en hebben allemaal een echte betekenis:

- `op het moment van schrijven` bij gedrag dat nog verandert. Voorbeeld: "Let op: op het
  moment van schrijven worden deze velden wél al op elke melding opgeslagen, maar staan ze nog
  niet op de schermen waar medewerkers werken."
- `De onderstaande stand is geverifieerd op 30 juli 2026.` bovenaan een resource-overzicht.
- `Indicatieve maandkosten (West Europe, pay-as-you-go, exclusief btw). Verifieer de
  bedragen in de Azure Pricing Calculator.` bij elk bedrag dat je niet uit een factuur haalt.
- `Ter indicatie: in juli 2026 kostte een analyse over zes maanden mail ongeveer 150 euro
  aan AI-verwerking.` met maand en jaartal erbij.
- `Ondanks zorgvuldige bouw en testen kunnen we niet garanderen dat offertes die in
  structuur sterk afwijken van bovenstaande varianten correct worden uitgelezen. Controleer
  een gegenereerde offerte daarom altijd voor verzending.`

Zet zo'n kanttekening bij de bewering zelf, niet in een verzamelalinea achteraan.

## 6. Getallen, eenheden, datums en bedragen

- Decimalen met een komma: `10,5 pt`, `± 0,015 euro per mail`. Duizendtallen met een punt:
  `100.000 tokens per minuut`, `3.500 klantmails per maand`.
- Bedragen: `45 tot 55 euro` of `€ 45 tot € 55`. Nooit `€ 45-55` met een streepje dat een
  en-dash kan worden. Vermeld altijd of het bedrag exclusief btw is.
- Bereiken: `100 tot 200`, `zes tot twaalf maanden`. Getallen tot en met twintig in lopende
  tekst voluit schrijven, tenzij het een meetwaarde of instelling is (`precies één e-mail`,
  maar `standaard 50` en `versie 2025-08-07`).
- Datums voluit in het Nederlands: `4 augustus 2026`, `30 juni 2026`. Geen `04-08-2026`,
  geen `2026-08-04`, behalve waar het letterlijk een modelversie of bestandsnaam is.
- Tijden en intervallen concreet: `elke 60 seconden`, `binnen ongeveer een minuut`,
  `binnen enkele minuten`. Niet "snel" of "vrijwel direct".
- Eenheden voluit of exact zoals Azure ze schrijft: `tokens per minuut`, `B3 (Basic)`,
  `Standard LRS`. Verzin geen eigen afkortingen.

## 7. Tabellen

- Kopregels kort: `Resource`, `Naam`, `Configuratie`, `Functie`. Geen hele vragen als kop.
  Uitzondering: een kop die een vraag beantwoordt mag, als hij kort blijft en de hele
  kolom hem nodig heeft (`Wat erin staat`, `Wanneer staat het aan`).
- Losse termen en waarden in een cel krijgen geen punt: `West Europe`, `Beide`,
  `Python 3.13, always-on, HTTPS only`.
- Bestaat een cel uit één of meer hele zinnen, dan gewone interpunctie met punt:
  "De klant dient herkenbaar een klacht in (ja/nee)."
- Zet in een cel nooit een leeg streepje als vulling. Laat de cel leeg of schrijf `geen`.
- Houd de kolomvolgorde in het hele document gelijk: eerst wat het is, dan hoe het is
  ingesteld, dan waar het voor dient.
- Een tabel is voor feiten die je per rij kunt vergelijken. Uitleg in twee alinea's zet je
  niet in een tabel.

## 8. Eén naam per ding

Kies per tool, scherm, veld en queue één naam en gebruik die in beide documenten, van de
voorpagina tot de bijlage. Ook als de code een andere naam gebruikt.

- De app heet `app-klantcontact-routing` en de map heet `routing`; in de documenten heet
  hij overal **de Routing tool**.
- De map heet `webapp` en de app `app-klantcontact-analyse`; in de documenten heet
  hij overal **de Analyse tool**.
- In de documenten van het andere project heten ze overal **de e-mailassistent** en **de
  offertegenerator**, ook waar de code `/emails` en `/api/*` gebruikt.

Is de codenaam ergens zichtbaar voor de lezer (in de URL, in de Azure Portal, in een
foutmelding, in een commando), leg de koppeling dan één keer uit op de plek waar de lezer
hem voor het eerst tegenkomt, en gebruik daarna weer alleen de gekozen naam:

> Routing tool (app-klantcontact-routing): dashboard plus een poller die elke 60 seconden
> nieuwe meldingen ophaalt.

Hetzelfde geldt voor begrippen: kies `queue` of `wachtrij`, `melding` of `ticket`, en wissel
niet. Neem de termen over die de klant zelf in zijn systeem ziet staan.

## 9. Lees dit terug

Loop na het schrijven, per document, deze vijf punten langs. Corrigeer wat je vindt
voordat je `build_docx.py` draait.

1. **Streepjes.** Zoek op `—` en `–` in de Markdown. Nul treffers, ook in tabellen en
   codeblokken.
2. **Verboden woorden.** Zoek op naadloos, krachtig, moeiteloos, revolutionair,
   geavanceerd, robuust, handomdraai, duik, ontgrendel, Kortom, Samengevat. Nul treffers.
3. **Getallen zonder bron.** Loop elk getal in het document langs en benoem voor jezelf het
   bestand, het commando of het gebruikersantwoord waar het vandaan komt. Kun je dat niet,
   haal het getal weg.
4. **Namen.** Komt elke tool, elk veld en elke queue overal onder dezelfde naam voor? Staat
   de codenaam alleen op de plek waar hij één keer wordt uitgelegd?
5. **Register.** Staat er per ongeluk een `az`-commando of een app setting in de
   gebruikershandleiding? Staat er per ongeluk een je-vorm in de lopende tekst van de
   technische documentatie?
