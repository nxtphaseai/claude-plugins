# Technische documentatie

Dit document beschrijft hoe je de technische documentatie opbouwt. De lezer is de
IT-afdeling van de klant of de externe partij die de Azure-tenant beheert. Die lezer kent
het project niet en moet na het lezen de oplossing kunnen beheren: weten wat er draait,
waar het aan hangt, wat er kan misgaan en wat hij zelf mag aanraken.

Toon: zakelijk-neutraal, geen je-vorm. Elke bewering komt uit de code, uit de uitkomst van
een read-only commando, of uit een antwoord van de gebruiker. Kun je iets niet onderbouwen,
laat het weg of stel er een vraag over. Zie `verificatie.md` en `vragenlijst.md`.

## Vaste hoofdstukindeling

Houd deze vijf hoofdstukken aan. Laat een paragraaf weg als hij niet van toepassing is,
maar verzin geen nieuwe hoofdstukvolgorde.

| Hoofdstuk | Paragrafen | Waar de inhoud vandaan komt |
|---|---|---|
| 1. Inleiding | 1.1 Wat we hebben gebouwd, 1.2 Technisch overzicht, 1.3 Ingebouwde begrenzingen, 1.4 Automatiseringen of koppelingen, Tech stack | Broncode, `requirements.txt`/`package.json`, startup-scripts, README, plus het probleem uit de gebruiker |
| 2. De Azure-omgeving | 2.1 Resource-overzicht, 2.2 Indicatieve kosten, 2.3 App settings, 2.4 Koppelingen | `az resource list`, `az webapp show`, `az webapp config appsettings list`, Terraform-bestanden als die er zijn |
| 3. Het AI-platform | 3.1 Wat er staat, 3.2 Beheren: waar en hoe, 3.3 Vooruitkijken, 3.4 Wat je beter niet doet | `az cognitiveservices account deployment list`, de app settings met de deployment-namen, de code die de client opbouwt |
| 4. Deployment en beheer | 4.1 Inrichting, 4.2 en verder een deploy-paragraaf per applicatie, daarna Opgeleverde artifacts, Periodiek beheer en Opschalen, ook genummerd (bij twee applicaties loopt dat tot 4.6) | `.github/workflows/*.yml`, Dockerfile, startup-scripts, `az webapp show`, de repo-boom |
| 5. Security en open punten | 5.1 Uitgangspunten, 5.2 Secrets-overzicht, 5.3 Aanbevolen verbeteringen, 5.4 Functionele beperkingen | Auth-configuratie, app settings, guard clauses in de code, `git log`, openstaande TODO's |

Noem in hoofdstuk 1 expliciet dat de functionele werking in de begeleidende
gebruikershandleiding staat, zodat de lezer weet wat hij hier niet moet zoeken.

Open hoofdstuk 2 met de vaste zin over waar alles draait, plus een verificatiedatum.
Voorbeeld uit het routeringsproject: "Alle resources draaien in de Azure-tenant van
Voorbeeld Groep, in West Europe, in resourcegroep rg-klantcontact (subscription
voorbeeld-dev). Het beheer van de tenant ligt bij de externe Azure-partij; Nxt Phase AI
levert de applicaties en de inrichting daarop. De onderstaande stand is geverifieerd op
30 juli 2026."

Als de klant maar één applicatie heeft, houd je dezelfde indeling aan met één
deploy-paragraaf. Draait er geen taalmodel in de oplossing, laat hoofdstuk 3 weg en
hernummer de rest.

## De vaste tabellen

Deze vier tabellen staan er altijd in, met precies deze kolommen.

### Resource-overzicht (paragraaf 2.1)

`| Resource | Naam | Configuratie | Functie |`

Eén regel per resource, in deze volgorde: Resource Group, App Service Plan, Web Apps,
Storage Account, file shares of containers, AI-resource, AI-project, Application Insights,
Log Analytics, Container Registry, certificaten. Vul de kolom Configuratie met wat de
beheerder moet weten (SKU, regio, runtime, always-on, HTTPS only, mounts, netwerkstand),
niet met alles wat `az` teruggeeft. De kolom Functie is één zin in gewone taal.

Haal de regels op met read-only commando's, niet uit je hoofd:

