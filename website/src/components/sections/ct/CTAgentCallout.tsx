export default function CTAgentCallout() {
  return (
    <section className="bg-grm-black px-8 py-12 md:px-20 md:py-16">
      <div className="mx-auto flex max-w-7xl flex-col gap-10 md:flex-row md:items-center md:gap-0">
        {/* LEFT — 60% */}
        <div className="w-full md:w-[60%]">
          <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.2em] text-grm-teal">
            ISSUE 1 &middot; JUNE 2026
          </p>
          <div className="mb-6 h-px w-8 bg-grm-teal" />
          <h2 className="font-merriweather text-[28px] font-bold leading-[1.3] text-white md:text-[32px]">
            We&apos;re selecting cover stories and agent profiles for Issue 1.
          </h2>
          <p className="mt-4 max-w-[480px] font-nunito text-[15px] leading-[1.75] text-white/70">
            If you&apos;re one of Marion County&apos;s top producers and you
            want your story told the right way, we want to hear from you.
          </p>
        </div>

        {/* RIGHT — 40% */}
        <div className="flex w-full flex-col items-center md:w-[40%]">
          <a
            href="https://cal.com/ron-kolb-cdlgsw/30min"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block rounded-[2px] bg-grm-teal px-10 py-4 font-nunito text-[15px] font-bold text-white transition-colors duration-200 hover:bg-[#3da0b5]"
          >
            Tell Us Your Story
          </a>
          <p className="mt-3 font-nunito text-[12px] text-white/50">
            Takes 30 minutes. No obligation.
          </p>
        </div>
      </div>
    </section>
  );
}
