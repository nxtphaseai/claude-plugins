import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { SANS } from "./theme";
import { EDITORIAL } from "./fonts";
import { enter } from "./anim";
import { NxtPhaseLogo, LOGO_RATIO } from "./Logo";

/**
 * VEREIST: zet PPEditorialNew-Italic.otf in public/fonts/ van het project.
 * fonts.ts laadt hem via staticFile("fonts/..."). Ontbreekt hij, dan valt de
 * tagline stil terug op Georgia en klopt de eindkaart niet meer.
 *
 * DE EINDKAART VAN NXTPHASE. Neem deze ongewijzigd over in elke demo-video: dezelfde meshgradient, hetzelfde
 * woordmerk, dezelfde tagline en dezelfde maatverhoudingen. De drie woorden die
 * daar boven het logo stonden komen hier niet terug; de kaart staat meteen in
 * beeld.
 *
 * De verhouding tagline/logo komt van de banner van de huisstijl: het woordmerk
 * is daar 459 px breed en de tagline 364, dus 0,79 keer zo breed.
 */

const LOGO_W = 620;

/**
 * Op de banner is de tagline precies zo breed als het woordmerk zonder het
 * beeldmerk. Dat is geen schatting maar een maat uit het logobestand zelf: de
 * "n" van "nxt" begint op x=107,4 in een viewBox van 509,088 breed.
 */
const WORDMARK_FRACTION = (509.088 - 107.4) / 509.088;

/**
 * Breedte van "We make AI Work" in PP Editorial New Italic, uitgedrukt in em.
 * Opgeteld uit de advance widths in het fontbestand, dus exact.
 */
const TAGLINE_EM_WIDTH = 7.662;

const TAGLINE_SIZE = (LOGO_W * WORDMARK_FRACTION) / TAGLINE_EM_WIDTH;

/**
 * De banner houdt een halve logohoogte tussen de onderkant van het logo en de
 * bovenkant van de hoofdletters. De tekstregel begint iets boven die
 * hoofdletters (0,076 em, nagemeten op een render), dus dat gaat er vanaf.
 */
const GAP = LOGO_W * LOGO_RATIO * 0.5 - TAGLINE_SIZE * 0.076;

const CREAM = "#F5F0E8";
const SIGNAL_GREEN = "#3E9B5D";

/**
 * De achtergrond van de banner: een lichte hoek linksonder die via verzadigd
 * groen naar bijna zwart rechtsboven loopt. Opgebouwd uit een paar radiale
 * vlekken over een donkere basis, zodat er geen harde bandjes in komen.
 */
const Gradient: React.FC<{ drift: number }> = ({ drift }) => (
  <AbsoluteFill
    style={{
      background: "#0a2d1e",
      transform: `scale(${1.06 + drift * 0.04})`,
    }}
  >
    <AbsoluteFill
      style={{
        background: [
          "radial-gradient(58% 88% at 1% 80%, rgba(226,240,228,0.98) 0%, rgba(226,240,228,0) 60%)",
          "radial-gradient(50% 76% at 23% 64%, rgba(74,168,105,0.95) 0%, rgba(74,168,105,0) 64%)",
          "radial-gradient(56% 80% at 47% 32%, rgba(23,92,57,0.9) 0%, rgba(23,92,57,0) 66%)",
          "radial-gradient(68% 96% at 93% 10%, rgba(4,20,13,0.96) 0%, rgba(4,20,13,0) 60%)",
          "radial-gradient(78% 108% at 100% 98%, rgba(3,16,10,0.92) 0%, rgba(3,16,10,0) 56%)",
        ].join(","),
      }}
    />
  </AbsoluteFill>
);

export const Outro: React.FC = () => {
  const frame = useCurrentFrame();

  // Het woordmerk komt pas op als de gesproken zin bijna klaar is; eerder
  // overlappen stem en eindkaart te lang.
  const brand = enter(frame, 62, 34);
  const drift = enter(frame, 0, 260);

  return (
    <AbsoluteFill style={{ fontFamily: SANS, overflow: "hidden" }}>
      <Gradient drift={drift} />

      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
          opacity: brand,
          transform: `translateY(${(1 - brand) * 18}px)`,
        }}
      >
        <NxtPhaseLogo width={LOGO_W} color={CREAM} />
        <div
          style={{
            fontFamily: `"${EDITORIAL}", Georgia, serif`,
            fontStyle: "italic",
            fontWeight: 400,
            fontSize: TAGLINE_SIZE,
            lineHeight: 1,
            marginTop: GAP,
            color: CREAM,
            whiteSpace: "nowrap",
          }}
        >
          We make AI <span style={{ color: SIGNAL_GREEN }}>Work</span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
