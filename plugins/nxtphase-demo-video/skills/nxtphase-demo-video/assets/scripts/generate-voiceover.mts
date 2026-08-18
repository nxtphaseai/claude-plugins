/**
 * Genereert de voice-over als ÉÉN doorlopende opname en knipt die daarna op in
 * één mp3 per scene. Draaien vanuit video/sales-video:
 *
 *   npm run voiceover
 *
 * Waarom in één keer: elke API-call is een eigen performance, dus acht losse
 * calls geven acht net iets andere stemmen (toonhoogte, tempo, inzet). Eén call
 * levert één doorlopende lezing op. De knippunten raden we niet: de API geeft
 * per teken een start- en eindtijd terug, dus we knippen precies tussen de
 * laatste klank van de ene scene en de eerste van de volgende.
 *
 * Opties:
 *   --voice=<id>       andere stem (id uit de URL van een stem bij ElevenLabs)
 *   --model=<id>       ander model (standaard eleven_v3)
 *   --tempo=<factor>   spreektempo bij het knippen, 1.0 is onbewerkt
 *   --recut            niet opnieuw genereren, alleen de bewaarde opname opknippen
 *   --dry-run          niets genereren, alleen laten zien wat er zou gebeuren
 *
 * Het tempo zit in de knipstap, niet in de opname: `--recut --tempo=1.0` geeft
 * dus een andere snelheid zonder nieuwe API-kosten.
 *
 * Na afloop meet het script elke scene en drukt het een SCENES-blok af dat bij
 * de opname past, met de animatielengte per scene als ondergrens.
 */
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { FPS, HARD_CUT_AFTER, SCENES, TAIL_S, screenFrames } from "../src/timeline.ts";
import { VOICEOVER } from "../src/voiceover.ts";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
const OUT_DIR = join(ROOT, "public", "voiceover");
/** De onbewerkte opname blijft staan, zodat opnieuw knippen niets kost. */
const TAKE = join(OUT_DIR, "volledige-opname.mp3");

/** Scheiding tussen twee scenes in de aangeboden tekst: een lege regel leest als een beat. */
const SEP = "\n\n";

/**
 * De sleutel staat in de .env van de repo (naast ORQ_API_KEY). Die lezen we hier
 * zelf in, zodat je het script kunt draaien zonder hem in je shell te zetten.
 * Een variabele die al in de omgeving staat, wint.
 */
for (const candidate of [join(ROOT, ".env"), join(ROOT, "..", "..", ".env")]) {
  if (!existsSync(candidate)) continue;
  try {
    process.loadEnvFile(candidate);
  } catch {
    // Een onleesbare .env mag het script niet tegenhouden.
  }
}

const arg = (naam: string) => {
  const found = process.argv.find((a) => a.startsWith(`--${naam}=`));
  return found ? found.slice(naam.length + 3) : undefined;
};

const dryRun = process.argv.includes("--dry-run");
const recut = process.argv.includes("--recut");
/** Onze vaste stem. Niet per project wisselen: dan klinken de video's niet als één reeks. */
const STANDAARD_STEM = "ARIOBKJtltx2F7r1TMzI";
const voiceId = arg("voice") ?? process.env.ELEVENLABS_VOICE_ID ?? STANDAARD_STEM;
const modelId = arg("model") ?? "eleven_v3";
const tempo = Number(arg("tempo") ?? 1.08);

if (!Number.isFinite(tempo) || tempo < 0.5 || tempo > 2) {
  console.error("--tempo moet tussen 0.5 en 2 liggen.");
  process.exit(1);
}

/** Alleen eleven_v3 volgt regie-aanwijzingen op; andere modellen lezen ze voor. */
const supportsTags = modelId === "eleven_v3";
const TAG = /\[[^\]]*\]/g;
const spokenText = (t: string) => t.replace(TAG, " ").replace(/\s+/g, " ").trim();

const getagd = VOICEOVER.filter((l) => TAG.test(l.text)).map((l) => l.id);
TAG.lastIndex = 0;
if (getagd.length && !supportsTags) {
  console.error(
    `Model ${modelId} leest regie-aanwijzingen voor in plaats van ze op te volgen, en die staan ` +
      `in: ${getagd.join(", ")}. Gebruik eleven_v3, of haal de vierkante haakjes uit src/voiceover.ts.`,
  );
  process.exit(1);
}

/**
 * Eén argument dichttimmeren voor de shell die het straks uit elkaar haalt. We
 * quoten altijd, ook als er niets bijzonders in staat: dan is er geen tweede
 * regel die kan afwijken van de eerste.
 *
 * POSIX: binnen enkele quotes is alles letterlijk, backslash incluis. Alleen de
 * enkele quote zelf past er niet in, dus die sluiten we af, zetten we er als
 * '\'' buiten neer, en daarna openen we opnieuw.
 *
 * Windows: cmd.exe kent geen enkele quotes, daar zijn dubbele quotes het enige
 * gereedschap. Binnen die quotes is niets meer bijzonder behalve de dubbele
 * quote zelf; die verdubbelen we, want "" leest als een letterlijke quote en
 * laat cmd zijn quote-stand houden. De backslashes vlak vóór een quote en aan
 * het eind van het argument verdubbelen we ook, anders escapen die alsnog de
 * quote die erop volgt en staat de rest van de regel open voor de shell.
 */
