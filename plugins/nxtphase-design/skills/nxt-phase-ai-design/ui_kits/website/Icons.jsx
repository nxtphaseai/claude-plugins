// Icons.jsx — minimal UI glyphs (diagonal arrow affordance used on CTAs)
function Arrow({ className }) {
  return (
    <svg className={className || "arr"} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 12L12 4" /><path d="M5.5 4H12V10.5" />
    </svg>
  );
}
function Caret({ className }) {
  return (
    <svg className={className || "caret"} viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2.5 4.5L6 8l3.5-3.5" />
    </svg>
  );
}
window.Arrow = Arrow;
window.Caret = Caret;
