---
name: nxtphase-documentatie
description: Genereer de opleverdocumentatie van een NxtPhase-project vanuit de projectmap: een gebruikershandleiding voor de eindgebruikers en een technische documentatie voor de IT-afdeling, allebei als bewerkbaar Word-document in de huisstijl. Gebruik deze skill bij elk verzoek om opleverdocumentatie, een gebruikershandleiding, een handleiding, een opleverrapport, een functionele beschrijving, een technische documentatie of beheerdocumentatie voor een project dat we gebouwd hebben, en bij het bijwerken daarvan. Verifieert elke bewering tegen de broncode en de echte Azure-deployment, en stelt de openstaande vragen aan de gebruiker in plaats van ze in te vullen.
metadata:
  tags: documentatie, oplevering, handleiding, word, docx, azure, huisstijl, nxtphase
---

# Opleverdocumentatie van NxtPhase

Aan het eind van een project leveren we twee documenten op:

- de **Gebruikershandleiding**, voor het team dat met de tool gaat werken;
- de **Technische documentatie**, voor de IT-afdeling die de omgeving beheert.

Ze horen bij elkaar en verwijzen naar elkaar. De gebruikershandleiding beschrijft de
werking en de bediening, de technische documentatie de architectuur, de resources en het
beheer.

Deze skill draait vanuit de projectmap van het klantproject en levert beide documenten als
bewerkbare .docx in de huisstijl.

---

## De drie harde regels

**1. Niets in de documentatie is een aanname.** Elke bewering traceert naar de broncode
(bestand en regel), naar de uitkomst van een read-only commando, of naar een expliciet
antwoord van de gebruiker. Kun je iets niet onderbouwen, dan gaat het niet in het
document: het wordt een vraag, of het wordt weggelaten. Dit geldt met nadruk voor
beloftes over kosten, veiligheid, beschikbaarheid, herstel en privacy. Zie
`reference/verificatie.md`, en lees dat bestand voor je begint.

**2. Vraag het, in plaats van het aannemelijk in te vullen.** Leveren we de code op als
zip? Via welk kanaal gaan de inloggegevens? Wie beheert de tenant straks? Blijft de
pipeline bij ons? Dat zijn afspraken, geen technische feiten, en ze staan nergens in de
code. De vaste vragenlijst en het moment waarop je elke vraag stelt staan in
`reference/vragenlijst.md`.

**3. Geen AI-taal, en nooit een em-dash.** Alles wat de klant leest is gewoon Nederlands.
Geen "naadloos", geen "krachtig", geen "het is niet alleen X, het is Y", en geen em-dash
`—` of en-dash `–` als leesteken. Herschrijf de zin, of gebruik een komma, dubbele punt
of punt. De volledige lijst staat in `reference/schrijfstijl.md`, en die lees je voordat
je gaat schrijven.

Nooit een secret, sleutel, wachtwoord, connection string of publish profile in een
document. Alleen de naam van de instelling en waar hij staat.

---

## Werkwijze

### Stap 1: verkennen en verifiëren

Nog niets schrijven. Eerst vaststellen wat er echt is.

Lees `reference/verificatie.md` en werk die volgorde af:

1. De projectmap: README, deployment-workflows, infrastructuurcode, startup-scripts,
   dependencies, de env-variabelen die de code echt uitleest, de plekken waar limieten en
   drempels staan, en de tests.
2. De echte deployment, met read-only Azure CLI-commando's. Nooit iets aanmaken,
   wijzigen of verwijderen tijdens het documenteren.
3. Git en de pipeline: waar staat de repository, welke workflows zijn er, wanneer is er
   voor het laatst gedeployd.

Leg tijdens het verkennen `docs/oplevering/bronnen.md` aan: per bewering die je straks
gaat opschrijven, waar hij vandaan komt. Dat bestand blijft in het project staan, zodat de
documentatie achteraf controleerbaar is en een volgende ronde niet opnieuw hoeft te graven.

Verzamel onderweg drie lijstjes:

- wat je hebt kunnen vaststellen;
- wat tegenstrijdig is (bijvoorbeeld een app setting die de code leest maar die in Azure
  niet bestaat), want dat is een bevinding voor de gebruiker en hoort bij de open punten;
- wat je niet kúnt vaststellen omdat het een afspraak is en geen feit.

Werkt de Azure CLI niet, of ontbreken de rechten, meld dat dan meteen aan de gebruiker en
vraag hoe je verder moet. Ga niet documenteren op basis van wat de code suggereert dat er
in Azure hoort te staan.

### Stap 2: de vragen stellen

Stel blok A uit `reference/vragenlijst.md` via `AskUserQuestion`. Dat zijn zes vragen en
`AskUserQuestion` neemt er vier per aanroep, dus twee rondes. Stel daarna alleen die vragen
uit blok B waarvan je in stap 1 hebt gezien dat ze spelen, plus de tegenstrijdigheden die
je hebt gevonden.

