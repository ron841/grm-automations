const BLOCKS = [
  {
    title: "Cover Story",
    body: "An in-depth feature on one of Marion County\u2019s top-producing agents. Not a puff piece. An honest conversation about how they built their business and what they\u2019ve learned.",
  },
  {
    title: "Service Company Spotlight",
    body: "Every issue profiles one outstanding service professional and puts them in front of every agent who reads the magazine.",
  },
  {
    title: "Market Pulse",
    body: "Marion County real estate numbers broken down plainly. Data agents can use in listing presentations the same week it arrives.",
  },
  {
    title: "Industry Insights",
    body: "One timely article per issue. Legislative changes, market shifts, negotiation strategies. Written for practitioners, not academics.",
  },
];

export default function CTWhatsInside() {
  return (
    <section className="bg-grm-cream px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-5xl">
        <p className="mb-4 text-center font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
          INSIDE EVERY ISSUE
        </p>
        <div className="mx-auto mb-10 h-[3px] w-10 bg-grm-teal" />

        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2">
          {BLOCKS.map((block) => (
            <div key={block.title} className="rounded-md bg-white p-8">
              <h3 className="mb-3 font-merriweather text-[22px] font-bold text-grm-black">
                {block.title}
              </h3>
              <p className="font-nunito text-base leading-[1.7] text-grm-black">
                {block.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
