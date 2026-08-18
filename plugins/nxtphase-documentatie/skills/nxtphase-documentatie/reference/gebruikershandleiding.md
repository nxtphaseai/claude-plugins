# Gebruikershandleiding

Dit bestand beschrijft hoe je de gebruikershandleiding opbouwt. De lezer van het
eindresultaat is een medewerker die morgen met de tool moet werken: een
klantenservicemedewerker, een salesmedewerker, een teamleider. Geen techneut. Hij wil
weten wat de tool voor hem doet, wat hij zelf moet blijven doen, en wat hij moet doen als
het misgaat.

Schrijf de handleiding als Markdown volgens `markdown.md` en zet hem daarna om met
`build_docx.py`. Front matter: `document: Gebruikershandleiding` (of, als de klant er om
vraagt, `Opleverrapport en functionele beschrijving`, zoals bij de oplevering van de
offertegenerator).

## Vaste hoofdstukindeling

Gebruik deze volgorde. Sla een hoofdstuk alleen over als het aantoonbaar niet bestaat in
dit project.

1. **Samenvatting.** Altijd hoofdstuk 1. Zie hieronder.
2. **Een hoofdstuk per tool.** Eén tool is één hoofdstuk, ook als er maar één is. Per
   hoofdstuk: wat de tool is, waar hij draait (letterlijke URL), hoe je inlogt,
   stap-voor-stap gebruik, wat je op het scherm ziet, en een tabel met de begrippen,
   velden of metrics die de gebruiker voor zich krijgt.
3. **Bijsturen en feedback.** Wat je doet als de tool het fout heeft. Verplicht zodra de
   tool iets beslist of iets verplaatst, aanmaakt of voorstelt.
4. **Instellingen die de klant zelf beheert.** Alleen als die er zijn. Beschrijf per
   instelling waar hij staat, wat hij doet, en vanaf wanneer een wijziging geldt.
5. **Scope: wat is wel en niet inbegrepen.** Bij een opleverrapport (zoals in het andere
   project) een eigen hoofdstuk met twee lijsten, "Wel inbegrepen" en "(Nog) niet
   inbegrepen". Bij een gebruikershandleiding mag dit in de samenvatting en in "Goed om te
   weten" landen.
6. **Mogelijke vervolgstappen.** Alleen opnemen als de klant er om vraagt of als er een
   afgesproken lijst ligt. Nooit zelf vervolgstappen verzinnen om het document te vullen.
7. **Bijlagen.** Voor lange referentietabellen die het lopende verhaal breken, zoals de
   volledige categorie-indeling in het routeringsproject (9 hoofdcategorieën, 23
   subcategorieën, 74 vragen).

## Hoofdstuk 1: Samenvatting

Dit hoofdstuk moet in gewone taal vier dingen doen, in deze volgorde:

1. **Wat is er opgeleverd.** Noem de tools bij naam en zeg in één zin per tool wat hij
   doet. In het routeringsproject: "Wij leveren twee samenhangende tools op voor de
   klantenservice-e-mail van Voorbeeld Groep."
2. **Waar de grens ligt tussen tool en mens.** Dit is de belangrijkste alinea van het hele
   document. In het routeringsproject: "De behandeling zelf blijft volledig bij de
   medewerkers: er gaat nooit automatisch een antwoord naar de klant zonder dat het team
   daarvoor heeft gekozen." In het andere project: "de tool bereidt voor, de medewerker
   controleert, past aan en verstuurt."
3. **Waar het draait en hoe je erbij komt.** Eén zin over de omgeving en de login, in
   gebruikerstaal. In het routeringsproject: draait in de Azure-omgeving van de klant,
   beveiligd met de Microsoft-login, alleen medewerkers die toegang hebben gekregen komen
   erbij.
4. **Wat dit document is en wat het niet is.** Sluit af met: dit is de
   gebruikershandleiding, de begeleidende technische documentatie beschrijft architectuur,
   resources en beheer voor de IT-afdeling.

