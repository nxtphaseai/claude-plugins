# Vragenlijst

Dit zijn de dingen die je niet uit de code, uit git of uit Azure kunt aflezen. Je vraagt ze
aan de gebruiker. Wat je hier niet gevraagd hebt en ook niet kunt verifiëren, schrijf je
niet op.

Regels voor het stellen:

- Stel de vragen met AskUserQuestion, maximaal vier per aanroep. Blok A is dus twee rondes.
- Geef altijd concrete keuzes, geen open vraag waar een keuze kan. Zet de optie die bij dit
  project het meest waarschijnlijk is vooraan, en zeg erbij waarom je dat denkt ("de repo
  heeft een `.github/workflows/`, dus ik ga uit van een pipeline").
- Stel een vraag nooit als je het antwoord al geverifieerd hebt. Zie `verificatie.md`.
- Herhaal het antwoord kort terug in je samenvatting voor je gaat schrijven, zodat een
  verkeerd begrepen antwoord niet in een .docx belandt.

## Blok A: altijd vragen, voor je begint met schrijven

A1 tot en met A5 stel je bij elk project, ook als je denkt het antwoord te weten. A6 stel je
alleen als de verkenning meer dan één omgeving laat zien; die uitzondering staat bij de vraag
zelf. Samen bepalen ze de voorpagina, welke bestanden je maakt en op welk niveau je schrijft.

### A1. Klantnaam en projectnaam, precies zoals ze op de voorpagina komen

Vraag beide in een vraag met vrije invoer. De klantnaam is de organisatie zoals de klant
zichzelf schrijft, niet de mapnaam van de repo, bijvoorbeeld `Voorbeeld Groep`. De
projectnaam is wat er is gebouwd, in de woorden van de klant: `Analyse tool en Routing
tool`, `E-mailassistent en offertegenerator`.

Effect: regel 1 en regel 3 van de voorpagina, en de front matter `klant:` en `project:`.

### A2. Opleverdatum

Vraag de datum die op de voorpagina moet staan. Voluit in het Nederlands: `4 augustus 2026`.
Dit is de datum van de oplevering, niet de datum van vandaag, en niet de datum waarop je de
Azure-stand hebt gecontroleerd. Die laatste noteer je apart als "stand geverifieerd op ...".

Effect: regel 5 van de voorpagina en de front matter `datum:`.

### A3. Welke documenten, en hoe heet het gebruikersdocument

Opties: beide documenten, alleen de gebruikershandleiding, alleen de technische
documentatie. Vraag er meteen bij hoe het gebruikersdocument moet heten. In de ene
oplevering heette het `Gebruikershandleiding`, in de andere `Opleverrapport en functionele
beschrijving`, en dat verschil is inhoudelijk: het tweede is meer een rapport over wat er
is opgeleverd, het eerste meer een bedieningsinstructie.

Effect: welke Markdown-bestanden je schrijft, de front matter `document:`, en de
verwijzingen over en weer ("de begeleidende technische documentatie beschrijft ..."). Lever
je maar één document, haal die verwijzing dan weg.

### A4. Wie gebruikt de tool

Vraag welk team of welke rol dagelijks met de tool werkt: bijvoorbeeld de klantenservice,
het salesteam, de planning. Vraag door of dat mensen zijn die de tool zelf instellen of
alleen bedienen.

Effect: de je-vorm en het detailniveau van de gebruikershandleiding, de "Zo gebruik je ..."
stappen, en of er een hoofdstuk komt over instellingen die de klant zelf beheert (in het
routeringsproject de routing-mapping en de automatiseringen).

### A5. Wie beheert de omgeving: interne IT of een externe partij

Opties: de interne IT-afdeling van de klant, een externe Azure-partij, gedeeld, nog niet
belegd. In de ene oplevering lag het tenantbeheer bij een externe partij en leverde Nxt
Phase AI alleen de applicaties en de inrichting daarop, en dat staat letterlijk zo in
hoofdstuk 2.

Effect: de toon en de aannames van de technische documentatie (mag je ervan uitgaan dat de
lezer rechten heeft in de portal?), de zin over wie wat beheert in de inleiding, en de
formulering van de beheerchecklist.

### A6. Welke omgeving is opgeleverd

Stel deze vraag alleen als je meer dan één omgeving hebt gevonden (dev, acceptatie,
productie, of app settings als `ROUTING_ENV=acc`). Vraag welke omgeving het document
beschrijft, en of de andere omgevingen benoemd moeten worden.

Effect: welke resource-namen, URL's en app settings in de tabellen komen, en of er een zin
komt als "de tool draait nu tegen de acceptatie-omgeving van het CRM-systeem".

## Blok B: vragen die je alleen stelt als de verkenning ze oproept

Loop deze lijst na nadat je de code en de Azure-stand hebt bekeken. Stel alleen de vragen
waarvan de trigger is opgegaan. Bundel ze in zo min mogelijk AskUserQuestion-rondes.

### B1. Leveren we de broncode op, en hoe

- Trigger: altijd wanneer je de technische documentatie schrijft. De tabel "Opgeleverde
  artifacts" kan niet gemaakt worden zonder dit antwoord.
- Vraag: zip met de volledige repository, overdracht van de GitHub-repository naar de klant,
  of blijft de repo bij ons en krijgt de klant alleen de draaiende applicatie.
- Effect: de tabel met opgeleverde artifacts. Bij een zip schrijf je "als zip met de
  volledige repository" en noem je per map wat erin zit (`app/`, `server/`, `terraform/`).
  Blijft de repo bij ons, dan noem je in de artifacts-tabel alleen wat de klant echt in
  handen krijgt, en beloof je nergens toegang tot de repository.

### B2. Waar staat de CI/CD-pipeline na oplevering

- Trigger: er staat een workflow in `.github/workflows/`.
- Vraag: blijft de pipeline op de GitHub-organisatie van Nxt Phase AI, of gaat hij over naar
  de klant. Zo ja, per wanneer.
- Effect: de deployment-paragraaf en de secrets-paragraaf. Blijft hij bij ons, dan schrijf
  je dat expliciet op, met de stap die de klant zou moeten zetten om zelf te deployen
  (publish profile downloaden en als repository-secret toevoegen, zoals in de documentatie
  van het routeringsproject). Gaat hij over, dan noem je welke secrets de klant zelf moet
  aanmaken (`ACR_USERNAME`, `ACR_PASSWORD`, `AZURE_WEBAPP_PUBLISH_PROFILE`).

### B3. Via welk kanaal worden inloggegevens en secrets gedeeld, en aan wie

- Trigger: de applicatie heeft een login, een gedeeld secret of een API-key die de klant
  nodig heeft. Bijvoorbeeld `BASIC_AUTH_USER`, `BASIC_AUTH_PASSWORD`, `ADDIN_SHARED_SECRET`.
- Vraag: via welk kanaal en aan welke persoon of rol worden ze aangeleverd.
- Effect: geen enkele waarde komt in het document. Je schrijft, net als in de echte
  documenten, "De inloggegevens worden apart aangeleverd." Vermeld wel waar de waarde
  aanpasbaar is (App Service, Settings, Environment variables) en welke setting het stuurt.
  Zet nooit een wachtwoord, key, connection string of client secret in de Markdown, ook niet
  als de gebruiker hem je geeft. Zet ook geen link naar de deelplek in het document.

### B4. Wie beheert de Azure-tenant na oplevering, en wie mag app settings wijzigen

- Trigger: er zijn Azure-resources, en A5 gaf "extern", "gedeeld" of "nog niet belegd".
- Vraag: wie is eigenaar van de subscription, en wie mag app settings, model-deployments en
  netwerkregels aanpassen.
- Effect: hoofdstuk over de Azure-omgeving en de beheerchecklist. Als de klant geen rechten
  heeft, schrijf je de beheerinstructies als "vraag de tenantbeheerder om ..." in plaats van
  als een `az`-commando dat de lezer zelf uitvoert.

### B5. Nazorg, support of SLA

- Trigger: altijd checken, maar alleen opnemen bij een expliciet antwoord.
- Vraag: is er een nazorgperiode afgesproken, een supportafspraak of een SLA, en wie is het
  aanspreekpunt aan beide kanten.
- Effect: zonder expliciet antwoord komt hier NIETS over in het document. Geen "wij staan
  klaar", geen reactietijd, geen periode, geen beloofde beschikbaarheid. Wel toegestaan
  zonder afspraak: de instructie hoe je een probleem meldt, zoals in de ene oplevering "meld
  het bij Nxt Phase AI, vermeld het tijdstip en een of twee meldingsnummers".

### B6. Indicatieve maandkosten

- Trigger: er staan Azure-resources met een SKU (App Service Plan, ACR, AI Foundry), en je
  kunt de SKU en het volume verifiëren.
- Vraag: mogen indicatieve maandkosten in het document, en op welke tarieven baseren we die
  (pay-as-you-go West Europe, of een afwijkende afspraak of korting van de klant).
- Effect: de paragraaf indicatieve kosten. Neem je hem op, dan altijd als bandbreedte per
  resource met de zin dat de bedragen geverifieerd moeten worden in de Azure Pricing
  Calculator, en altijd met de grootste variabele erbij (in beide echte documenten het
  tokenverbruik). Geen antwoord betekent: paragraaf weglaten.

### B7. Schermafbeeldingen

- Trigger: je schrijft een gebruikershandleiding met "Zo gebruik je ..."-stappen.
- Vraag: zijn er screenshots beschikbaar, van welke schermen, en in welke map staan ze.
- Effect: de `![Bijschrift](pad.png)`-regels in de Markdown. Zonder bestanden zet je geen
  placeholders en geen verwijzingen naar beeld dat er niet is. Schrijf de stappen dan zo dat
  ze zonder plaatje te volgen zijn, en noem in je eindrapport welke schermen een screenshot
  zouden verdienen.

### B8. Bekende beperkingen en open punten

- Trigger: altijd bij de technische documentatie, en bij de gebruikershandleiding zodra je
  in de code iets vindt dat nog niet af is (een stand die niet geïmplementeerd is, een
  hardcoded lijst, een ontbrekende koppeling).
- Vraag: welke beperkingen en open punten moeten expliciet benoemd worden, en welke zijn
  bewuste ontwerpkeuzes.
- Effect: het onderscheid tussen twee lijsten. Bewuste keuzes gaan onder "functionele
  beperkingen" met de reden erbij ("er is bewust geen automatische backfill"). Dingen die
  nog niet af zijn krijgen in de gebruikershandleiding een "Let op:"-regel, zoals in het
  routeringsproject over de AI-velden die wel gevuld worden maar nog niet op het scherm
  staan.

### B9. Kennisoverdracht

- Trigger: de klant moet na oplevering zelf iets kunnen (een analyse herdraaien, de routing
  aanpassen, een deploy uitvoeren).
- Vraag: is er een sessie of overdracht geweest of gepland, en moet die in het document.
- Effect: alleen bij ja een korte alinea met wat er is overgedragen en aan wie. Nooit een
  toekomstige sessie beloven die niet is afgesproken.

### B10. Taal van de documenten

- Trigger: de klant is internationaal, de codebase of de interface is Engels, of de
  gebruiker noemt Engelstalige lezers.
- Vraag: Nederlands of Engels.
- Effect: de volledige documenttekst. Bij Engels blijven de huisstijlregels gelijk, blijven
  resource-namen en app settings ongewijzigd, en geldt het verbod op em-dashes en op
  marketingtaal onverkort.

### B11. Mogen klantnaam en resource-namen letterlijk in het document

- Trigger: altijd kort controleren voor je gaat schrijven.
- Vraag: mogen de klantnaam, de resource-namen, de URL's en de mailboxadressen letterlijk in
  het document.
- Effect: normaal is het antwoord ja, want het is een document van de klant zelf. De echte
  opleveringen noemen de web-apps, de resourcegroep en het adres van de gedeelde mailbox
  gewoon bij naam, want zonder die namen kan de beheerder de resource niet terugvinden. Is
  het antwoord nee, dan vervang je namen consequent door een rolomschrijving en meld je in
  je eindrapport welke tabellen daardoor minder bruikbaar worden.

## Als het antwoord "weet ik niet" is

Dan komt het onderwerp in de lijst met open punten, niet als bewering in de tekst. Schrijf
op wat er openstaat en wie het kan beantwoorden, en vul het gat niet met een aanname, een
schatting of een algemene formulering.
