export default function HomeFinalCTA() {
  return (
    <section className="bg-grm-black px-8 py-[72px] md:px-20 md:py-[100px]">
      <div className="mx-auto max-w-3xl text-center">
        <p className="mb-6 font-comfortaa text-[10px] font-bold uppercase tracking-[0.25em] text-grm-teal">
          FOUNDING PARTNER &middot; LIMITED AVAILABILITY
        </p>
        <div className="mx-auto mb-10 h-px w-10 bg-grm-teal" />

        <h2 className="mx-auto mb-6 max-w-[700px] font-merriweather text-[36px] font-bold leading-[1.15] text-white md:text-[52px]">
          Right now, you&apos;re a founding partner.
        </h2>

        <div className="mx-auto max-w-[520px]">
          <p className="mb-4 font-nunito text-[17px] leading-[1.8] text-white/70">
            The first issue is being built right now.
          </p>
          <p className="mb-4 font-nunito text-[17px] leading-[1.8] text-white/70">
            The businesses who come in now are not just buying ad space.
          </p>
          <p className="font-nunito text-[17px] leading-[1.8] text-white/70">
            After Issue 1, you&apos;re an advertiser.
          </p>
        </div>

        <div className="mt-12">
          <a
            href="https://cal.com/ron-kolb-cdlgsw/30min"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block rounded-[2px] bg-grm-teal px-12 py-4 font-nunito text-[15px] font-bold tracking-[0.05em] text-white transition-colors duration-200 hover:bg-[#3da0b5]"
          >
            Let&apos;s Talk
          </a>
          <p className="mt-4">
            <span className="font-nunito text-[13px] text-grm-teal no-underline transition-colors hover:underline cursor-pointer">
              or request our media kit
            </span>
          </p>
        </div>
      </div>
    </section>
  );
}
