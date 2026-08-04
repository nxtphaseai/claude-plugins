import { Easing, interpolate } from "remotion";
import { EASE_ENTER, EASE_INOUT } from "./theme";

const clamp = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

/** 0 -> 1 met de standaard entree-curve. */
export const enter = (frame: number, start: number, duration = 20) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    ...clamp,
    easing: Easing.bezier(...EASE_ENTER),
  });

/** 0 -> 1 -> 0: komt op, blijft staan, gaat weer weg. */
export const inOut = (
  frame: number,
  start: number,
  hold: number,
  fade = 15,
) => {
  const a = enter(frame, start, fade);
  const b = interpolate(frame, [start + fade + hold, start + fade + hold + fade], [0, 1], {
    ...clamp,
    easing: Easing.in(Easing.cubic),
  });
  return a - b;
};

/** Symmetrische curve voor bewegingen die ergens naartoe gaan en stoppen. */
export const move = (frame: number, start: number, duration: number) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    ...clamp,
    easing: Easing.bezier(...EASE_INOUT),
  });

/** Getal dat optelt, met de entree-curve zodat het afremt op het eind. */
export const countTo = (
  frame: number,
  start: number,
  duration: number,
  to: number,
  from = 0,
) => interpolate(enter(frame, start, duration), [0, 1], [from, to]);

/** Nederlandse notatie: punt als duizendtal, komma als decimaal. */
export const nl = (value: number, decimals = 0) =>
  value.toLocaleString("nl-NL", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });

/** Staggered index-timing: item i start `step` frames na item i-1. */
export const stagger = (index: number, start: number, step: number) =>
  start + index * step;

export { clamp };
