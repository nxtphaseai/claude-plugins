// App.jsx — composition
function App() {
  const [contactOpen, setContactOpen] = React.useState(false);
  const openContact = () => {
    setContactOpen(true);
    const el = document.getElementById("contact");
    if (el) window.scrollTo({ top: el.offsetTop, behavior: "smooth" });
  };
  return (
    <React.Fragment>
      <Nav onContact={openContact} />
      <Hero onContact={openContact} />
      <Proof />
      <Journey />
      <Values />
      <Stats />
      <Cases />
      <CTA open={contactOpen} setOpen={setContactOpen} />
      <Footer />
    </React.Fragment>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
