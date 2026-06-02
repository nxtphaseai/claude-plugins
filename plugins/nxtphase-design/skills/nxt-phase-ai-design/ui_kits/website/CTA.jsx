// CTA.jsx — dark closing card with inline contact reveal (NL)
const { useState: useCtaState } = React;

function CTA({ open, setOpen }) {
  const [sent, setSent] = useCtaState(false);
  return (
    <section className="cta" id="contact">
      <div className="wrap">
        <div className="cta-inner">
          <span className="eyebrow-green">Zonder verplichtingen</span>
          {!sent ? (
            <React.Fragment>
              <h2>Klaar om de eerste stap te zetten?</h2>
              <p>Vertel ons waar jullie staan. We denken graag mee over de beste volgende stap — plan een gesprek of stuur ons een bericht.</p>
              {!open ? (
                <div className="cta-ctas">
                  <button className="btn btn-green" onClick={() => setOpen(true)}>Plan een gesprek <Arrow /></button>
                  <button className="btn btn-ghost" onClick={() => setOpen(true)}>Stuur een bericht</button>
                </div>
              ) : (
                <form className="contact" onSubmit={(e) => { e.preventDefault(); setSent(true); }}>
                  <input placeholder="Naam" required />
                  <input placeholder="Werk e-mail" type="email" required />
                  <textarea className="full" placeholder="Waar staan jullie met AI vandaag?"></textarea>
                  <div className="full" style={{ textAlign: "center" }}><button className="btn btn-green" type="submit">Verstuur bericht <Arrow /></button></div>
                </form>
              )}
            </React.Fragment>
          ) : (
            <div className="sent">
              Bedankt — we nemen binnen één werkdag contact op.
              <span className="mut">koen@nxtphase.ai · +31 6 1234 5678</span>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

window.CTA = CTA;