"Weet ik niet" is een geldig antwoord. Dat onderwerp komt dan in de lijst met open punten,
niet als bewering in de tekst.

### Stap 3: de indeling laten goedkeuren

Lever eerst de inhoudsopgave van beide documenten, met per hoofdstuk één regel over wat
erin komt en waar de inhoud vandaan komt. Laat die goedkeuren voordat je gaat schrijven.
Dat scheelt een hele ronde herschrijven.

De vaste indelingen staan in `reference/gebruikershandleiding.md` en
`reference/technische-documentatie.md`. Wijk daarvan af als het project daarom vraagt,
maar benoem waarom.

### Stap 4: schrijven

Lees `reference/schrijfstijl.md`, en daarna het bestand van het documenttype dat je
schrijft. Schrijf naar:

- `docs/oplevering/gebruikershandleiding.md`
- `docs/oplevering/technische-documentatie.md`

Het Markdown-dialect en de verplichte front matter staan in `reference/markdown.md`. De
voorpagina en de inhoudsopgave komen uit de front matter en de koppen; zet ze niet zelf in
de tekst.

Schrijf de twee documenten na elkaar, niet door elkaar. Ze hebben een ander register en
een andere lezer, en dat gaat mis als je wisselt.

### Stap 5: bouwen

```bash
python <skillmap>/assets/build_docx.py docs/oplevering/technische-documentatie.md \
  -o "docs/oplevering/260804 Technische documentatie.docx"
```

De bestandsnaam volgt de bestaande oplevering: `<jjmmdd> <Documenttype>.docx`, met de
opleverdatum. Dus `260804 Gebruikershandleiding.docx` en
`260804 Technische documentatie.docx`.

`<skillmap>` is de map waarin deze SKILL.md staat. Als plugin geïnstalleerd is dat
`${CLAUDE_PLUGIN_ROOT}/skills/nxtphase-documentatie`, handmatig geïnstalleerd
`.claude/skills/nxtphase-documentatie` in het project of in `~/.claude/`. Zoek het pad op
als je het niet zeker weet, en gebruik een absoluut pad in het commando.

Het script heeft alleen Python 3.8 of nieuwer nodig, verder niets: geen pip install, geen
pandoc, geen Word. Gebruik `python3` waar dat de naam is. Controleer de exitcode: `1`
betekent dat het document geschreven is maar dat er iets ontbrak, meestal een afbeelding.

### Stap 6: controleren en opleveren

Loop de controlelijst uit `reference/huisstijl.md` na op het gebouwde document, en de
inhoudelijke controlelijst uit het bestand van het documenttype.

Lever daarna aan de gebruiker:

- de twee .docx-bestanden;
- de lijst met open punten die in de documenten staat;
- de vragen die nog niet beantwoord zijn;
- de tegenstrijdigheden die je in stap 1 hebt gevonden.

Zeg er expliciet bij welke beweringen op een antwoord van de gebruiker rusten en niet op
code of Azure. Dat zijn de plekken die verouderen zodra een afspraak verandert.

---

## Een bestaand document bijwerken

Werk de Markdown-bron in `docs/oplevering/` bij en bouw opnieuw. Bewerk nooit de .docx
als bron: die wordt bij de volgende run overschreven.

Draai stap 1 wel opnieuw, ook bij een kleine wijziging. De deployment kan veranderd zijn
sinds de vorige keer, en de zin "stand geverifieerd op <datum>" in de technische
documentatie moet kloppen.

Is de .docx door de klant bewerkt en wil je die wijzigingen behouden, vraag dan eerst wat
er is aangepast en verwerk dat in de Markdown-bron.

---

## Naslag

| Bestand | Waarvoor |
|---|---|
| `reference/verificatie.md` | Hoe je elke bewering onderbouwt, met de read-only commando's |
| `reference/vragenlijst.md` | De vragen aan de gebruiker, en wanneer je ze stelt |
| `reference/gebruikershandleiding.md` | Structuur, bouwstenen en toon van de gebruikershandleiding |
| `reference/technische-documentatie.md` | Structuur, vaste tabellen en beheerhoofdstukken |
| `reference/schrijfstijl.md` | Nederlandse schrijfstijl, verboden woorden, de em-dashregel |
| `reference/huisstijl.md` | Hoe het Word-document eruitziet, en hoe je dat controleert |
| `reference/markdown.md` | Het Markdown-dialect en de opties van `build_docx.py` |
| `assets/build_docx.py` | Markdown naar .docx, alleen standaardbibliotheek |
| `assets/brand/nxt-phase-ai-logo-black.png` | Het logo in de voettekst |
