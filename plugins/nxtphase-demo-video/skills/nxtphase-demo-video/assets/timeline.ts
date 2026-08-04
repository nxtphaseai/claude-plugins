/**
 * De tijdlijn van de video, los van React zodat ook een gewoon node-script (bv.
 * een voice-overgenerator) hem kan lezen. Importeer hier niets uit remotion of
 * theme: dat trekt de browserbundel mee.
 */

export const FPS = 30;

/** Lengte van elke overgang tussen twee scenes, in frames. */
export const T = 12;

/**
 * Index van de scene waarna bewust GEEN overgang komt. Na de e-mailassistent
 * springen we hard naar de offertegenerator: dat is een andere tool, en een
 * zachte fade zou suggereren dat het één doorlopend scherm is.
 */
export const HARD_CUT_AFTER = 99; // index van de scene waarna een harde cut komt; 99 = geen

/**
 * Scenelengtes in frames, volgens het goedgekeurde beat sheet. Een scene met
 * een uitgaande overgang krijgt T frames extra, omdat de overgang die frames
 * van de zichtbare tijd afsnoept.
 */
/**
 * `minScreen` is de lengte die de animatie zelf nodig heeft. Komt er een
 * voice-over bij, dan mag een scene langer worden om de zin af te maken, maar
 * nooit korter dan dit. Het generatiescript rekent dat voor je uit.
 */
export const SCENES = [
  // SJABLOON. Vervang dit door de scenes van dit project. `minScreen` is de
  // lengte die de animatie zelf nodig heeft; `duration` mag groter zijn als de
  // voice-over dat vraagt. Het generatiescript rekent dat voor je uit en drukt
  // een voorstel af. Een scene met een uitgaande overgang krijgt T frames extra.
  { id: "scene-01", titel: "Probleem", duration: 250 + T, minScreen: 250 },
  { id: "scene-02", titel: "Kern", duration: 700 + T, minScreen: 700 },
  { id: "scene-03", titel: "Resultaat", duration: 480 + T, minScreen: 480 },
  { id: "scene-04", titel: "Slot", duration: 300, minScreen: 240 },
] as const;

/** Heeft de scene op deze index een uitgaande overgang? */
export const hasTransitionAfter = (i: number): boolean =>
  i < SCENES.length - 1 && i !== HARD_CUT_AFTER;

const TRANSITION_COUNT = SCENES.filter((_, i) => hasTransitionAfter(i)).length;

export const TOTAL_FRAMES =
  SCENES.reduce((sum, s) => sum + s.duration, 0) - TRANSITION_COUNT * T;

/** Startframe van elke scene in de uiteindelijke tijdlijn. */
export const sceneStarts = (): number[] => {
  const starts: number[] = [];
  let at = 0;
  SCENES.forEach((s, i) => {
    starts.push(at);
    at += s.duration - (hasTransitionAfter(i) ? T : 0);
  });
  return starts;
};

/**
 * Hoeveel seconden er per scene te spreken valt. Iets korter dan de scene zelf:
 * een zin die tot de laatste frame doorloopt, loopt hoorbaar door de overgang
 * heen. Nu nog niet gebruikt, maar de schermteksten zijn er wel op getimed
 * zodat er later een voice-over overheen kan zonder de scenes te herbouwen.
 */
export const SPEECH_BUDGET_S = (index: number): number =>
  Math.max(1, (SCENES[index].duration - T) / FPS - 0.6);

/**
 * Stilte na de laatste klank van een scene, zodat een zin niet tegen de
 * overgang aan botst.
 */
export const TAIL_S = 0.45;

/** Zichtbare lengte van een scene, dus zonder de frames die de overgang opeet. */
export const screenFrames = (index: number): number =>
  SCENES[index].duration - (hasTransitionAfter(index) ? T : 0);
