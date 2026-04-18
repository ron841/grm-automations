// Shared nav + footer + soil strata injected into every page.
window.OXF = window.OXF || {};

OXF.nav = function (active) {
  return `
  <nav class="nav">
    <div class="nav-inner">
      <a class="nav-logo" href="index.html">
        <span class="mark" aria-hidden="true"></span>
        Oxford <em>Lawn</em>
      </a>
      <ul class="nav-list">
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="services.html">Services</a></li>
        <li><a href="process.html">Process</a></li>
        <li><a href="gallery.html">Gallery</a></li>
        <li><a href="reviews.html">Reviews</a></li>
        <li><a href="contact.html">Contact</a></li>
        <li><a href="library.html" style="color:var(--lawn-700);">⌘ Library</a></li>
        <li><a href="mobile.html" style="color:var(--lawn-700);">⌘ Mobile</a></li>
        <li><a href="gap-catalog.html" style="color:var(--lawn-700);">⌘ Gap</a></li>
        <li><a href="typographic-classes.html" style="color:var(--lawn-700);">⌘ Type</a></li>
        <li><a href="soil-cross-section-references.html" style="color:var(--lawn-700);">⌘ Soil</a></li>
      </ul>
      <a class="nav-phone" href="tel:+13524463497">
        <b>Call</b> (352) 446-3497
      </a>
    </div>
  </nav>`;
};

OXF.strata = function () {
  return `
  <div class="strata" aria-hidden="true">
    <div style="display:grid;grid-template-columns:0.6fr 1.6fr 1fr 1.2fr 0.7fr;">
      <div class="layer l-thatch">Thatch · 0–1"</div>
      <div class="layer l-grass">Living grass</div>
      <div class="layer l-roots">Root zone · 1–4"</div>
      <div class="layer l-compost">Compost / loam · 4–8"</div>
      <div class="layer l-subsoil">Subsoil</div>
    </div>
  </div>`;
};

OXF.footer = function () {
  return `
  <footer class="foot">
    <div class="wrap">
      <div class="foot-grid">
        <div>
          <div style="font-family:var(--f-display);font-size:1.8rem;line-height:1;">Oxford <em style="color:var(--lawn-500);font-style:italic;">Lawn</em></div>
          <p style="margin-top:1rem;max-width:32ch;opacity:0.85;">Organic lawn restoration. Based in Wildwood, Florida, working across Sumter, Lake, and Marion County since 2008.</p>
          <div style="margin-top:1.25rem;font-family:var(--f-mono);font-size:0.7rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--lawn-500);">Soil driven. Earth approved.</div>
        </div>
        <div>
          <h4>The Rehab</h4>
          <ul class="foot-list">
            <li><a href="process.html#dethatch">Dethatching</a></li>
            <li><a href="process.html#aerate">Core aeration</a></li>
            <li><a href="process.html#compost">Compost top-dressing</a></li>
            <li><a href="services.html">Full services</a></li>
            <li><a href="gallery.html">Project gallery</a></li>
          </ul>
        </div>
        <div>
          <h4>Service area</h4>
          <ul class="foot-list">
            <li>The Villages</li>
            <li>Wildwood</li>
            <li>Oxford &amp; Summerfield</li>
            <li>Ocala (South)</li>
            <li>Leesburg &amp; Fruitland Park</li>
            <li>Lady Lake &amp; Clermont</li>
          </ul>
        </div>
        <div>
          <h4>Direct</h4>
          <ul class="foot-list">
            <li><a href="tel:+13524463497">(352) 446-3497</a></li>
            <li><a href="mailto:Tom@oxfordlawn.com">Tom@oxfordlawn.com</a></li>
            <li>4656 County Road 502<br>Wildwood, FL 34785</li>
            <li>Mon–Fri · 8am – 6pm</li>
            <li><a href="contact.html">Free on-site assessment</a></li>
          </ul>
        </div>
      </div>
      <div class="foot-bottom">
        <div>© 2026 Oxford Lawn · Owner Tom O'Brien · Est. 2008</div>
        <div>A GRM ceiling concept · Design direction, April 2026</div>
      </div>
    </div>
  </footer>`;
};

// Inject on load
document.addEventListener('DOMContentLoaded', () => {
  const navHost = document.getElementById('nav-host');
  const footHost = document.getElementById('foot-host');
  if (navHost) navHost.innerHTML = OXF.nav();
  if (footHost) footHost.innerHTML = OXF.footer();
});
