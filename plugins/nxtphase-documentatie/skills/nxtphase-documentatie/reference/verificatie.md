# Verificatie

Dit bestand bepaalt wat er in de opleverdocumenten mag staan. Werk het volledig af
voordat je één regel documentatie schrijft.

## 1. De bewijsregel

Elke bewering in beide documenten traceert naar precies één van deze drie bronnen:

- **(a) Broncode.** Bestand plus regelnummer, uit de projectmap waarin je draait.
- **(b) De uitkomst van een read-only commando.** `az ...`, `gh ...`, `git ...`, met de
  echte output.
- **(c) Een expliciet antwoord van de gebruiker** in deze sessie.

Kun je een bewering niet aan a, b of c hangen, dan gebeurt er één van twee dingen: je
stelt de vraag aan de gebruiker (zie `vragenlijst.md`), of je laat de bewering weg. Nooit
invullen op basis van wat gebruikelijk is, wat in de README staat terwijl de code iets
anders doet, of wat logisch lijkt gezien de rest van de architectuur.

Dit geldt ook voor getallen die er onschuldig uitzien. "De poller draait elke 60
seconden" moet komen uit `startup_routing.sh` regel N met `--interval 60`, of uit de
app setting `POLL_INTERVAL_SECONDS`. "Batchlimiet standaard 50" komt uit de regel in de
code waar die default staat, niet uit het geheugen.

## 2. Verkenningsvolgorde in de projectmap

Loop deze volgorde af. Noteer per stap wat je vindt in het bronnenbestand (§6).

1. **README en docs/.** Lees ze, maar behandel ze als een claim, niet als bewijs. Wat de
   README zegt controleer je in de code. Wijkt de README af, dan is dat een bevinding.
2. **Deployment.** `.github/workflows/*.yml`. Haal eruit: wat triggert de deploy (push
   op main, handmatig), welke jobs er zijn, wat er wel en niet in het deploy-pakket zit,
   naar welke resource elke job deployt, en welke GitHub-secrets de workflow verwacht.
   Wat bewust buiten het pakket blijft (state-mappen, data-mappen) is documentatiewaardig.
3. **Infrastructuur.** `terraform/`, `*.bicep`, `main.tf`, `manual-setup-checklist.md`.
   Stel vast of de infra in code staat en of die code de live situatie weerspiegelt.
4. **Startup en processen.** `Dockerfile`, `startup*.sh`, `Procfile`, het startup command:
   hoeveel processen er in één app draaien en hoe ze starten.
5. **Tech stack.** `requirements.txt`, `pyproject.toml`, `package.json`. Noem alleen
   versies die je hier of in de app-config leest.
6. **Env-variabelen die de code echt uitleest.** Grep, niet gokken:
   ```bash
   grep -rn "os.environ\|os.getenv\|process\.env" --include="*.py" --include="*.js" --include="*.ts" .
   ```
   De uitkomst is de complete lijst van instellingen die de app kent. Alles wat hier niet
   in staat, hoort niet in de app-settings-tabel van de technische documentatie.
7. **Limieten, drempels en intervallen.** Grep op de plek waar ze staan en noteer bestand
   plus regel:
   ```bash
   grep -rn "max_batch\|MAX_BATCH\|interval\|timeout\|retry\|retries\|limit\|batch_size" --include="*.py" .
   ```
   Dit levert de inhoud van een paragraaf als "Ingebouwde begrenzingen": batchlimiet,
   poll-interval, timeouts, retries, wachtstrategie bij 429.
8. **Tests.** `tests/`. Wat getest wordt mag je benoemen als getest. Wat niet getest is,
   noem je niet "getest" en niet "gevalideerd".

## 3. De echte deployment vaststellen met Azure CLI

Draai deze commando's letterlijk. Vervang `<rg>` en `<app>` door de gevonden waarden.
Noteer per commando wat je eruit haalt.

```bash
az account show -o json
```
Welke subscription en tenant je aanspreekt. Klopt die niet met het project, dan stop je
en vraag je de gebruiker om de juiste subscription.

```bash
az group list -o table
az resource list -g <rg> -o table
```
De volledige resource-lijst van de resourcegroep. Dit is de basis van het
resource-overzicht in hoofdstuk 2 van de technische documentatie.

```bash
az webapp list -o table
az webapp show -g <rg> -n <app> -o json
```
Uit `az webapp show` haal je: `httpsOnly`, `state`, `defaultHostName`,
`siteConfig.linuxFxVersion` (runtime of container-image), `possibleOutboundIpAddresses`
en de app service plan-id.

