/**
 * Haalt de CSS letterlijk uit de echte app en schrijft die als gescopete
 * stylesheets naar src/styles/. Zo ziet de video er niet "ongeveer" uit als de
 * tools, maar exact: dezelfde regels, dezelfde waarden.
 *
 *   node scripts/extract-styles.mjs
 *
 * Waarom scopen: de taskpane, de editor en de offerte definiëren alle drie
 * :root-variabelen en delen klassenamen. In de video staan ze in één document,
 * dus elke selector krijgt er een scope-klasse voor. De regels zelf worden
 * nooit aangepast.
 *
 * Twee soorten bron:
 *   kind "html" — het <style>-blok uit een zelfstandig HTML-bestand
 *   kind "css"  — een los stylesheet-bestand
 *
 * Overgenomen uit een eerder demo-videoproject en uitgebreid met losse
 * CSS-bestanden.
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = join(HERE, "..", "..", "..");
const OUT_DIR = join(HERE, "..", "src", "styles");

const SOURCES = [
  {
    kind: "html",
    file: join(REPO, "app", "emails", "taskpane.html"),
    scope: "app-addin",
    out: "addin.css",
  },
  {
    kind: "css",
    file: join(REPO, "app", "css", "quote.css"),
    scope: "app-quote",
    out: "quote.css",
  },
  {
    kind: "css",
    file: join(REPO, "app", "css", "editor.css"),
    scope: "app-editor",
    out: "editor.css",
  },
];

/** De <style>-inhoud uit een los HTML-bestand. */
function extractStyle(html) {
  const start = html.indexOf("<style>");
  const end = html.indexOf("</style>", start);
  if (start === -1 || end === -1) throw new Error("geen <style>-blok gevonden");
  return html.slice(start + "<style>".length, end);
}

/**
 * Commentaar eruit vóór het parsen. In de bron-CSS staan toelichtingen met
 * accolades erin; die lopen anders mee in het haakjes-tellen, waardoor de regel
 * erna niet gescopet wordt.
 */
function stripComments(css) {
  return css.replace(/\/\*[\s\S]*?\*\//g, "");
}

/** Splitst op komma's die buiten haakjes staan, zodat :is(a,b) heel blijft. */
function splitSelectors(text) {
  const parts = [];
  let depth = 0;
  let current = "";
  for (const ch of text) {
    if (ch === "(" || ch === "[") depth++;
    else if (ch === ")" || ch === "]") depth--;
    if (ch === "," && depth === 0) {
      parts.push(current);
      current = "";
    } else {
      current += ch;
    }
  }
  parts.push(current);
  return parts.map((p) => p.trim()).filter(Boolean);
}

/**
 * Zet één selector om naar de gescopete variant. `html`, `body` en `:root`
 * slaan op het scope-element zelf; al het andere wordt een nakomeling daarvan.
 */
function scopeSelector(selector, scope) {
  const s = selector.trim();
  if (!s) return s;
  if (s === ":root" || s === "html" || s === "body") return `.${scope}`;
  const rootLike = s.match(/^(?::root|html|body)(?=[.:#[\s>+~])/);
  if (rootLike) return `.${scope}${s.slice(rootLike[0].length)}`;
  if (s === "*") return `.${scope} *`;
  return `.${scope} ${s}`;
}

/** Loopt de stylesheet blok voor blok af en schrijft hem gescopet terug. */
function scopeCss(css, scope) {
  let out = "";
  let i = 0;

  const readBlock = (from) => {
    let depth = 0;
    for (let j = from; j < css.length; j++) {
      if (css[j] === "{") depth++;
      else if (css[j] === "}") {
        depth--;
        if (depth === 0) return j;
      }
    }
    throw new Error("ongebalanceerde accolades in de bron-CSS");
  };

  while (i < css.length) {
    const brace = css.indexOf("{", i);
    if (brace === -1) {
      out += css.slice(i);
      break;
    }
    const prelude = css.slice(i, brace);
    const close = readBlock(brace);
    const body = css.slice(brace + 1, close);
    const trimmed = prelude.trim();

    if (/^@(media|supports|container|layer)/.test(trimmed)) {
      out += `${prelude}{${scopeCss(body, scope)}}`;
    } else if (/^@keyframes/.test(trimmed)) {
      // Naam prefixen zodat twee bronnen met dezelfde animatienaam elkaar niet
      // overschrijven.
      out += `${prelude.replace(/@keyframes\s+([\w-]+)/, `@keyframes ${scope}-$1`)}{${body}}`;
    } else if (trimmed.startsWith("@")) {
      out += `${prelude}{${body}}`;
    } else {
      const selectors = splitSelectors(prelude).map((s) => scopeSelector(s, scope));
      const leading = prelude.match(/^\s*/)[0];
      out += `${leading}${selectors.join(",")}{${body}}`;
    }
    i = close + 1;
  }
  return out;
}

/** Verwijzingen naar hernoemde keyframes meeverhuizen. */
function renameAnimations(css, scope) {
  const names = [...css.matchAll(/@keyframes\s+([\w-]+)/g)].map((m) => m[1]);
  let out = css;
  for (const name of names) {
    const original = name.replace(new RegExp(`^${scope}-`), "");
    if (original === name) continue;
    out = out.replace(
      new RegExp(`(animation(?:-name)?\\s*:[^;}]*?)\\b${original}\\b`, "g"),
      `$1${name}`,
    );
  }
  return out;
}

/**
 * De offerte-CSS verwijst met relatieve paden naar ../assets/. In de video
 * staan die bestanden onder public/, dus de verwijzingen moeten mee.
 */
function rewriteAssetUrls(css) {
  // De bundler lost url() op tijdens het bouwen, vanaf de map van de
  // stylesheet (src/styles/). Daarom een relatief pad naar public/assets/ en
  // geen absoluut pad: dat laatste bestaat op schijf niet.
  return css.replace(/url\((['"]?)\.\.\/assets\//g, "url($1../../public/assets/");
}

mkdirSync(OUT_DIR, { recursive: true });

for (const src of SOURCES) {
  const raw = readFileSync(src.file, "utf8");
  const css = stripComments(src.kind === "html" ? extractStyle(raw) : raw);
  const scoped = rewriteAssetUrls(renameAnimations(scopeCss(css, src.scope), src.scope));

  // Controle: elke regel moet gescopet zijn, anders lekt hij naar de andere app.
  const unscoped = [...scoped.matchAll(/(^|})\s*([^@{}]+)\{/g)]
    .map((m) => m[2].trim())
    .filter((sel) => sel && !sel.split(",").every((s) => s.includes(`.${src.scope}`)));
  if (unscoped.length) {
    console.error(`  LET OP, niet gescopete selectors: ${unscoped.slice(0, 5).join(" | ")}`);
    process.exitCode = 1;
  }
  const header =
    `/* Automatisch gegenereerd door scripts/extract-styles.mjs.\n` +
    `   Bron: ${src.file.replace(REPO, "<repo>")}\n` +
    `   Niet met de hand aanpassen: draai het script opnieuw als de app verandert. */\n`;
  writeFileSync(join(OUT_DIR, src.out), header + scoped, "utf8");
  console.log(`${src.out}: ${scoped.length} tekens, scope .${src.scope}`);
}
