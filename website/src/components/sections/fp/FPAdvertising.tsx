export default function FPAdvertising() {
  return (
    <section id="advertising" className="bg-grm-black px-8 py-12 md:px-20 md:py-[72px]">
      <div className="mx-auto flex max-w-7xl flex-col items-start gap-10 md:flex-row md:items-stretch md:gap-0">
        {/* ITEM 1 — 38% */}
        <div className="w-full pr-0 md:w-[38%] md:pr-12">
          <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.25em] text-grm-teal">
            01
          </p>
          <h3 className="mb-3.5 font-merriweather text-[28px] font-bold leading-[1.2] text-white">
            The guide.
          </h3>
          <p className="font-nunito text-[14px] leading-[1.7] text-white/60">
            Your ad in a guide designed to be kept. Premium paper. Clean design.
            Useful content. When the AC breaks in July, they don&apos;t Google.
            They grab The Front Porch.
          </p>
        </div>

        {/* Vertical divider */}
        <div
          className="hidden w-px self-center bg-grm-teal md:block"
          style={{ height: 56 }}
        />

        {/* ITEM 2 — 31% */}
        <div className="w-full pl-0 md:w-[31%] md:pl-12">
          <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.25em] text-grm-teal">
            02
          </p>
          <h3 className="mb-3.5 font-merriweather text-[24px] font-bold leading-[1.2] text-white">
            Category.
          </h3>
          <p className="font-nunito text-[13px] leading-[1.7] text-white/60">
            A few spots available per category, per year. Once a category
            fills, it is closed for the year. The dentist a new family finds in
            month one is probably their dentist for the next decade.
          </p>
        </div>

        {/* Vertical divider */}
        <div
          className="hidden w-px self-center bg-grm-teal md:block"
          style={{ height: 56 }}
        />

        {/* ITEM 3 — 31% */}
        <div className="w-full pl-0 md:w-[31%] md:pl-12">
          <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.25em] text-grm-teal">
            03
          </p>
          <h3 className="mb-3.5 font-merriweather text-[24px] font-bold leading-[1.2] text-white">
            Social.
          </h3>
          <p className="font-nunito text-[13px] leading-[1.7] text-white/60">
            Your ad lands in their mailbox in the first 60 days. Then your
            campaign runs through our social pages every month after that. Seen
            in the guide. Found on their phone. Chosen when they&apos;re ready.
          </p>
        </div>
      </div>
    </section>
  );
}