const quote = (p: string) =>
  process.platform === "win32"
    ? `"${p.replace(/(\\*)"/g, '$1$1""').replace(/(\\*)$/, "$1$1")}"`
    : `'${p.replace(/'/g, "'\\''")}'`;

/**
 * Een commando draaien en ALLES teruggeven wat het zegt. ffprobe schrijft zijn
 * informatie naar stderr, niet naar stdout, dus wie alleen stdout leest krijgt
 * niets te zien. Het commando gaat als één string naar de shell, want `npx` is
 * op Windows een .cmd en die start node niet zonder shell.
 */
const run = (parts: string[]) => {
  const r = spawnSync(parts.map(quote).join(" "), { shell: true, encoding: "utf8" });
  return { status: r.status, output: `${r.stdout ?? ""}${r.stderr ?? ""}` };
};

const ffmpeg = (args: string[]) => {
  const r = run(["npx", "remotion", "ffmpeg", ...args]);
  if (r.status !== 0) {
    console.error(r.output.split("\n").slice(-12).join("\n"));
    throw new Error("ffmpeg gaf een fout");
  }
};

/** Lengte van een audiobestand in seconden, via de ffprobe die Remotion meelevert. */
const durationSeconds = (file: string): number | null => {
  const m = run(["npx", "remotion", "ffprobe", file]).output.match(
    /Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)/,
  );
  return m ? Number(m[1]) * 3600 + Number(m[2]) * 60 + Number(m[3]) : null;
};

/**
 * Waar in de aangeboden tekst de eerste en laatste GESPROKEN letter van elke
 * scene staat. De regie-aanwijzingen tellen niet mee: die worden niet
 * uitgesproken, dus knippen we er niet op.
 */
const sceneCharRanges = () => {
  const ranges: { from: number; to: number }[] = [];
  let at = 0;
  VOICEOVER.forEach((line, i) => {
    const t = line.text;
    let from = 0;
    // Voorbij de eventuele aanwijzingen aan het begin.
    for (;;) {
      while (from < t.length && /\s/.test(t[from])) from++;
      if (t[from] === "[") {
        const close = t.indexOf("]", from);
        if (close === -1) break;
        from = close + 1;
        continue;
      }
      break;
    }
    let to = t.length - 1;
    while (to > from && /\s/.test(t[to])) to--;
    ranges.push({ from: at + from, to: at + to });
    at += t.length + (i < VOICEOVER.length - 1 ? SEP.length : 0);
  });
  return ranges;
};

/** Voorstel voor de scenelengtes: spreektijd plus staart, maar nooit korter dan de animatie. */
const suggestScenes = (spoken: (number | null)[]) => {
  console.log("\nVoorstel voor SCENES in src/timeline.ts:");
  let total = 0;
  spoken.forEach((sec, i) => {
    if (sec == null) return;
    const scene = SCENES[i];
    const wanted = Math.round((sec + TAIL_S) * FPS);
    const screen = Math.max(wanted, scene.minScreen);
    const hasTransition = i !== HARD_CUT_AFTER && i !== spoken.length - 1;
    total += screen + (hasTransition ? 12 : 0);
    const reden = screen > wanted ? "animatie" : "stem";
    console.log(
      `  { id: "${scene.id}", duration: ${screen}${hasTransition ? " + T" : ""}, minScreen: ${scene.minScreen} },` +
        `   // ${sec.toFixed(1)}s gesproken, ${reden} bepaalt de lengte`,
    );
  });
  const frames = total - 6 * 12;
  const secs = frames / FPS;
  console.log(`  totaal ${frames} frames = ${Math.floor(secs / 60)}:${String(Math.round(secs) % 60).padStart(2, "0")}`);
};

if (dryRun) {
  console.log(`Model ${modelId}, stem ${voiceId}, tempo ${tempo}\n`);
  VOICEOVER.forEach((line, i) => {
    const tekens = spokenText(line.text).length;
    console.log(`${line.id}: ${tekens} tekens · schatting ${(tekens / 13.5 / tempo).toFixed(1)}s`);
  });
  suggestScenes(VOICEOVER.map((l) => spokenText(l.text).length / 13.5 / tempo));
} else {
  await maak();
}

