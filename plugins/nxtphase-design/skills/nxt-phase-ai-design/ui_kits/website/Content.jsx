// Content.jsx — Proof, Journey, Values, Stats, Cases (NL)
const C = "../../assets";
const { useState: useContentState } = React;

const CLIENTS = ["ANP", "KLAFS", "Triferto", "ARAG", "begra", "RITUALS", "KeyGene", "nha", "MCB", "Veldhuis"];

function Proof() {
  return (
    <section className="proof">
      <div className="wrap">
        <div className="panel proof-inner">
          <div>
            <span className="eyebrow-green">Vertrouwd door</span>
            <h2><span className="g">20+</span> Bedrijven gingen je voor.</h2>
          </div>
          <div className="logos">
            {CLIENTS.map((c) => <span className="lg" key={c}>{c}</span>)}
          </div>
        </div>
      </div>
    </section>
  );
}

const PHASE_DETAIL = [
  { n: "01", t: "Verkennen", b: "Een eerlijk beeld van wat AI voor jullie kan doen. We starten bij jullie team." },
  { n: "02", t: "Prioriteren", b: "We meten waar AI het meeste verschil maakt. Dan kiezen we waar we beginnen." },
  { n: "03", t: "Ontwerpen", b: "We ontwerpen de oplossing rond jullie proces — niet andersom." },
  { n: "04", t: "Bouwen", b: "Senior delivery, geen slideware. Werkende systemen in jullie stack." },
  { n: "05", t: "Schalen", b: "AI die in productie leeft — gemeten, onderhouden en verbeterd." },
];

function Journey() {
  const [active, setActive] = useContentState(1);
  return (
    <section className="journey" id="journey">
      <div className="wrap">
        <div className="shead">
          <span className="eyebrow-green">Vijf fases</span>
          <h2>Waar staan jullie in je AI-reis?</h2>
          <p>Elke organisatie zit ergens. Herken je jezelf in één van deze fases? Wij sluiten aan op waar jullie staan.</p>
        </div>
        <div className="phase-row">
          {PHASE_DETAIL.map((p, i) => (
            <div key={p.n} className={"phase" + (i === active ? " active" : "")}
              onMouseEnter={() => setActive(i)} onClick={() => setActive(i)}>
              <div className="pn">{p.n}</div>
              <h3>{p.t}</h3>
              <p>{p.b}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

const VALUES = [
  { t: "AI zonder hype.", b: "We houden het eerlijk en praktisch. Helder advies over wat realistisch is — en wat niet.", icon: "icon-a", bg: "var(--surface-2)" },
  { t: "Waarde eerst.", b: "Eerst meten waar AI het meeste verschil maakt. Dan bouwen wat écht werkt.", icon: "icon-b", bg: "var(--soft-mint)" },
  { t: "Proces vóór technologie.", b: "We beginnen bij het proces, niet bij de tool. Dan kijken we waar automatisering iets toevoegt.", icon: "icon-c", bg: "var(--soft-peach)" },
  { t: "Eén team.", b: "Geen overdracht tussen consultants en developers. Wij zijn verantwoordelijk voor het eindresultaat.", icon: "icon-d", bg: "var(--postit-blue)" },
];

function Values() {
  return (
    <section className="values" id="about">
      <div className="wrap">
        <div className="shead">
          <span className="eyebrow-green">Waarom Nxt Phase</span>
          <h2>Vier kerntrekken.</h2>
        </div>
        <div className="value-grid">
          {VALUES.map((v) => (
            <div className="value" key={v.t}>
              <div className="vtile" style={{ background: v.bg }}><img src={C + "/icons/" + v.icon + ".svg"} alt="" /></div>
              <div><h3>{v.t}</h3><p>{v.b}</p></div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Stats() {
  return (
    <section className="stats">
      <div className="wrap">
        <div className="panel stats-inner">
          <div className="stat"><div className="num">20<em>+</em></div><div className="lab">klanten in productie</div></div>
          <div className="stat"><div className="num">15<em>+</em></div><div className="lab">jaar AI- en strategie-ervaring</div></div>
          <div className="stat"><div className="num">100<em>%</em></div><div className="lab">NL-based · GDPR-conform</div></div>
        </div>
      </div>
    </section>
  );
}

const CASES = [
  { img: "/images/workspace-2.jpg", tag: "MCB Staalhandel · Wholesale", t: "Tijd tot waarde: 8 weken.", b: "AI rechtstreeks in Outlook en SAP. Leest orders, haalt gegevens eruit, verwerkt e-mails automatisch." },
  { img: "/images/still-life-2.jpg", tag: "NHA Opleidingen · Education", t: "Sneller, consistenter, altijd beschikbaar.", b: "AI neemt de feitelijke beoordeling van duizenden examenvragen over. Constanter, sneller, schaalbaar." },
];

function Cases() {
  return (
    <section className="cases" id="work">
      <div className="wrap">
        <div className="shead">
          <span className="eyebrow-green">Bewijs in de praktijk</span>
          <h2>Resultaten die tellen.</h2>
          <p>Van strategie naar productie, met meetbare impact.</p>
        </div>
        <div className="case-grid">
          {CASES.map((c) => (
            <article className="case" key={c.tag}>
              <div className="ph"><img src={C + c.img} alt="" /></div>
              <div className="body">
                <div className="tag eyebrow-green">{c.tag}</div>
                <h3>{c.t}</h3>
                <p>{c.b}</p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { Proof, Journey, Values, Stats, Cases });