```bash
az webapp config show -g <rg> -n <app> -o json
```
Hieruit komen `alwaysOn`, `appCommandLine` (het startup command), `healthCheckPath`,
`ftpsState`, `http20Enabled` en `numberOfWorkers`. Staat `healthCheckPath` op `null`,
dan is er geen health check ingesteld; dat is een aanbeveling voor hoofdstuk 5, geen
storing.

```bash
az webapp config appsettings list -g <rg> -n <app> -o json
```
**LET OP: dit geeft de waarden van de secrets terug.** Neem uitsluitend de **namen** over
in de documentatie en in het bronnenbestand. Nooit de waarden, ook niet afgekort, ook
niet "de eerste vier tekens". Bij een niet-geheime instelling (`WEBSITES_PORT=8000`,
`POLL_INTERVAL_SECONDS=60`, `STORAGE_ROOT=/data`) mag de waarde wel mee.

```bash
az appservice plan show -g <rg> -n <plan> -o json
```
SKU, tier, aantal instances, Linux of Windows. Dit is de basis voor de kostenparagraaf en
voor de opschaal-instructie.

```bash
az cognitiveservices account show -g <rg> -n <account> -o json
az cognitiveservices account deployment list -g <rg> -n <account> --query "[].{naam:name, model:properties.model.name, versie:properties.model.version, type:sku.name, capaciteit:sku.capacity}" -o table
```
Het eerste geeft kind, SKU, custom subdomein en `properties.networkAcls` (staat de
resource achter een adreslijst, en zo ja hoeveel regels). Het tweede geeft per deployment
de naam, het model, de modelversie, het deployment-type (`sku.name`, bijvoorbeeld
`Standard`, `GlobalStandard` of `DataZoneStandard`) en de capaciteit (`sku.capacity`).
Dat is precies de deployment-tabel uit hoofdstuk 3 van de techdoc uit het routeringsproject.

Twee dingen om hier niet in te trappen. Zonder die `--query` toont `-o table` alleen de
kolommen Name en ResourceGroup, dus dan mis je model, versie, type en capaciteit. En
`sku.capacity` telt in eenheden van 1.000 tokens per minuut: capaciteit 100 betekent
100.000 tokens per minuut. De limiet zelf staat ook in `properties.rateLimits`, met een
regel voor `token` en een voor `request`.

Het quotum in de regio, en hoeveel daarvan al in gebruik is, komt uit een apart commando.
Dat kent geen `-g`, alleen een regio:

```bash
az cognitiveservices usage list -l <regio> --query "[].{metric:name.value, gebruikt:currentValue, limiet:limit}" -o table
```

```bash
az storage account show -g <rg> -n <account> -o json
az resource show -g <rg> -n <naam> --resource-type microsoft.insights/components -o json
az webapp auth show -g <rg> -n <app> -o json
```
Storage: kind, SKU, `allowBlobPublicAccess`, `minimumTlsVersion`. App Insights: bestaat
het, en waaraan hangt het.

Voor App Insights bestaat ook `az monitor app-insights component show -g <rg> -a <naam>`,
maar dat commando zit in de extensie `application-insights`. Is die niet geïnstalleerd,
dan vraagt de CLI interactief of hij hem mag installeren en loopt je sessie vast op die
prompt. Gebruik daarom `az resource show`, of installeer de extensie bewust vooraf.

`az webapp auth show` vertelt of App Service Authentication aanstaat, welke provider er
is ingericht en met welke client-ID. De uitvoer heeft twee vormen. Met de extensie
`authV2` krijg je de v2-vorm: de stand staat in
`properties.globalValidation.requireAuthentication`, de client-ID in
`properties.identityProviders.azureActiveDirectory.registration.clientId`. Zonder die
extensie krijg je de klassieke vorm, met `enabled`, `defaultProvider` en `clientId` op het
hoogste niveau. Kijk in de v2-vorm niet naar `enabled` per provider: providers die nooit
zijn ingericht staan daar ook op `true`, maar met een lege `registration`. Een provider
telt pas als ingericht wanneer er een client-ID onder staat. Zonder deze uitkomst schrijf
je niet dat de app achter Entra-login staat.

Voor de repo: `git remote -v` (waar de code staat), `git log -1 --format="%H %ad %s"`
(welke commit je documenteert) en `gh workflow list` (welke workflows actief zijn).

