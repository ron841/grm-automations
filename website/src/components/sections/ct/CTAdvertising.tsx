export default function CTAdvertising() {
  return (
    <section id="advertising" className="bg-grm-black px-8 py-12 md:px-20 md:py-[72px]">
      <div className="mx-auto flex max-w-7xl flex-col items-start gap-10 md:flex-row md:items-stretch md:gap-0">
        {/* ITEM 1 — 38% */}
        <div className="w-full pr-0 md:w-[38%] md:pr-12">
          <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.25em] text-grm-teal">
            01
          </p>
          <h3 className="mb-3.5 font-merriweather text-[28px] font-bold leading-[1.2] text-white">
            Print.
          </h3>
          <p className="font-nunito text-[14px] leading-[1.7] text-white/60">
            Your ad in a magazine that sits on desks, gets passed around
            offices, and stays in the hands of the people who refer business. A
            social post disappears in 0.3 seconds. A magazine gets picked up
            four to five times.
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
            Digital.
          </h3>
          <p className="font-nunito text-[13px] leading-[1.7] text-white/60">
            Your campaign runs through The Closing Table&apos;s Instagram and
            Facebook pages. When agents see your business in their feed, they
            see a recommendation from the publication they already trust.
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
            Community.
          </h3>
          <p className="font-nunito text-[13px] leading-[1.7] text-white/60">
            Two mixers and one annual awards gala. Every advertiser receives two
            complimentary tickets. Your brand in the room with the top 500
            agents and service companies in Marion and Sumter Counties.
          </p>
        </div>
      </div>
    </section>
  );
}
