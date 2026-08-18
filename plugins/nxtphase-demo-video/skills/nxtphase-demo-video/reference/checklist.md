# Nakijklijst

Opgebouwd uit echte feedback. Loop hem af vóór je oplevert, dan komt het niet alsnog terug.

## Beeld

- [ ] **Geen valse verversing tussen scenes.** Blijft hetzelfde scherm staan over een
      scenegrens heen, dan mag het venster daar niet opnieuw zijn intro-animatie doen. Dat
      leest als een refresh. Zet de opkomst alleen aan waar een venster voor het eerst
      verschijnt.
- [ ] **Klikposities opgemeten, niet geschat.** Render een still op het frame van de klik en
      kijk of de ring op de knop ligt. Coördinaten binnen het appvenster, dan door
      `toScreen()`.
- [ ] **Nooit twee muisaanwijzers tegelijk.** Geef elke aanwijzer een eindframe.
- [ ] **Het gevolg van een handeling is zichtbaar.** Een klik op "invoegen" laat het resultaat
      zien in de omringende applicatie, en daarna wat ermee gebeurt.
- [ ] **Accenten zijn duidelijk en blijven staan.** Een korte puls van anderhalve seconde is te
      subtiel. Gebruik een rand van 3px met een zachte gloed, laat hem inzoomen en staan.
- [ ] **Geen dood moment aan het eind van een scene.** Vergelijk `minScreen` met wat er
      werkelijk gebeurt.
- [ ] **Panelen vallen niet af.** Als de inhoud hoger is dan het venster, maak het venster
      hoger of laat het meescrollen.
- [ ] **Fonts kloppen.** Geen onbedoelde systeem-serif. Het lettertype van de eindkaart
      staat in `public/fonts/`.
- [ ] **Scrolls trillen niet.** Afgerond op hele beeldpixels.
- [ ] **De inhoud scrollt, niet de scrollcontainer.**
- [ ] **Geen verspringende composities** bij elementen die na elkaar opkomen.
- [ ] **Geen eigen verbetering van de app.** Ziet iets er lelijk uit, pas dan de
      synthetische data aan, niet de markup.

## Tempo

- [ ] Liever te strak dan te ruim. Twijfel je, kort in.
- [ ] Een pagina die langs scrollt moet je kunnen lezen: liever een langere scene met een
      tragere scroll dan andersom.
- [ ] De eindkaart komt pas op als de laatste zin bijna klaar is.

## Tekst en stem

- [ ] Geen drieslagen of slogantaal.
- [ ] Geen verzonnen cijfers.
- [ ] Getallen voluit geschreven.
- [ ] Schermteksten uit als er een voice-over is.
- [ ] Scenelengtes komen overeen met de laatste opname.

## Anonimiteit

- [ ] `grep` op de klantnaam, de zaalnamen, de productnamen en de mailadressen, in `src/`,
      `scripts/` en de gegenereerde bestanden.
- [ ] Themakleur verschoven ten opzichte van de huisstijl van de klant.
- [ ] Geen logo of beeldmerk van de klant.
- [ ] Foto's zijn gegenereerd, tonen geen bestaande locatie of persoon en bevatten geen tekst.
- [ ] De verdeling van de synthetische data heeft een andere vórm dan die van de klant.
- [ ] De context speelt in een andere sector dan die van de opdrachtgever.
- [ ] Niets uit een screenshot van een echte mailbox overgenomen.

## Techniek

- [ ] `npx tsc --noEmit` is schoon.
- [ ] Alle Remotion-pakketten op exact dezelfde versie.
- [ ] Geen fontbestanden meegecommit die je niet mag herdistribueren (zie `fonts.md`).
- [ ] Stylesheets opnieuw geëxtraheerd na een wijziging in de app.
- [ ] Gegenereerde HTML opnieuw gegenereerd na een wijziging in de content.

## Demopagina, als die er komt

Alleen relevant als stap 6 is gedraaid. De volledige lijst staat in `demopagina.md`.

- [ ] Video speelt af, getest zonder NXT Phase-account.
- [ ] Bij een SharePoint-link: sharing staat op "Iedereen met de link", door de gebruiker bevestigd.
- [ ] Nederlandse en Engelse versie hebben hetzelfde aantal bullets.
- [ ] CTA-blok letterlijk overgenomen, beide talen.
- [ ] Icon en plek onder de juiste sectiekop nog handmatig zetten, en dat ook gezegd.

## Bij oplevering vertellen

- Wat er is gewijzigd en waarom.
- Wat je bewust anders hebt gedaan dan gevraagd, en waarom.
- Wat er nog openstaat of wat je hebt laten liggen omdat er niet om gevraagd was.