```bash
az resource list -g <rg> -o table
az webapp show -g <rg> -n <app> --query "{runtime:siteConfig.linuxFxVersion, alwaysOn:siteConfig.alwaysOn, https:httpsOnly, startup:siteConfig.appCommandLine}"
az appservice plan show -g <rg> -n <plan> --query "{sku:sku.name, os:kind, instances:sku.capacity}"
```

### App settings per applicatie (paragraaf 2.3)

`| App setting | Waarde en betekenis |`

Eén tabel per applicatie, met boven elke tabel de app-naam als tussenkopje. Zet in de
tweede kolom de werkelijke waarde alleen als die niet gevoelig is, en zet er altijd bij wat
hij doet. Voorbeelden uit het routeringsproject: "STORAGE_ROOT | /data, het mountpunt van
de Azure Files-share. Hier landen analyses, LLM-caches en dataset-snapshots, zodat alles
een deploy of herstart overleeft." en "ROUTING_MAX_BATCH | Optioneel; standaard 50. De
drempel van de batchwacht."

Voor secrets schrijf je alleen wat de setting stuurt, nooit de waarde. Groepeer varianten
die bij elkaar horen op één regel (`AZURE_OPENAI_*`, `CRM_*`). Zet erboven waar je ze
wijzigt: App Service, Settings, Environment variables, en dat de app daarna automatisch
herstart. Bron: `az webapp config appsettings list -g <rg> -n <app> -o table`, en de code
die de variabelen leest, zodat je de betekenis en de standaardwaarde klopt.

### Opgeleverde artifacts (genummerde paragraaf in hoofdstuk 4)

`| Artifact | Inhoud |`

Vaste rijen: Broncode (repository of repo-zip), Container en build als er een Dockerfile is,
Infrastructuur als er Terraform is, Deployment (workflows en startup-scripts),
Controlescripts als die er zijn, Documentatie. Beschrijf in de kolom Inhoud de echte mappen
met een korte functie erachter, zoals "routing/ (Routing tool: dashboard, poller, live
classifier, routing-mapping en automatiseringen)". Loop de repo-boom af, noem geen map die
niet bestaat.

### Secrets-overzicht (paragraaf 5.2)

`| Secret | Stuurt welk onderdeel |`

Voeg een kolom `App` toe als er meer dan één applicatie is, zoals in het routeringsproject.
Alleen namen, nooit waarden, nooit fragmenten van waarden. Neem ook de secrets op die niet
in Azure staan maar in GitHub (publish profiles, registry-credentials) en de secrets die het
platform zelf beheert (`MICROSOFT_PROVIDER_AUTHENTICATION_SECRET`). Zet erbij waar ze
gewijzigd worden en wat er stopt als er één verloopt.

Draait er een taalmodel, voeg dan in hoofdstuk 3 de deployment-tabel toe:
`| Deployment | Model en versie | Type | Capaciteit | Waarvoor de applicaties het gebruiken |`.
Bron: `az cognitiveservices account deployment list` met de `--query` uit `verificatie.md`,
paragraaf 3. Zonder die query laat `-o table` model, versie, type en capaciteit weg.

## Hoofdstuk 1.3: ingebouwde begrenzingen

Dit is voor een beheerder een van de waardevolste paragrafen. Hij moet regel voor regel uit
de code komen. Zoek naar guard clauses, vroege returns, standaardwaarden van
commandoregel-argumenten, drempels, intervallen, retries, timeouts en env-vars die gedrag
uitschakelen. Grep op `max`, `limit`, `batch`, `interval`, `timeout`, `readonly`, `dry`,
`enabled`, en lees elke plek waar de code besluit om iets níet te doen.

Beschrijf per rem drie dingen:

1. Wat hij begrenst, in gewone taal.
2. Wat er gebeurt als de grens geraakt wordt.
3. Of hij uit te zetten is, en zo ja waar.

Uit het routeringsproject, als maatstaf voor het detailniveau:

- Geen backfill: alleen meldingen die ná het starten binnenkomen worden verwerkt.
- Verse-melding-regel: alleen meldingen met precies één e-mail worden automatisch
  beoordeeld.
- Verwerkt-lijst: een melding gaat nooit twee keer door de LLMs.
- Batchlimiet (`--max-batch`, standaard 50): ziet een tick méér kandidaten dan deze grens,
  dan verwerkt hij er geen enkele. Dit is de bescherming tegen een onverwachte bulk.
- Drietraps-schakelaar, live gelezen bij elke tick: uit, categorisatie of routing. Een
  ontbrekend of onleesbaar schakelbestand telt als uit.