Vermijd in de samenvatting: versienummers, resource-namen, modelnamen, frameworknamen.
Die horen in de technische documentatie.

## De vaste bouwstenen

Deze vijf komen in beide echte opleveringen terug. Gebruik ze consequent en met dezelfde
kopteksten, zodat de lezer ze herkent.

### "Zo gebruik je ..." (genummerde stappen)

Een kopje op niveau 3, daarna genummerde stappen die de gebruiker letterlijk kan volgen.
Noem schermnamen, tabbladen en knoppen bij hun echte naam. Maximaal vijf stappen; wordt
het langer, splits dan in twee blokken.

Voorbeeld (een eerder add-in-project, "Zo gebruik je de add-in"):

1. Open een aanvraagmail in Outlook.
2. Open het zijpaneel van de assistent via de add-in-knop in de Outlook-werkbalk.
3. Het paneel toont welke informatie de assistent in de mail heeft herkend, bijvoorbeeld de
   gevraagde datum en het aantal deelnemers, en wat er nog mist.
4. Lees het concept-antwoord, pas aan waar je wilt, en verstuur het zelf.

Kopvarianten die zijn gebruikt: "Zo draai je een nieuwe analyse", "Zo gebruik je de Routing
tool", "Zo pas je de routing aan", "In de praktijk". Kies een variant die het werkwoord van
de gebruiker bevat.

### "Goed om te weten" (grenzen in een bulletlijst)

Een bulletlijst direct na een gebruiksuitleg, met de grenzen en de verrassingen. Elke
bullet is één feit, geen alinea. Hier horen juist de dingen die de tool níet doet.

Voorbeeld (de oplevering van de offertegenerator):

- De offerte volgt exact de geüploade pdf-export uit het boekingssysteem. Er is geen live
  koppeling met dat systeem. Als de aanvraag wijzigt, moet de offerte opnieuw worden
  geëxporteerd en geüpload.
- De bedragen komen uit het boekingssysteem. De totalen worden een op een overgenomen,
  niet herrekend. Een fout in de offerte komt dus door een fout in het boekingssysteem.

Voorbeeld (routering): "Een melding die door een medewerker is opgepakt of verplaatst,
wordt door de tool nooit meer aangeraakt."

### "Let op:" (voor wat nog niet af is)

Een aandachtsblok (`>` in de Markdown) of een alinea die begint met "Let op:". Gebruik dit
uitsluitend voor functionaliteit die nog niet werkt, nog niet zichtbaar is, of niet
gegarandeerd kan worden. Nooit als opsmuk.

Voorbeeld (routering): "Let op: op het moment van schrijven worden deze velden wél al op
elke melding opgeslagen, maar staan ze nog niet op de schermen waar medewerkers werken. Ze
zijn dus nog niet zichtbaar. Het toevoegen ervan aan de paginaweergave is een kleine,
eenmalige aanpassing binnen het CRM-systeem door het IT-team van de klant."

Voorbeeld (offertegenerator): "Let op: ondanks zorgvuldige bouw en testen kunnen we niet
garanderen dat offertes die in structuur sterk afwijken van bovenstaande varianten
automatisch correct worden uitgelezen. Controleer een gegenereerde offerte daarom altijd
voor verzending."

### Een tabel voor wat de gebruiker op het scherm ziet

Elk toolhoofdstuk krijgt minimaal één tabel die de begrippen, velden of metrics uitlegt die
de gebruiker letterlijk voor zich krijgt. Gebruik de schermnaam als rijlabel, niet de
technische veldnaam uit de code, tenzij die twee gelijk zijn.

Beproefde kolomindelingen:

