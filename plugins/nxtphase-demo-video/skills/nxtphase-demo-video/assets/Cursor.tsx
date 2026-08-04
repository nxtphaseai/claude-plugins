import React from "react";
import { useCurrentFrame } from "remotion";
import { move } from "../anim";

/**
 * Een muisaanwijzer die van A naar B beweegt en op het eind kort indrukt.
 * Alleen daar gebruiken waar de kijker moet zien dát er geklikt wordt; verder
 * blijft hij uit beeld.
 */
/** Waar de punt van de pijl in de svg zit. */
const TIP_X = 3;
const TIP_Y = 2;

export const Cursor: React.FC<{
  from: { x: number; y: number };
  to: { x: number; y: number };
  /** Startframe van de beweging. */
  at: number;
  /** Duur van de beweging in frames. */
  duration?: number;
  /** Frame waarop de klik zichtbaar is (na aankomst). */
  clickAt?: number;
  /** Frame waarna de aanwijzer uit beeld is; laat weg om hem te laten staan. */
  until?: number;
}> = ({ from, to, at, duration = 26, clickAt, until }) => {
  const frame = useCurrentFrame();
  if (frame < at - 6) return null;
  if (until !== undefined && frame > until) return null;

  const t = move(frame, at, duration);
  const x = from.x + (to.x - from.x) * t;
  const y = from.y + (to.y - from.y) * t;

  const clicking = clickAt !== undefined && frame >= clickAt && frame < clickAt + 8;
  const ring = clicking ? (frame - clickAt!) / 8 : 0;

  return (
    // De punt van de pijl staat op (3,2) in de svg, niet op (0,0). Zonder deze
    // correctie zet left/top de linkerbovenhoek op de doelcoördinaat en wijst de
    // aanwijzer dus net naast de knop.
    <div
      style={{
        position: "absolute",
        left: x - TIP_X,
        top: y - TIP_Y,
        pointerEvents: "none",
      }}
    >
      {clicking ? (
        <div
          style={{
            position: "absolute",
            left: -10,
            top: -10,
            width: 20 + ring * 34,
            height: 20 + ring * 34,
            marginLeft: -(ring * 17),
            marginTop: -(ring * 17),
            borderRadius: 999,
            border: "2px solid rgba(15,108,189,.55)",
            opacity: 1 - ring,
          }}
        />
      ) : null}
      <svg width="26" height="30" viewBox="0 0 26 30" style={{ display: "block" }}>
        <path
          d="M3 2l16 12.2-7.3.9 4.2 8.6-3.4 1.7-4.2-8.6-5.3 5z"
          fill="#111"
          stroke="#fff"
          strokeWidth="1.6"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
};
