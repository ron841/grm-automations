export default function HomeHowItWorks() {
  return (
    <section className="bg-grm-black px-8 py-12 md:px-20 md:py-[72px]">
      <div className="mx-auto flex max-w-7xl flex-col items-start gap-10 md:flex-row md:items-stretch md:gap-0">
        {/* ITEM 1 — 40% */}
        <div className="w-full pr-0 md:w-[40%] md:pr-12">
          <p className="mb-4 font-merriweather text-[11px] font-bold uppercase tracking-[0.3em] text-grm-teal">
            01
          </p>
          <h3 className="mb-4 font-merriweather text-[28px] font-bold leading-[1.2] text-white">
            Print opens the door.
          </h3>
          <p className="font-nunito text-[14px] leading-[1.7] text-white/65">
            Your business in a premium magazine that top agents and new
            homeowners actually read, share, and keep.
          </p>
        </div>

        {/* Vertical divider */}
        <div className="hidden w-px self-center bg-grm-teal md:block" style={{ height: 60 }} />

        {/* ITEM 2 — 30% */}
        <div className="w-full pl-0 md:w-[30%] md:pl-12">
          <p className="mb-4 font-merriweather text-[11px] font-bold uppercase tracking-[0.3em] text-grm-teal">
            02
          </p>
          <h3 className="mb-4 font-merriweather text-[24px] font-bold leading-[1.2] text-white">
            Digital keeps it open.
          </h3>
          <p className="font-nunito text-[13px] leading-[1.7] text-white/65">
            Your campaign extends through our social pages. Our audience. Your
            business. Third-party credibility no ad buy can replicate.
          </p>
        </div>

        {/* Vertical divider */}
        <div className="hidden w-px self-center bg-grm-teal md:block" style={{ height: 60 }} />

        {/* ITEM 3 — 30% */}
        <div className="w-full pl-0 md:w-[30%] md:pl-12">
          <p className="mb-4 font-merriweather text-[11px] font-bold uppercase tracking-[0.3em] text-grm-teal">
            03
          </p>
          <h3 className="mb-4 font-merriweather text-[24px] font-bold leading-[1.2] text-white">
            Community makes it last.
          </h3>
          <p className="font-nunito text-[13px] leading-[1.7] text-white/65">
            Events, features, and word-of-mouth turn one ad buy into something
            that compounds.
          </p>
        </div>
      </div>
    </section>
  );
}
