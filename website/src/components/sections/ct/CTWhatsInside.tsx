const ENTRIES = [
  {
    number: "01",
    title: "Cover Story",
    body: "An in-depth feature on one of Marion County\u2019s top-producing agents. Not a puff piece. An honest conversation about how they built their business and what they\u2019ve learned.",
  },
  {
    number: "02",
    title: "Service Company Spotlight",
    body: "Every issue profiles one outstanding service professional and puts them in front of every agent who reads the magazine.",
  },
  {
    number: "03",
    title: "Market Pulse",
    body: "Marion County real estate numbers broken down plainly. Data agents can use in listing presentations the same week it arrives.",
  },
  {
    number: "04",
    title: "Industry Insights",
    body: "One timely article per issue. Legislative changes, market shifts, negotiation strategies. Written for practitioners, not academics.",
  },
];

export default function CTWhatsInside() {
  return (
    <section className="bg-grm-cream px-8 py-12 md:px-20 md:py-20">
      {/* Header */}
      <div className="mx-auto max-w-5xl text-center">
        <p className="font-comfortaa text-[10px] font-bold uppercase tracking-[0.25em] text-grm-teal">
          INSIDE EVERY ISSUE
        </p>
        <div className="mx-auto mt-3.5 h-px w-8 bg-grm-teal" />
      </div>

      {/* Table of contents */}
      <div className="mx-auto mt-14 max-w-5xl">
        {ENTRIES.map((entry, i) => (
          <div key={entry.number}>
            {/* Divider above (except first) */}
            {i > 0 && <div className="h-px w-full bg-grm-teal/20" />}

            <div className="flex flex-col gap-4 py-7 md:flex-row md:items-baseline md:gap-0">
              {/* Number — 15% */}
              <div className="w-full md:w-[15%]">
                <span className="font-merriweather text-[13px] font-bold tracking-[0.2em] text-grm-teal">
                  {entry.number}
                </span>
              </div>

              {/* Content — 85%, split 50/50 */}
              <div className="flex w-full flex-col gap-2 md:w-[85%] md:flex-row md:gap-12">
                <h3 className="w-full font-merriweather text-[20px] font-bold text-grm-black md:w-1/2">
                  {entry.title}
                </h3>
                <p className="w-full font-nunito text-[14px] leading-[1.65] text-grm-black/65 md:w-1/2">
                  {entry.body}
                </p>
              </div>
            </div>
          </div>
        ))}

        {/* Closing rule */}
        <div className="h-px w-full bg-grm-teal/20" />
      </div>
    </section>
  );
}