| Situatie | Kolommen |
|---|---|
| Velden in een extern systeem | Veld, Wat erin staat |
| Cijfers in een dashboard | Metric, Wat het meet en hoe het wordt berekend, Goed om te weten |
| Bestemmingen of routes | Queue, Wat hoort erin, Team |
| Standen van een schakelaar | Stand, Wat het betekent voor jou als medewerker |
| Opbouw van een gegenereerd document | #, Pagina, Wanneer, Wat bepaalt de inhoud |

De derde kolom "Goed om te weten" is waardevol: daar staat de valkuil bij het cijfer. In
het routeringsproject bij Sentiment: "Sentiment meet de toon van de klant, niet de ernst
van de situatie: een vriendelijk gemelde storing scoort neutraal." Zoek per rij zo'n zin.
Kun je hem niet onderbouwen uit de code of uit een antwoord van de gebruiker, laat de cel
dan leeg.

### Bijsturen en feedback

Een eigen paragraaf. Bouw hem op als een lijst van situaties die de gebruiker in de praktijk
tegenkomt, elk met een kopje op niveau 3 en een concrete handeling. In het routeringsproject
zijn dat er drie: "Een melding staat in de verkeerde queue", "De routing verwerkt even
niets", "Een bepaald type mail gaat structureel verkeerd".

Vaste elementen in dit hoofdstuk:

- De geruststelling, onderbouwd. In het routeringsproject: "Alles wat de AI doet is een laag
  bovenop het bestaande proces in het CRM-systeem: er kan geen mail of melding verloren
  gaan."
- Het onderscheid tussen een instellingsprobleem (dat lost de klant zelf op) en een
  inhoudelijk probleem (dat is feedback naar Nxt Phase AI).
- Eén concreet feedbackkanaal, met de exacte handeling. In het routeringsproject: een
  comment op de melding met een vermelding van @nxtphase, de reden dat de indeling niet
  klopt, en welke queue het wel had moeten zijn. Vraag de gebruiker welk kanaal geldt als
  het niet uit de code blijkt.
- Wat de gebruiker ondertussen doet zodat de klant niet wacht. De correctie gaat voor, de
  feedback is voor de verbetering achteraf.
- Waarom dit kanaal. Eén korte alinea. Losse signalen via wisselende kanalen raken kwijt.

## Toon en taal

- Je-vorm. "Je logt in met je Microsoft-account", niet "de gebruiker authenticeert".
- Korte zinnen. Eén gedachte per zin.
- Geen jargon, geen resource-namen, geen code, geen modelnamen, geen bestandspaden.
  Schrijf "de tool controleert direct of de juiste kolommen aanwezig zijn", niet "validatie
  van het schema".
- Wel letterlijk: URL's, schermnamen, tabbladnamen, knopteksten, veldnamen zoals de
  gebruiker ze ziet, queue- en mapnamen. Schrijf de URL voluit, ook in lopende tekst.
- Nooit een em-dash of en-dash als leesteken. Komma, dubbele punt, punt of haakjes.
- Geen marketingtaal. Niet "naadloos", "krachtig", "moeiteloos", "revolutionair", en niet
  "het is niet alleen X, het is Y".
- Getallen en bedragen alleen met bron en datum: "op het moment van schrijven (juli 2026)
  kostte een analyse over zes maanden ongeveer 150 euro aan AI-verwerking".

## Maak expliciet wat er níet gebeurt

Dit is het patroon dat in beide documenten de meeste onzekerheid wegneemt. Neem in elke
gebruikershandleiding minimaal drie van dit soort zinnen op, verspreid over samenvatting en
"Goed om te weten":

- "Er gaat nooit ongevraagd een bericht naar de klant."
- "De tool raakt een eenmaal verplaatste melding nooit meer aan."
- "Er is geen live koppeling met het boekingssysteem."
- "Er wordt niets met terugwerkende kracht verplaatst."
- "De assistent bevestigt nooit een datum of een prijs."