async function maak() {
  mkdirSync(OUT_DIR, { recursive: true });
  const joined = VOICEOVER.map((l) => l.text).join(SEP);

  let alignment: { characters: string[]; character_end_times_seconds: number[]; character_start_times_seconds: number[] } | null =
    null;

  if (recut) {
    if (!existsSync(TAKE)) {
      console.error(`Geen bewaarde opname op ${TAKE}. Draai eerst zonder --recut.`);
      process.exit(1);
    }
    const cached = join(OUT_DIR, "volledige-opname.alignment.json");
    if (!existsSync(cached)) {
      console.error("De tijdstempels van de vorige opname ontbreken; draai opnieuw zonder --recut.");
      process.exit(1);
    }
    alignment = JSON.parse(readFileSync(cached, "utf8"));
    console.log(`Opnieuw knippen uit ${TAKE}, tempo ${tempo}\n`);
  } else {
    const apiKey = process.env.ELEVENLABS_API_KEY;
    if (!apiKey) {
      console.error("Zet ELEVENLABS_API_KEY (of gebruik --dry-run).");
      process.exit(1);
    }
    console.log(`Model ${modelId}, stem ${voiceId}, tempo ${tempo}`);
    console.log(`Eén opname van ${joined.length} tekens…\n`);

    const response = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}/with-timestamps`,
      {
        method: "POST",
        headers: { "xi-api-key": apiKey, "Content-Type": "application/json" },
        body: JSON.stringify({
          text: joined,
          model_id: modelId,
          voice_settings: supportsTags
            ? { stability: 0.5, similarity_boost: 0.75 }
            : { stability: 0.55, similarity_boost: 0.75, style: 0.15 },
        }),
      },
    );

    if (!response.ok) {
      console.error(`${response.status}: ${await response.text()}`);
      console.error(
        "\nLukt dit model niet met tijdstempels, probeer dan --model=eleven_multilingual_v2 " +
          "(dan moeten de regie-aanwijzingen wel uit src/voiceover.ts).",
      );
      process.exit(1);
    }

    const data = (await response.json()) as {
      audio_base64: string;
      alignment: typeof alignment;
    };
    writeFileSync(TAKE, Buffer.from(data.audio_base64, "base64"));
    if (!data.alignment) {
      console.error("De API gaf geen tijdstempels terug, dus knippen kan niet.");
      process.exit(1);
    }
    alignment = data.alignment;
    writeFileSync(join(OUT_DIR, "volledige-opname.alignment.json"), JSON.stringify(alignment));
    console.log(`Opname bewaard als ${TAKE}`);
  }

  const chars = alignment!.characters;
  if (chars.length !== joined.length) {
    console.error(
      `De tijdstempels dekken ${chars.length} tekens, de tekst is er ${joined.length}. ` +
        "Knippen zou dan op de verkeerde plek gebeuren.",
    );
    process.exit(1);
  }

  const starts = alignment!.character_start_times_seconds;
  const ends = alignment!.character_end_times_seconds;
  const ranges = sceneCharRanges();
  const takeLength = durationSeconds(TAKE) ?? ends[ends.length - 1];

  // Knip halverwege de stilte tussen twee scenes: zo houdt elk fragment een
  // beetje aanloop en uitloop en klinkt de overgang niet afgehakt.
  const cuts = ranges.map((r, i) => {
    const from = i === 0 ? 0 : (ends[ranges[i - 1].to] + starts[r.from]) / 2;
    const to = i === ranges.length - 1 ? takeLength : (ends[r.to] + starts[ranges[i + 1].from]) / 2;
    return { from, to };
  });

  const spoken: (number | null)[] = [];
  cuts.forEach((cut, i) => {
    const target = join(OUT_DIR, `${SCENES[i].id}.mp3`);
    const args = ["-y", "-ss", cut.from.toFixed(3), "-to", cut.to.toFixed(3), "-i", TAKE];
    if (tempo !== 1) args.push("-filter:a", `atempo=${tempo}`);
    args.push("-c:a", "libmp3lame", "-q:a", "2", target);
    ffmpeg(args);
    spoken.push(durationSeconds(target));
    console.log(`${SCENES[i].id}: ${(cut.to - cut.from).toFixed(1)}s geknipt`);
  });

  console.log("\nLengte per scene (gesproken / beschikbaar):");
  let tooLong = 0;
  spoken.forEach((sec, i) => {
    const budget = screenFrames(i) / FPS - 0.4;
    if (sec == null) {
      console.log(`  ${SCENES[i].id}: ? / ${budget.toFixed(1)}s`);
      return;
    }
    const over = sec > budget;
    if (over) tooLong++;
    console.log(
      `  ${SCENES[i].id}: ${sec.toFixed(1)}s / ${budget.toFixed(1)}s` +
        (over ? `  TE LANG met ${(sec - budget).toFixed(1)}s` : ""),
    );
  });
  console.log(
    tooLong
      ? `\n${tooLong} scene(s) te lang. Neem de lengtes hieronder over in src/timeline.ts.`
      : "\nAlles past binnen de huidige scenes.",
  );
  suggestScenes(spoken);
}