- Leesmodus-rem `ROUTING_READONLY`: zet alle schrijfacties stil, ongeacht de
  dashboard-schakelaars.

Maak het onderscheid tussen instelbaar en niet-instelbaar expliciet. In het
routeringsproject is de batchlimiet instelbaar via een app setting, terwijl de regel dat
meldingen met een signaal (klacht, geschildreiging, compensatie, spoed) nooit een concept
krijgen niet uit te zetten is zonder codewijziging. Schrijf dat er letterlijk bij. Beloof
nooit dat iets "niet kan" als de code alleen een standaardwaarde hanteert.

## Hoofdstuk 3: beheren

Behandel in deze volgorde: capaciteit ophogen bij throttling, model of modelversie wijzigen,
keys roteren, verbruik en kosten volgen, en tot slot "wat je beter niet doet".

Regels voor dit hoofdstuk:

- Read-only commando's die in het document komen, heb je zelf gedraaid tegen de echte
  resource. Beheercommando's die iets wijzigen (capaciteit ophogen, key roteren, deployen)
  voer je nooit uit, ook niet om ze te controleren: die staan er als instructie voor de
  lezer, met de echte resourcenamen erin en de syntax nagekeken met `az <groep> --help`.
  Zie `verificatie.md`, paragraaf 4. Een commando dat je op geen van beide manieren hebt
  kunnen verifiëren, gaat niet in het document.
- Bij Microsoft-functionaliteit link je naar `learn.microsoft.com` in plaats van de uitleg
  over te schrijven. Schrijf één zin context en daarachter de link, zoals "Stappenplan:
  Sleutels roteren." Zo veroudert het document niet mee met de portal.
- Noem bij capaciteit het beschikbare quotum in de regio en hoeveel daarvan in gebruik is,
  zodat de lezer weet of er ruimte is zonder aanvraag bij Microsoft. Die twee getallen komen
  uit `az cognitiveservices usage list -l <regio>`, niet uit een schatting; zie
  `verificatie.md`, paragraaf 3. Krijg je dat commando niet uitgevoerd, laat de getallen dan
  weg.
- Bij keys roteren: benoem dat er twee keys zijn, dus roteren kan zonder downtime, en noem
  elke applicatie die dezelfde key gebruikt. In het routeringsproject staat er expliciet:
  vergeet de Analyse tool niet als je bij de Routing tool roteert.
- Bij kosten volgen: schrijf dat een budget alleen signaleert. Het stopt geen verbruik en de
  kostendata loopt een dag achter. Het enige harde plafond is het tokenquotum per minuut.
- "Wat je beter niet doet" is een bulletlijst met per punt de handeling en het gevolg. De
  klassieker: een deployment hernoemen of verwijderen breekt de applicaties omdat die de
  deployment op naam aanroepen.

## De valkuil-vorm

Gebruik voor elke beheerhandeling met een verborgen bijwerking deze vaste opbouw: eerst het
probleem, dan het commando, dan "Herkennen als het vergeten is:" met het symptoom. Dat laatste
blok is verplicht, want de beheerder leest het document meestal pas als er al iets stuk is.

Het voorbeeld uit het routeringsproject, paragraaf 4.6:

> Probleem: de AI-resource is afgeschermd met een adreslijst. Alleen de uitgaande
> IP-adressen van de apps en de beheerwerkplek mogen hem aanroepen. Die adressen horen bij
> de prijscategorie van het App Service Plan, niet bij de app. Na een wijziging van
> categorie sluit de firewall de apps dus buiten. Dit speelt bij opschalen naar een andere
> categorie en bij verhuizing naar een ander plan of een andere regio, niet bij meer
> instances binnen dezelfde categorie, een restart of een deploy.
>
> Commando: haal `possibleOutboundIpAddresses` van elke app op, vul de adreslijst opnieuw
> en controleer daarna dat de stand Enabled, Deny en het juiste aantal adressen toont.
>
> Herkennen als het vergeten is: beide apps blijven draaien en mails worden opgehaald, maar
> elke categorisatie mislukt met HTTP 403 en een melding over Virtual Network of Firewall
> rules. Dat lijkt op een key- of quotumprobleem maar is dat niet.

Zet er waar van toepassing bij hoe je tijdelijk terugdraait, en waarschuw voor de knop die
erger is dan het probleem. In het routeringsproject: kies bij netwerktoegang nooit
Disabled, want dat schakelt niet de firewall uit maar de publieke toegang zelf, waarna
beide apps stilvallen.

