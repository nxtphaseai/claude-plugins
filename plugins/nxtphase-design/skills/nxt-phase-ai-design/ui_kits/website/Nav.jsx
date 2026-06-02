// Nav.jsx — floating pill nav with "Aanpak" dropdown
const A = "../../assets";
const { useState: useNavState, useRef: useNavRef, useEffect: useNavEffect } = React;

const PHASES = [
  { n: "01", t: "Verkennen" },
  { n: "02", t: "Prioriteren" },
  { n: "03", t: "Ontwerpen" },
  { n: "04", t: "Bouwen" },
  { n: "05", t: "Schalen" },
];

function scrollToId(id) {
  const el = document.getElementById(id);
  if (el) window.scrollTo({ top: el.offsetTop - 80, behavior: "smooth" });
}

function Nav({ onContact }) {
  const [open, setOpen] = useNavState(false);
  const ddRef = useNavRef(null);
  useNavEffect(() => {
    const close = (e) => { if (ddRef.current && !ddRef.current.contains(e.target)) setOpen(false); };
    document.addEventListener("click", close);
    return () => document.removeEventListener("click", close);
  }, []);
  return (
    <nav className="nav">
      <div className="wrap nav-inner">
        <img className="nav-logo" src={A + "/logos/logo-off-black.svg"} alt="Nxt Phase AI" />
        <div className="nav-links">
          <button className="nav-link" onClick={() => scrollToId("work")}>Cases</button>
          <div className={"nav-dd" + (open ? " open" : "")} ref={ddRef}>
            <button className="nav-link" onClick={() => setOpen((o) => !o)}>Aanpak <Caret /></button>
            <div className="dd-menu">
              {PHASES.map((p) => (
                <button key={p.n} className="dd-item" onClick={() => { setOpen(false); scrollToId("journey"); }}>
                  <span className="ddn">{p.n}</span><span className="ddt">{p.t}</span>
                </button>
              ))}
            </div>
          </div>
          <button className="nav-link" onClick={() => scrollToId("about")}>Over ons</button>
          <button className="btn btn-dark nav-cta" onClick={onContact}>Plan een gesprek <Arrow /></button>
        </div>
      </div>
    </nav>
  );
}

window.Nav = Nav;
window.scrollToId = scrollToId;
window.PHASES = PHASES;
