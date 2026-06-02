// Footer.jsx
const F = "../../assets";

function Footer() {
  return (
    <footer className="footer">
      <div className="wrap footer-inner panel">
        <img src={F + "/logos/logo-off-black.svg"} alt="Nxt Phase AI" />
        <div className="meta">We make pragmatic AI work. · <a href="#top">nxtphase.ai</a></div>
        <div className="meta">Amsterdam · GDPR-conform · © 2026</div>
      </div>
    </footer>
  );
}

window.Footer = Footer;
