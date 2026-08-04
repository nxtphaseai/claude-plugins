# Valkuilen

Stuk voor stuk fouten die echt gemaakt zijn en die zich in elk volgend project opnieuw
aandienen. Dit is het meest waardevolle deel van deze skill: ze kosten anders opnieuw een
halve dag.

## Beeldkwaliteit

**Scroll op hele beeldpixels.** Een scroll met fractionele pixels laat dunne lijnen en
kleine cijfers elk frame anders uitrasteren. Dat zie je als trillen, en het valt het eerst
op bij een grafiekas of een tabelrand.

```ts
const snapScroll = (px: number) => Math.round(px * ZOOM) / ZOOM;
```

**Scroll de inhoud, niet de scrollcontainer.** Verschuif je een `section` met
`overflow-y: auto`, dan verschuift ook de rand waarop geknipt wordt en verdwijnt de
onderkant van de inhoud. Zet een `div` binnenin en verschuif die.

**CSS-transities en -animaties uit.** Zie `exactheid.md`. Ze lopen op wandkloktijd terwijl
Remotion frame voor frame rendert, dus het beeld hapert.

**Render met PNG-tussenframes en CRF 16.** De standaard (JPEG 80) kost zichtbaar scherpte
bij kleine cijfers en dunne lijnen. Staat al goed in `assets/remotion.config.ts`.

## Positionering

**Meten in plaats van schatten.** Elke positie die met het oog is geschat, zat er later
naast. Wat wel werkt:

- *Muispositie*: render één frame op schaal 1 en zoek met PIL het doelelement en de
  aanwijzer op kleur. Zo bleek in een eerder project een klik 52 pixels te laag te staan.
  Snellere variant: render een still op het frame van de klik en kijk of de ring op de knop
  ligt.
- *Typografieverhoudingen*: haal ze uit de bronbestanden. De breedte van een tagline volgt
  uit de advance widths in het fontbestand (`fontTools`); waar een woordmerk begint staat in
  het logobestand.
- *Momenten in de stem*: gebruik de tijdstempels van de TTS-API, niet je oor.

**De punt van de muisaanwijzer.** Een cursor-svg op `left/top` zetten plaatst de
linkerbovenhoek op die coördinaat, niet de punt van de pijl. `assets/Cursor.tsx` corrigeert
dat al met `TIP_X`/`TIP_Y`; bouw je een eigen aanwijzer, doe het dan ook.

**Nooit twee aanwijzers tegelijk.** Geef elke aanwijzer een eindframe.

## Compositie

**Transparant is niet wit.** Een kaart met `rgba(kleur, 0)` als achtergrond laat de
paginakleur zien en oogt dus anders dan een kaart met een witte achtergrond. Geef alles
dezelfde basis en leg de tint er als laag overheen:
`backgroundImage: linear-gradient(tint, tint)`.

**Reserveer ruimte voor wat later verschijnt.** Elementen die één voor één opkomen laten de
compositie verspringen. Twee oplossingen: een vaste hoogte voor de rij, of alles vanaf het
begin gedempt tonen (`opacity 0.16`) en laten oplichten. Dat laatste is meestal mooier: bij
drie woorden die na elkaar verschijnen hangt de eerste anders seconden lang links van het
midden.

**Geen valse verversing tussen scenes.** Blijft hetzelfde scherm staan over een scenegrens
heen, laat het venster daar dan niet opnieuw zijn intro-animatie doen. Dat leest als een
refresh. Zet de opkomst alleen aan waar een venster voor het eerst verschijnt.

## Trouw aan de app

**Neem de tekortkomingen van de app over, niet je eigen verbetering.** Kapt de app labels af
op 130px en zet ze altijd rechts van het punt, dan doet de video dat ook. Ziet dat er lelijk
uit bij een punt aan de rand, dan is de oplossing niet het label omklappen (dan wijkt de
video af van de app), maar de synthetische data zo kiezen dat het label past.

**Venstermaat net boven de breakpoint.** Kies de logische breedte van het venster bewust:
1440 ligt net boven een breakpoint van 1400, zodat de brede desktop-indeling geldt. Schaal
daarna het geheel op (1,2 werkt goed) in plaats van de fontgroottes aan te passen; zo
kloppen alle marges en fontgroottes van de echte app.

**Verwijs naar de bron.** Zet in de scene een comment met bestand en regelnummer naar de
render-functie die je hebt overgenomen. Dat maakt controleren en bijwerken mogelijk.

## Scripting

**`ffprobe` schrijft naar stderr, niet stdout.** Wie alleen stdout leest, meet niets.

**Rond een totaal af vóór je het in minuten en seconden splitst.** Anders wordt 119,9
seconden "1:00" in plaats van "2:00".

**Controleer stills, niet de hele video.** Het werkpaard:

```bash
npx remotion still <comp> out/check.png --frame=2130 --scale=0.5
```