## 4. Alleen read-only

Tijdens het documenteren maak je niets aan, wijzig je niets en verwijder je niets. Geen
`az ... create`, `update`, `set`, `delete`, `restart`, `deploy`. Geen `terraform apply`.
Geen push, geen workflow-run starten. Je beschrijft de stand, je verandert hem niet.

Faalt een commando door ontbrekende rechten, een verkeerde subscription of een resource
die niet bestaat, dan is dat een **bevinding**. Meld hem aan de gebruiker met het
commando en de foutmelding erbij, en vraag hoe verder. Gok nooit de waarde die je niet
kon ophalen, en schrijf nooit "waarschijnlijk B3" of "vermoedelijk West Europe".
Commando's die de gebruiker later zelf uitvoert (capaciteit ophogen, key roteren,
handmatig deployen) horen wel in het document, als instructie. Voer ze niet uit.

## 5. Secrets versus identifiers

Geen enkele waarde van een secret, key, connection string, client secret, publish profile
of wachtwoord komt in de documentatie of in het bronnenbestand. Je noemt de **naam** van
de instelling en de **plek** waar hij staat.

Goed: "`AZURE_OPENAI_API_KEY`, app setting op beide apps, geeft toegang tot de
taalmodellen in AI Foundry."
Fout: elke regel waarin de waarde zelf staat.

Identifiers zijn iets anders dan geheimen. Een tenant-ID, een client-ID (application ID),
een subscription-ID, een resource-naam, een hostname en een deployment-naam zijn
aanduidingen, geen sleutels. Die horen in het document, want de IT-afdeling heeft ze
nodig om de juiste app-registratie terug te vinden. In beide echte opleveringen staat de
client-ID van de app-registratie dan ook letterlijk in het Azure-hoofdstuk, in de vorm
`App Registration (client ID: 00000000-0000-0000-0000-000000000000) met applicatie-permissie
Mail.Read en admin consent`. De grens: een client-ID mag, de bijbehorende client secret
nooit.

Let op dat dit gaat over het document dat naar de klant gaat. Zet de echte identifiers van
een klant niet in een bestand dat ergens anders terechtkomt, en dus ook niet in een issue,
een commit of een openbare repository.

## 6. Het bronnenbestand

Schrijf tijdens het verifiëren mee in `docs/oplevering/bronnen.md` in de projectmap. Eén regel
per bewering, gegroepeerd per hoofdstuk van het document waar de bewering landt. Format:

```markdown
# Bronnen

Projectmap: <pad>
Commit: <sha> (<datum>)
Subscription: <naam> (<id>)
Geverifieerd op: <datum>

## Technische documentatie, hoofdstuk 2

| Bewering | Type | Bron | Uitkomst |
|---|---|---|---|
| App Service Plan is B3 (Basic), 1 instance | commando | `az appservice plan show -g rg-x -n plan-x` | `sku.name=B3`, `sku.tier=Basic`, `sku.capacity=1` |
| Poller draait met interval 60 s | code | `startup_routing.sh:7` | `python -m routing.poller --loop --interval 60` |
| Batchlimiet standaard 50 | code | `routing/poller.py:64` | `DEFAULT_MAX_BATCH = 50` |
| Always-on staat aan op beide apps | commando | `az webapp config show -g rg-x -n app-x` | `alwaysOn: true` |
| Maandkosten indicatief 45 tot 55 euro | gebruiker | antwoord op vraag K3 | bevestigd op <datum> |
| Geen health check ingesteld | commando | `az webapp config show -g rg-x -n app-x` | `healthCheckPath: null` |
```

Regels voor dit bestand: type is altijd `code`, `commando` of `gebruiker`. Bij `code`
altijd bestand plus regelnummer. Bij `commando` het commando zoals je het draaide, zonder
de secret-waarden uit de output. Bij `gebruiker` naar welke vraag het antwoord hoort en
op welke datum.

Staat een bewering niet in dit bestand, dan staat hij niet in het document. Controleer
dat aan het eind: loop de conceptdocumenten door en zoek per feitelijke bewering de regel
in `bronnen.md`. Wat je niet terugvindt, haal je weg of leg je voor aan de gebruiker.

## 7. Tegenstrijdigheden tussen code en Azure

Deze twee gevallen komen in de praktijk voor en zijn altijd een bevinding:

- **De code leest een env-variabele uit die niet als app setting bestaat.** De app draait
  dan op de default uit de code, of valt om. Meld het aan de gebruiker, met de regel uit
  de code erbij, en vraag of dit bewust is.
- **Er staat een app setting in Azure die de code nergens uitleest.** Meestal een restant.
  Meld het, en zet hem niet in de app-settings-tabel alsof hij werkt.

Zelfde behandeling bij een resource in Terraform die niet in Azure bestaat, een workflow
die naar een andere app-naam deployt dan er draait, of een README die een ander interval
noemt dan de code. Leg de tegenstrijdigheid voor aan de gebruiker, met beide kanten. Los je
hem samen op, dan verwerk je het antwoord (type `gebruiker`). Blijft hij open, dan gaat
hij als los punt naar de paragraaf met open punten en beperkingen in de technische
documentatie. Verzwijg hem nooit.

## 8. Stand geverifieerd op

Zet in de technische documentatie, in de inleiding van het Azure-hoofdstuk, één zin met
de datum waarop je de omgeving hebt uitgelezen. Zo staat het in de techdoc uit het
routeringsproject: "De onderstaande stand is geverifieerd op 30 juli 2026." Gebruik de
echte datum van je `az`-commando's, niet de datum van de oplevering.

Noem in dezelfde alinea ook de subscription en de resourcegroep, zodat een lezer later
kan controleren waar de stand vandaan komt.

## 9. Wat je nooit belooft zonder bewijs

Deze uitspraken mogen alleen in het document als je ze in de code of in Azure hebt
aangetoond, of als de gebruiker ze expliciet bevestigt. Anders laat je ze weg.

- **Uptime, beschikbaarheid, SLA.** Wij leveren geen SLA tenzij de gebruiker zegt dat er
  een SLA is afgesproken, en dan alleen in de woorden van de gebruiker.
- **Doorlooptijden en snelheid.** "Elke 60 seconden" mag als het interval in de code of in
  een app setting staat. Een interval is alleen geen doorlooptijd: uit een poll van 60
  seconden volgt niet dat een mail binnen 60 seconden verwerkt is, want de wachttijd tot de
  volgende ronde komt bovenop de verwerking. Is de doorlooptijd gemeten, schrijf dan dat
  het gemeten is en waarop. Anders "ongeveer", of niets.
- **Kosten.** Altijd als indicatie, altijd met regio, prijsmodel en "exclusief btw", en
  altijd met de zin dat de lezer de bedragen in de Azure Pricing Calculator verifieert.
  Bedragen komen van de gebruiker of uit een gemeten verbruik, niet uit een schatting van
  jou.
- **Security-eigenschappen.** "Achter Entra-login" vraagt om `az webapp auth show`.
  "HTTPS only" om `httpsOnly: true`. "Afgeschermd met een adreslijst" om
  `networkAcls.defaultAction: Deny` plus het aantal regels. "Alleen leesrechten op die
  mailbox" om de daadwerkelijke permissie en de access policy.
- **AVG-conformiteit.** Schrijf nooit dat een oplossing AVG-conform of GDPR-compliant is.
  Beschrijf wat feitelijk zo is: waar de data staat, welke regio, wie erbij kan, wat er
  gelogd wordt en wat er niet gelogd wordt.
- **Dat data niet voor training wordt gebruikt.** Alleen als je het deployment-type hebt
  vastgesteld en je verwijst naar de documentatie van Microsoft. Formuleer het als een
  eigenschap van de dienst met een bronlink, niet als een garantie van ons.
- **Dat iets automatisch herstelt.** Alleen bij een aantoonbare health check, restart
  policy of retry in de code. Staat `healthCheckPath` op `null`, dan controleert App
  Service de app niet actief en wordt een instance die blijft draaien maar niet meer
  antwoordt ook niet vervangen. Schrijf dan niet dat de oplossing zichzelf herstelt. Beloof
  het omgekeerde net zo min: een proces of container dat crasht, wordt door het platform
  wel opnieuw gestart.
- **Dat er geen mail naar de klant gaat.** Alleen als je het hebt aangetoond: geen
  verzend-endpoint in de code, geen `Mail.Send`-permissie op de app-registratie, of een
  ontwerp waarin het resultaat een concept of interne notitie is. Dit is een van de
  belangrijkste beloftes in beide klantdocumenten, dus onderbouw hem hard.

Twijfel je bij een van deze punten, dan is de vraag aan de gebruiker altijd goedkoper dan
de belofte.
