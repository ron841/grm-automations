const STATS = [
  { number: "500", label: "Marion County\u2019s top real estate service companies per issue" },
  { number: "350", label: "Marion County top producers, verified from Stellar MLS transaction data" },
  { number: "150", label: "Sumter County and The Villages top producers" },
  { number: "$2.8B", label: "In annual Marion County home sales volume" },
  { number: "12", label: "Issues per year" },
];

export default function CTWhyThisWorks() {
  return (
    <section className="bg-white px-6 py-20 lg:px-8">
      <div className="mx-auto grid max-w-5xl grid-cols-1 gap-12 lg:grid-cols-5">
        {/* Left column — copy (60%) */}
        <div className="lg:col-span-3">
          <p className="mb-4 font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
            WHY THIS WORKS
          </p>
          <div className="mb-6 h-[3px] w-10 bg-grm-teal" />

          <h2 className="mb-6 font-merriweather text-[32px] font-bold leading-tight text-grm-black">
            These are the people who control $2.8 billion in annual home sales.
          </h2>

          <p className="font-nunito text-base leading-[1.7] text-grm-black">
            If you&apos;re a lender, title company, inspector, or photographer,
            this is the only publication that reaches both sides of the referral
            relationship. When a top agent sees your name next to a cover story
            about one of their peers, you&apos;re not cold-calling anymore.
            You&apos;re already known.
          </p>
        </div>

        {/* Right column — stat stack (40%) */}
        <div className="lg:col-span-2">
          <div className="flex flex-col gap-6">
            {STATS.map((stat) => (
              <div
                key={stat.label}
                className="border-l-[3px] border-grm-teal pl-5"
              >
                <p className="font-merriweather text-4xl font-bold text-grm-teal">
                  {stat.number}
                </p>
                <p className="mt-1 font-nunito text-[13px] text-grm-black/60">
                  {stat.label}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
