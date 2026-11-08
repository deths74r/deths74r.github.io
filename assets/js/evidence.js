// Keep evidence notes folded until a reader follows a reference or opens one.
(() => {
  function revealEvidence() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    if (!/^evidence-(?:ref-)?[0-9]+$/.test(id)) return;
    const target = document.getElementById(id);
    if (!target) return;
    const note = target.closest("details.evidence-box");
    if (note) note.open = true;
    target.scrollIntoView({ block: "start" });
    const focusTarget = note ? note.querySelector("summary") : target;
    focusTarget.focus({ preventScroll: true });
  }
  document.addEventListener("click", event => {
    const link = event.target.closest("a.evidence-ref, a.evidence-backlink");
    if (!link || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const href = link.getAttribute("href");
    if (!href || !document.getElementById(href.slice(1))) return;
    event.preventDefault();
    history.pushState(null, "", href);
    revealEvidence();
  });
  window.addEventListener("hashchange", revealEvidence);
  revealEvidence();
})();