## De kostenparagraaf

Vaste vorm, altijd:

1. Kop het lijstje met "Indicatieve maandkosten (regio, pay-as-you-go, exclusief btw)".
2. Eén regel per kostenpost, met een bandbreedte, niet met één getal.
3. Een totaalregel met de grootste variabele erbij benoemd. Bij beide referentieprojecten is
   dat het tokenverbruik.
4. De zin dat de bedragen geverifieerd moeten worden in de Azure Pricing Calculator op basis
   van de actuele tarieven en het werkelijke volume.

Noem nooit een bedrag dat je niet kunt onderbouwen. Een SKU-prijs onderbouw je met de
Pricing Calculator of met de factuur van de klant. Een tokenprijs per verwerkte eenheid
onderbouw je met een gemeten run, zoals in het routeringsproject: "Een volledige analyse
over zes maanden mail kostte in juli 2026 ongeveer € 150 aan tokens." Heb je die meting
niet, schrijf dan dat de post volume-afhankelijk is en vraag de gebruiker om cijfers.
Vermeld ook of er gereserveerde capaciteit is ingekocht; is die er niet, schrijf dat er
per token wordt afgerekend.

## Hoofdstuk 5: security en open punten

Vier paragrafen, in deze volgorde.

- **Uitgangspunten.** Bulletlijst: hoe toegang geregeld is (Entra, Basic Auth, gedeeld
  secret), waar de data staat en of die de tenant verlaat, welke rechten een
  integratiegebruiker heeft en welke bewust niet, welke begrenzers er zijn, en wat er wel en
  niet gelogd wordt. Wees precies over de negatieve beweringen: "er worden nooit e-mails
  verstuurd of verwijderd" schrijf je alleen als je in de code hebt vastgesteld dat de
  rechten en de aanroepen dat uitsluiten.
- **Secrets-overzicht.** De tabel hierboven, plus waar ze gewijzigd worden.
- **Aanbevolen verbeteringen.** Open hiermee de zin dat dit geconstateerde aandachtspunten
  zijn en geen storingen. Wees eerlijk over wat nog niet goed staat. Voorbeelden uit het
  routeringsproject: er is geen health check ingesteld, en één App Service Plan draagt beide
  apps waardoor een zware analyse-run de andere tool kan vertragen. Noem per punt het
  nadeel en de logische vervolgstap.
- **Functionele beperkingen.** De bewuste ontwerpkeuzes die de beheerder anders als bug
  aanmeldt: geen backfill, alleen verse meldingen, geen live koppeling waar handmatige
  upload gekozen is, categorie-indeling niet via de interface aanpasbaar.

## Checklist voordat je omzet naar Word

Loop deze punten na op het concept in Markdown, en pas daarna `build_docx.py`.

- [ ] Elke resourcenaam, SKU, regio en versie komt uit de uitkomst van een read-only
      commando, en de verificatiedatum staat in hoofdstuk 2.
- [ ] Elk commando in het document is uitgevoerd of gecontroleerd, en gebruikt de echte
      resourcegroep- en resourcenamen van dit project.
- [ ] Geen enkele secret-waarde, connection string, key of client secret staat in de tekst
      of in een voorbeeldoutput.
- [ ] De vier vaste tabellen staan erin met de juiste kolomkoppen, en elke tabelrij is
      terug te leiden tot code of CLI-uitkomst.
- [ ] Elke rem in paragraaf 1.3 verwijst naar een echte plek in de code, en per rem staat er
      of hij uit te zetten is.
- [ ] Elke bedragregel is een bandbreedte, staat onder het kopje "indicatief", en de
      Pricing Calculator wordt genoemd.
- [ ] Bij elke beheerhandeling met een bijwerking staat "Herkennen als het vergeten is:".
- [ ] Microsoft-functionaliteit is gelinkt naar learn.microsoft.com, niet overgeschreven.
- [ ] Hoofdstuk 5.3 en 5.4 zijn ingevuld en niet leeg gelaten om het net af te laten lijken.
- [ ] Geen em-dash of en-dash, geen AI-marketingtaal, geen belofte over gedrag, kosten of
      veiligheid die niet aantoonbaar is.
- [ ] De front matter klopt (klant, project, document, datum) en er staat geen zelfgemaakte
      voorpagina of inhoudsopgave in de Markdown.
