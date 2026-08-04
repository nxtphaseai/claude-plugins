import { continueRender, delayRender, staticFile } from "remotion";

/** Naam waaronder het display-font van de huisstijl beschikbaar is in CSS. */
export const EDITORIAL = "PP Editorial New";

/**
 * Beide web-apps laden Switzer via Fontshare (zie de <link> in hun index.html).
 * De video doet exact hetzelfde, zodat de typografie klopt en niet "ongeveer"
 * lijkt. Lukt het laden niet, dan valt de CSS vanzelf terug op system-ui en
 * gaat de render gewoon door: een mislukte render is erger dan een ander font.
 */
const FONTSHARE = "https://api.fontshare.com/v2/css?f[]=switzer@400,500,600&display=swap";

let started = false;

export const loadSwitzer = () => {
  if (started || typeof document === "undefined") return;
  started = true;

  const handle = delayRender("Switzer laden (Fontshare)");
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = FONTSHARE;
  document.head.appendChild(link);

  const done = () => continueRender(handle);
  Promise.race([
    Promise.all([
      document.fonts.load("400 15px Switzer"),
      document.fonts.load("500 15px Switzer"),
      document.fonts.load("600 15px Switzer"),
    ]),
    new Promise((resolve) => setTimeout(resolve, 10000)),
  ]).then(done, done);
};

/**
 * Het display-font van de huisstijl, voor de tagline op de eindkaart. Anders
 * dan Switzer staat dit bestand lokaal in public/fonts/, dus hier is geen
 * netwerk in het spel en kan de render er gewoon op wachten.
 */
let editorialStarted = false;

export const loadEditorial = () => {
  if (editorialStarted || typeof document === "undefined") return;
  editorialStarted = true;

  const handle = delayRender("PP Editorial New laden");
  const face = new FontFace(
    EDITORIAL,
    `url(${staticFile("fonts/PPEditorialNew-Italic.otf")}) format("opentype")`,
    { style: "italic", weight: "400" },
  );
  face.load().then(
    (loaded) => {
      document.fonts.add(loaded);
      continueRender(handle);
    },
    () => continueRender(handle),
  );
};

/**
 * Heeft het project een eigen lettertype nodig, bijvoorbeeld omdat een app dat
 * via een <link> laadt en het dus niet in de geëxtraheerde CSS zit, voeg hier
 * dan een loader toe volgens hetzelfde patroon en roep hem aan vanuit Root.tsx.
 *
 * Roep hem echt aan: een export die nergens gebruikt wordt, wordt door de
 * bundler weggeoptimaliseerd en dan valt de tekst stil terug op een systeemfont.
 */
