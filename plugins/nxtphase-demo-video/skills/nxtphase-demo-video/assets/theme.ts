import { loadFont as loadSans } from "@remotion/google-fonts/Inter";
import { loadFont as loadMono } from "@remotion/google-fonts/JetBrainsMono";

/**
 * De NxtPhase-huisstijl gebruikt Switzer (via Fontshare, zie fonts.ts). Die is
 * niet als npm-pakket beschikbaar, dus we renderen met Inter als visueel
 * neutrale vervanger. Dit is de enige plek waar het font wordt vastgelegd.
 *
 * Let op: dit font geldt alleen voor het kader van de video (schermteksten,
 * eindkaart). Alles binnen een app-venster erft de fonts van de app zelf, en
 * die komen uit de gescopete CSS in src/styles/.
 */
// Alleen de gewichten en subsets die we echt gebruiken: anders doet elke
// render honderden losse fontverzoeken.
export const SANS = loadSans("normal", {
  weights: ["400", "500", "600"],
  subsets: ["latin"],
}).fontFamily;

export const MONO = loadMono("normal", {
  weights: ["400", "600"],
  subsets: ["latin"],
}).fontFamily;


/**
 * Kader van de video: de NxtPhase-huisstijl. Deze waarden liggen vast.
 *
 * Heeft een project kleuren van de klant nodig, zet die dan in het project zelf
 * en niet hier. En verschuif ze ten opzichte van de echte huisstijl, zie
 * reference/anonimiseren.md.
 */
export const C = {
  cream: "#F5F0E8",
  surface: "#F7F3ED",
  card: "#FFFFFF",
  ink: "#090909",
  inkSoft: "#6E6862",
  stone: "#9B9590",
  green: "#3E9B5D",
  greenText: "#2E7647",
  orange: "#E86B10",
  orangeText: "#A44A08",
  line: "rgba(9,9,9,.10)",
  lineSoft: "rgba(9,9,9,.06)",
} as const;


/** Uniforme entree-curve voor alles wat in beeld schuift. */
export const EASE_ENTER = [0.16, 1, 0.3, 1] as const;
export const EASE_INOUT = [0.45, 0, 0.55, 1] as const;

export const shadow = {
  card: "0 1px 2px rgba(9,9,9,.04), 0 8px 24px rgba(9,9,9,.05)",
  raised: "0 2px 6px rgba(9,9,9,.06), 0 18px 50px rgba(9,9,9,.10)",
} as const;
