// Hero.jsx — "We make AI work." hero (NL)
const heroAssets = "../../assets";

function Hero({ onContact }) {
  return (
    <section className="hero" id="top">
      <div className="wrap hero-grid">
        <div>
          <h1>We make AI<br/><em>work.</em></h1>
          <p className="lead">Nxt Phase AI helpt mkb+ bedrijven om van AI-ambitie naar echte bedrijfsresultaten te gaan. Geen hype, geen eindeloze pilots. Werkende oplossingen in productie.</p>
          <button className="btn btn-dark" onClick={onContact}>Plan een kennismakingsgesprek <Arrow /></button>
        </div>
        <div className="hero-img">
          <img src={heroAssets + "/images/workspace-1.jpg"} alt="Aan tafel — strategie en uitvoering" />
        </div>
      </div>
    </section>
  );
}

window.Hero = Hero;