Elke zin van dit type moet aantoonbaar zijn in de code. Wijs de plek aan (bestand plus
regel) voordat je hem opschrijft: de guard die op één e-mail per melding controleert, de
check die een al verwerkte melding overslaat, het ontbreken van elke uitgaande send-call.
Kun je het niet aanwijzen, schrijf de zin dan niet op, ook niet in afgezwakte vorm. Zie
`verificatie.md`. Is het gedrag onduidelijk, maak er dan een vraag van, zie `vragenlijst.md`.

## Functionaliteit die nog niet af is

Drie regels, zonder uitzondering:

1. Laat het niet weg. De gebruiker komt er zelf achter, en dan klopt het document niet meer.
2. Beschrijf het niet als af. Geen toekomstige tijd die als heden leest.
3. Markeer het met "Let op: op het moment van schrijven ..." en zeg erbij wie het afmaakt en
   hoe groot het is. Het routeringsproject doet dit twee keer: de AI-velden die nog niet op
   de schermen staan, en de stand "Automatisch" bij automatiseringen die "nog niet
   beschikbaar" is en pas komt zodra het CRM-systeem het toelaat.

Zet ontbrekende functionaliteit die buiten scope viel niet onder "Let op:" maar in de lijst
"(Nog) niet inbegrepen", zoals de offertegenerator doet met de koppeling naar het
boekingssysteem en het digitaal ondertekenen.

## Schermafbeeldingen

- Neem er alleen een op waar woorden tekortschieten: waar een knop staat, hoe een zijpaneel
  eruitziet, welke keuze in een dialoog gemaakt moet worden. Het add-in-project toont het
  zijpaneel van de add-in; het routeringsproject toont de dialoog "Eigenaar wijzigen".
- Verwijs in de tekst naar de afbeelding en zeg wat de lezer erop moet zien. Een losse
  schermafbeelding zonder zin eromheen voegt niets toe.
- Nooit klantdata of herleidbare gegevens: geen echte namen, adressen, e-mailadressen,
  meldingnummers, telefoonnummers, IBAN's of bedragen van echte klanten. Gebruik een
  testrecord of maak de gegevens onleesbaar voordat je de afbeelding opneemt.
- Vraag de gebruiker om de afbeeldingen aan te leveren of om toestemming om ze te maken.
  Verzin nooit een schermafbeelding en beschrijf nooit een scherm dat je niet gezien hebt.
- Opnemen met `![Bijschrift](screenshots/naam.png)`. Het bijschrift is een hele zin.

## Checklist voor het concept

Loop deze lijst langs voordat je de Markdown omzet naar .docx. Bij elk "nee": eerst
repareren.

- [ ] Hoofdstuk 1 zegt in gewone taal wat er is opgeleverd en waar de grens ligt tussen tool
      en mens.
- [ ] Elk toolhoofdstuk noemt de letterlijke URL of de plek in het systeem, en hoe je inlogt.
- [ ] Elk toolhoofdstuk heeft een "Zo gebruik je ..." met genummerde stappen.
- [ ] Elk toolhoofdstuk heeft minimaal één tabel met de begrippen of velden van het scherm.
- [ ] Er staan minimaal drie expliciete "dit gebeurt niet"-zinnen in, en van elke zin heb je
      de plek in de code genoteerd.
- [ ] Alles wat nog niet af is, staat er met "Let op: op het moment van schrijven ...".
- [ ] Er is een hoofdstuk over bijsturen en feedback met een concreet feedbackkanaal.
- [ ] Geen em-dash, geen en-dash, geen marketingtaal.
- [ ] Geen resource-namen, code, modelnamen of bestandspaden in de lopende tekst.
- [ ] Geen bedrag, percentage of doorlooptijd zonder bron en peildatum.
- [ ] Geen klantdata of herleidbare gegevens in de schermafbeeldingen.
- [ ] Elke bewering is terug te voeren op code, op de uitkomst van een read-only commando,
      of op een antwoord van de gebruiker. Wat dat niet is, staat er niet in.
