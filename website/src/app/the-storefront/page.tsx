import type { Metadata } from "next";
import PreviewIntakeForm from "@/components/forms/PreviewIntakeForm";
import "./landing-tokens.css";
import "./landing.css";

export const metadata: Metadata = {
  title: "The Storefront — Websites built to be recommended by AI | Get Rooted Media",
  description:
    "The Storefront: a website that the AI actually recommends. For Marion County contractors. $1,000 to build, $150 a month to keep sharp. Live in 14 days.",
  alternates: {
    canonical: "https://getrootedmedia.com/the-storefront",
  },
  openGraph: {
    title: "The Storefront — Websites built to be recommended by AI",
    description:
      "For Marion County contractors. $1,000 to build, $150 a month. Live in 14 days.",
    type: "website",
    url: "https://getrootedmedia.com/the-storefront",
    siteName: "Get Rooted Media",
  },
  twitter: {
    card: "summary_large_image",
  },
};

const schema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Service",
      "@id": "https://getrootedmedia.com/the-storefront#service",
      "name": "The Storefront",
      "provider": {
        "@type": "LocalBusiness",
        "name": "Get Rooted Media LLC",
        "telephone": "+1-352-598-7289",
        "email": "ron@getrootedmedia.com",
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "Ocala",
          "addressRegion": "FL",
          "addressCountry": "US",
        },
        "areaServed": "Marion County, FL",
      },
      "serviceType":
        "Website design and development for home-services contractors",
      "offers": [
        {
          "@type": "Offer",
          "name": "Setup",
          "price": "1000",
          "priceCurrency": "USD",
        },
        {
          "@type": "Offer",
          "name": "Monthly",
          "price": "150",
          "priceCurrency": "USD",
          "priceSpecification": {
            "@type": "UnitPriceSpecification",
            "billingIncrement": 1,
            "unitText": "MONTH",
          },
        },
      ],
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Will my site show up on Google?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text":
              "Yes. Every site we build ships server-rendered and fast, with clean structure Google can read on the first crawl. We set up your local signals for Ocala and Marion County so you rank for the work you do in the towns you serve.",
          },
        },
        {
          "@type": "Question",
          "name": "What is the difference between SEO and getting recommended by AI?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text":
              "SEO gets you ranked on Google. AI recommendation gets you quoted by ChatGPT and other assistants when someone asks for the best in your trade. Both run on the same foundation: clean code, clear facts, and structured data. We build for both at once.",
          },
        },
        {
          "@type": "Question",
          "name": "Why custom Next.js instead of Wix, Squarespace, or WordPress?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text":
              "Drag-and-drop builders bury your content in heavy code that loads slow and reads messy. Custom Next.js gives you faster pages, cleaner markup, and the schema AI engines look for. A template cannot match that.",
          },
        },
        {
          "@type": "Question",
          "name": "What does The Storefront cost?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text":
              "A flat $1,000 to build, due at signing. Then $150 a month for hosting, updates, AI citation monitoring, and a scheduled content refresh. No retainers. No upsells.",
          },
        },
        {
          "@type": "Question",
          "name": "Can I see it before I pay?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text":
              "Yes. We build a free preview of your homepage within 7 days. If you like it, we migrate it to your domain. If you do not, nothing changes and you keep the wireframe.",
          },
        },
      ],
    },
  ],
};

