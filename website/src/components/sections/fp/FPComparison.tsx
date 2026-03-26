const ROWS = [
  {
    is: "A premium guide people keep on the kitchen counter",
    isNot: "A coupon book that goes straight to recycling",
  },
  {
    is: "Mailed to new homeowners within their first 60 days",
    isNot: "A mass mailer to 50,000 people who already have a dentist",
  },
  {
    is: "Category-limited: a few spots available per category",
    isNot: "Five plumbers fighting for attention on the same page",
  },
  {
    is: "An editorial recommendation, not a sales pitch",
    isNot: "A Google result buried under 50 competitors",
  },
];

export default function FPComparison() {
  return (
    <section className="bg-white px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-4xl">
        {/* Header row */}
        <div className="mb-6 grid grid-cols-2 gap-6">
          <h3 className="font-comfortaa text-[13px] font-bold uppercase tracking-widest text-fp-sage">
            WHAT THE FRONT PORCH IS
          </h3>
          <h3 className="font-comfortaa text-[13px] font-bold uppercase tracking-widest text-grm-black">
            WHAT IT IS NOT
          </h3>
        </div>

        {/* Rows */}
        <div className="flex flex-col">
          {ROWS.map((row, i) => (
            <div
              key={i}
              className={`grid grid-cols-2 gap-6 px-4 py-5 ${
                i % 2 === 0 ? "bg-grm-cream" : "bg-white"
              }`}
            >
              <p className="font-nunito text-base leading-relaxed text-grm-black">
                {row.is}
              </p>
              <p className="font-nunito text-base leading-relaxed text-grm-black/60">
                {row.isNot}
              </p>
            </div>
          ))}
        </div>

        <p className="mt-10 text-center font-merriweather text-[24px] font-bold text-grm-black">
          It&apos;s yours or it&apos;s theirs.
        </p>
      </div>
    </section>
  );
}
