import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { enter } from "../anim";
import { C, shadow } from "../theme";

/**
 * Een appvenster in beeld. De inhoud wordt op zijn eigen logische maten
 * gerenderd en als geheel opgeschaald: zo is elke marge en fontgrootte exact
 * die van de echte app, alleen ingezoomd voor leesbaarheid op video.
 */

export const STAGE_W = 1920;
export const STAGE_H = 1080;

/**
 * Waar het venster staat. Met de voice-over staan er geen schermteksten meer
 * onder het venster, dus het mag verticaal gecentreerd: (1080 - 940) / 2 = 70.
 * Zet je de schermteksten weer aan (zie Caption.tsx), zet dit dan terug op 26.
 */
export const WINDOW_TOP = 70;
export const CAPTION_Y = 990;

export type WindowGeom = {
  zoom: number;
  x: number;
  y: number;
  w: number;
  h: number;
};

/** Berekent de plaatsing van een venster van w x h logische pixels. */
export const geom = (w: number, h: number, zoom: number, top = WINDOW_TOP): WindowGeom => ({
  zoom,
  x: (STAGE_W - w * zoom) / 2,
  y: top,
  w: w * zoom,
  h: h * zoom,
});

/** Zet een punt binnen het appvenster om naar beeldcoördinaten (voor de muis). */
export const toScreen = (g: WindowGeom, vx: number, vy: number) => ({
  x: g.x + vx * g.zoom,
  y: g.y + vy * g.zoom,
});

export const AppWindow: React.FC<{
  children: React.ReactNode;
  contentW: number;
  contentH: number;
  g: WindowGeom;
  /** Titelbalkje met adres; laat weg voor een app die geen browser is. */
  url?: string;
  start?: number;
  /**
   * Laat het venster opkomen. Alleen aanzetten als het venster voor het eerst
   * in beeld komt. Blijft hetzelfde scherm over een scenegrens heen staan, dan
   * moet dit uit: de opkomst leest daar als een onverklaarbare verversing,
   * terwijl de overgang tussen de scenes het beeld al doorkruist.
   */
  animateIn?: boolean;
}> = ({ children, contentW, contentH, g, url, start = 0, animateIn = false }) => {
  const frame = useCurrentFrame();
  const p = animateIn ? enter(frame, start, 24) : 1;
  const chromeH = url ? 44 : 0;

  return (
    <div
      style={{
        position: "absolute",
        left: g.x,
        top: g.y,
        width: g.w,
        height: g.h + chromeH,
        borderRadius: 12,
        border: `1px solid ${C.line}`,
        boxShadow: shadow.raised,
        overflow: "hidden",
        background: C.card,
        opacity: p,
        transform: `translateY(${(1 - p) * 24}px) scale(${0.99 + p * 0.01})`,
      }}
    >
      {url ? (
        <div
          style={{
            height: chromeH,
            background: C.surface,
            borderBottom: `1px solid ${C.line}`,
            display: "flex",
            alignItems: "center",
            gap: 9,
            padding: "0 16px",
          }}
        >
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              style={{ width: 10, height: 10, borderRadius: 999, background: "rgba(9,9,9,.13)" }}
            />
          ))}
          <div
            style={{
              marginLeft: 12,
              background: C.card,
              border: `1px solid ${C.line}`,
              borderRadius: 999,
              padding: "3px 14px",
              fontFamily: "ui-monospace,'Cascadia Mono',Consolas,monospace",
              fontSize: 13,
              color: C.inkSoft,
            }}
          >
            {url}
          </div>
        </div>
      ) : null}

      <div style={{ width: g.w, height: g.h, overflow: "hidden" }}>
        <div
          style={{
            width: contentW,
            height: contentH,
            transform: `scale(${g.zoom})`,
            transformOrigin: "top left",
          }}
        >
          {children}
        </div>
      </div>
    </div>
  );
};

/** De vaste achtergrond van elke scene. */
export const Stage: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ background: C.cream }}>{children}</AbsoluteFill>
);