export default function WebPage() {
  return (
    <main className="web-landing">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      />

      {/* ============ 1. HERO (cream) ============ */}
      <section className="hero sec--cream" data-screen-label="01 Hero">
        <div className="container">
          <div className="eb">— Get Rooted Media &nbsp;·&nbsp; Web Services &nbsp;·&nbsp; Marion County</div>
          <div className="pubmark" style={{ marginTop: 18 }}>
            <span className="the">The</span>
            <span className="title">Storefront.</span>
          </div>
          <div className="dek">We build it. We host it. We update it.<br />You answer the phone.</div>
          <div className="rule"></div>

          <div className="opener">
            <p className="lede">
              <span className="drop">A</span> Belleview homeowner with a burst pipe at 9 PM does not open Google and scroll past four ads. They ask ChatGPT. The assistant reads a handful of plumber websites, picks one, and hands them a name and a phone number.
            </p>
            <p className="lede">They call that number. Almost zero chance it was yours.</p>
            <p className="lede">That is not a prediction. That is how local search works in 2026. The numbers tell the rest of the story.</p>
          </div>

          <div className="stats">
            <div className="stat">
              <div className="num">527%</div>
              <div className="dk">Year-over-year growth in AI-referred visits to business websites.</div>
              <div className="src">SE Ranking GEO research, 2025–2026</div>
            </div>
            <div className="stat">
              <div className="num">1.2%</div>
              <div className="dk">Of home-services locations currently recommended by ChatGPT for local queries.</div>
              <div className="src">BrightLocal, 2026</div>
            </div>
            <div className="stat">
              <div className="num">17%</div>
              <div className="dk">Overlap between AI-cited URLs and Google Page 1 organic results.</div>
              <div className="src">Ziff Davis analysis, 2026</div>
            </div>
            <div className="stat">
              <div className="num">44.2%</div>
              <div className="dk">Of AI citations pulled from the first 30% of the page.</div>
              <div className="src">SE Ranking GEO research, 2026</div>
            </div>
          </div>
        </div>
      </section>

      {/* ============ 2. THE SHIFT (black) ============ */}
      <section className="shift sec--black" data-screen-label="02 Shift">
        <div className="container">
          <div className="head">
            <div className="eb">— Section 01 &nbsp;·&nbsp; The shift</div>
            <h2>The old game is a decade long.<br />The new game starts on day one.</h2>
          </div>

          <div className="body">
            <div>
              <p>The old SEO game takes a decade. A plumber who set up a WordPress site in 2015 and spent ten years collecting backlinks from HomeAdvisor, Angi, Yelp, and the local paper has a moat on Google. That moat took ten years to dig.</p>
              <p>The new game starts fresh the morning your site goes live. AI assistants do not care about backlinks. They do not care about domain age.</p>
            </div>
            <div>
              <p>They care about schema markup, fact density in the first paragraph, and whether their crawlers are allowed in at all. All of that ships on day one of a well-built site.</p>
              <p>And the assistant picks one contractor per query. One. Not ten. If your site is not the one it picks, you do not get a second chance on that search.</p>
            </div>
          </div>

          <div className="pull">
            <span className="mark" aria-hidden="true">&ldquo;</span>
            <span className="body">Your competitor&apos;s ten-year Google moat is worth <em>nothing</em> in this new game.</span>
            <div className="tail">The first contractor in Marion County to ship a site built for AI citation owns that query for years.</div>
          </div>
        </div>
      </section>

      {/* ============ 3. THE DIAGNOSIS (cream) ============ */}
      <section className="diagnosis sec--cream" data-screen-label="03 Diagnosis">
        <div className="container">
          <div className="eb">— Section 02 &nbsp;·&nbsp; The diagnosis</div>
          <h2>Every Marion County contractor site we look at has the same three holes.</h2>

          <ol className="holes">
            <li>
              <div className="n">01</div>
              <div>
                <div className="ft">No schema markup.</div>
                <div className="dk">The AI has to guess what trade you run, what you charge, where you work, and whether you are trustworthy. It usually guesses wrong or gives up.</div>
              </div>
            </li>
            <li>
              <div className="n">02</div>
              <div>
                <div className="ft">Marketing filler where the facts should be.</div>
                <div className="dk">Your homepage opens with &ldquo;we pride ourselves on quality work&rdquo; or similar. The AI needs your license number, years in business, service area, review count, and phone. Those are almost always missing from the first paragraph.</div>
              </div>
            </li>
            <li>
              <div className="n">03</div>
              <div>
                <div className="ft">AI crawlers blocked by accident.</div>
                <div className="dk">WordPress security plugins quietly return a 403 error to GPTBot, ClaudeBot, and PerplexityBot. Your site is invisible to them not by choice. By default.</div>
              </div>
            </li>
          </ol>
        </div>
      </section>

      {/* ============ 4. THIRTY-SECOND TEST (teal) ============ */}
      <section className="test-sec sec--teal" data-screen-label="04 Thirty-second test">
        <div className="container">
          <div className="test">
            <div className="eb">— Thirty-second test</div>
            <div className="head">Pull out your phone. Open ChatGPT. Ask: <em>&ldquo;Best [your trade] in Ocala.&rdquo;</em></div>
            <div className="tail">If your name is not the one it hands back, we should talk.</div>
            <div className="cta-row">
              <a className="cta" href="#preview" data-cta="test-preview">Get my free preview →</a>
              <span className="meta">
                Or call us:{" "}
                <a
                  href="tel:3525987289"
                  style={{
                    color: "#fff",
                    textDecoration: "underline",
                    textDecorationColor: "rgba(255,255,255,0.5)",
                  }}
                >
                  (352) 598-7289
                </a>
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* ============ 5. WHAT WE SHIP (cream) ============ */}
      <section className="ship sec--cream" data-screen-label="05 What we ship">
        <div className="container">
          <div className="eb">— Section 03 &nbsp;·&nbsp; The fix</div>
          <h2>
            <span className="line">What we</span>
            <span className="line">ship <span className="teal"><em>on day one.</em></span></span>
          </h2>
          <p className="lede">Every Get Rooted Media site ships with the AI citation playbook built in. You do not ask for it. You do not pay extra. It is what we build.</p>

          <ol className="ships">
            <li>
              <div className="n">01</div>
              <div>
                <div className="ft">Trade-specific Schema.org markup.</div>
                <div className="dk">Plumber, Electrician, RoofingContractor. Not a generic tag.</div>
              </div>
            </li>
            <li>
              <div className="n">02</div>
              <div>
                <div className="ft">FAQPage schema on every service page.</div>
                <div className="dk">The single strongest predictor of AI citation we have measured.</div>
              </div>
            </li>
            <li>
              <div className="n">03</div>
              <div>
                <div className="ft">Fact-dense first paragraph.</div>
                <div className="dk">License number, years in business, cities served, review count, phone. Every line is a citation anchor.</div>
              </div>
            </li>
            <li>
              <div className="n">04</div>
              <div>
                <div className="ft">Every AI crawler allowed.</div>
                <div className="dk">GPTBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Bingbot, Googlebot. No plugin in the way.</div>
              </div>
            </li>
            <li>
              <div className="n">05</div>
              <div>
                <div className="ft">Images in WebP and AVIF.</div>
                <div className="dk">Your site loads in under two seconds on a phone. PageSpeed above 90.</div>
              </div>
            </li>
            <li>
              <div className="n">06</div>
              <div>
                <div className="ft">Scheduled content refresh.</div>
                <div className="dk">Every thirteen weeks we update your review counts, rotate a seasonal FAQ, and swap a project photo. AI assistants read that as freshness, and freshness earns citations.</div>
              </div>
            </li>
          </ol>
        </div>
      </section>

      {/* ============ 5b. SEO + GEO (teal) ============ */}
      <section className="seo sec--teal" data-screen-label="5b Found everywhere">
        <div className="container">
          <div className="eb">— Found everywhere</div>
          <h2>FOUND ON GOOGLE.<br />CITED BY AI.</h2>
          <div className="body">
            <div>
              <p>Most local websites sit invisible. Yours will not. Every page we build ships with the foundation Google rewards: server-rendered HTML that crawls clean, load times that pass Core Web Vitals, and structured data that tells search engines exactly who you are and where you work.</p>
              <p>We tune the local signals for Ocala and Marion County, so your business shows up when a neighbor searches for what you do.</p>
            </div>
            <div>
              <p>Search is splitting in two. People ask Google. They ask AI. We build for both.</p>
              <p>Clean structure and direct answers make your site easy for Google to rank and easy for AI engines to quote. One site, found everywhere your customers look.</p>
            </div>
          </div>
          <div className="buildline">This runs on custom Next.js code, not a drag-and-drop template. You get faster pages, cleaner markup, and search performance a website builder cannot match.</div>
        </div>
      </section>

      {/* ============ 6. PRICING (black) ============ */}
      <section className="pricing sec--black" data-screen-label="06 Pricing">
        <div className="container">
          <div className="eb">— What it costs</div>
          <h2>Flat rates. No retainers. No upsells.</h2>
          <div className="price-grid">
            <div className="p">
              <div className="lbl">— Setup, one-time</div>
              <div className="num">$1,000</div>
              <div className="sub">Due at signing. Live in 14 days. Includes schema, copywriting, photography review, migration.</div>
            </div>
            <div className="p">
              <div className="lbl">— Then, monthly</div>
              <div className="num">$150 <span className="mo">/ mo</span></div>
              <div className="sub">Hosting, updates, AI citation monitoring, scheduled content refresh, real humans on the phone.</div>
            </div>
          </div>
        </div>
      </section>

      {/* ============ 7. THE PREVIEW + INTAKE (teal) ============ */}
      <section className="preview sec--teal" id="preview" data-screen-label="07 Preview">
        <div className="container">
          <div className="eb">— The Preview</div>
          <div className="head">
            <span className="word">Free.</span>
            <span className="word">Yours in <em>7 days.</em></span>
            <span className="word">Before you sign anything.</span>
          </div>
          <p className="body">We build a preview of your new homepage. You see the schema, the fact-dense opener, the way ChatGPT will read it. If you like it, we migrate it to your domain. If you do not, nothing changes and you keep the wireframe.</p>

          <div className="intake">
            <h3>Request your free preview.</h3>
            <p className="note">Three fields. No call required yet. We review every submission personally.</p>
            <PreviewIntakeForm />
          </div>
        </div>
      </section>

      {/* ============ 8. SIGN-OFF + DUAL CTA (cream) ============ */}
      <section className="signoff sec--cream" id="book" data-screen-label="08 Sign-off">
        <div className="container">
          <div className="ron">
            <div className="eb">— Sign-off</div>
            <h2>We built Get Rooted Media out of Ocala because Marion County is full of good contractors whose phones ought to ring more than they do.</h2>
            <p>The ones who unlock the shop at 6:45, load the truck by seven, and run next week&apos;s numbers at the kitchen table on Sunday. If that is your phone, this is the fix.</p>
            <div className="tag">Locally rooted. Professionally grown.</div>
          </div>

          <div className="dual-cta">
            <a className="side" href="tel:3525987289" data-cta="footer-phone">
              <span className="eb">— Call us</span>
              <span className="num">(352) 598-7289</span>
              <span className="sub">Truck-friendly. Leave a voicemail if it rings.</span>
            </a>
            <div className="divider">OR</div>
            <a className="side dark" href="https://cal.com/ron-kolb-cdlgsw/30min" data-cta="footer-book">
              <span className="eb">— Book online</span>
              <span className="num">15 minutes →</span>
              <span className="sub">cal.com/ron-kolb-cdlgsw</span>
            </a>
          </div>
        </div>
      </section>

      {/* ============ 8b. FAQ (black) ============ */}
      <section className="faq sec--black" id="faq" data-screen-label="8b FAQ">
        <div className="container">
          <div className="eb">— Common questions</div>
          <h2>Questions contractors ask before they sign.</h2>
          <div className="qa">
            <div className="item">
              <div className="q">Will my site show up on Google?</div>
              <div className="a">Yes. Every site we build ships server-rendered and fast, with clean structure Google can read on the first crawl. We set up your local signals for Ocala and Marion County so you rank for the work you do in the towns you serve.</div>
            </div>
            <div className="item">
              <div className="q">What is the difference between SEO and getting recommended by AI?</div>
              <div className="a">SEO gets you ranked on Google. AI recommendation gets you quoted by ChatGPT and other assistants when someone asks for the best in your trade. Both run on the same foundation: clean code, clear facts, and structured data. We build for both at once.</div>
            </div>
            <div className="item">
              <div className="q">Why custom Next.js instead of Wix, Squarespace, or WordPress?</div>
              <div className="a">Drag-and-drop builders bury your content in heavy code that loads slow and reads messy. Custom Next.js gives you faster pages, cleaner markup, and the schema AI engines look for. A template cannot match that.</div>
            </div>
            <div className="item">
              <div className="q">What does The Storefront cost?</div>
              <div className="a">A flat $1,000 to build, due at signing. Then $150 a month for hosting, updates, AI citation monitoring, and a scheduled content refresh. No retainers. No upsells.</div>
            </div>
            <div className="item">
              <div className="q">Can I see it before I pay?</div>
              <div className="a">Yes. We build a free preview of your homepage within 7 days. If you like it, we migrate it to your domain. If you do not, nothing changes and you keep the wireframe.</div>
            </div>
          </div>
        </div>
      </section>

      {/* ============ 9. SOURCES STRIP (cream, thin) ============ */}
      <section className="sources-strip sec--cream" data-screen-label="09 Sources">
        <div className="container">
          <div className="sources-row">
            <div className="lbl">— Research + Sources</div>
            <div className="body">SE Ranking GEO research on AI citation patterns and content freshness · BrightLocal research on AI recommendations for local services · Ziff Davis analysis of AI-cited URLs vs. Google Page 1 organic · OpenAI GPTBot &amp; Anthropic Claude crawler documentation · Schema.org type hierarchy &amp; Google structured-data docs · Answer.AI llms.txt specification (llmstxt.org).</div>
          </div>
        </div>
      </section>
    </main>
  );
}
