const BENEFITS = [
  {
    number: "01",
    title: "Rate lock.",
    body: "Your monthly rate never increases as long as you remain an advertiser.",
  },
  {
    number: "02",
    title: "Founding Partner recognition.",
    body: "Issue 1 is the one people keep. Your name is in it permanently.",
  },
  {
    number: "03",
    title: "First right of renewal.",
    body: "No one takes your position before you get the first call.",
  },
  {
    number: "04",
    title: "Featured in the launch story.",
    body: "Everywhere Issue 1 goes, your name goes with it.",
  },
];

export default function CTFoundingPartner() {
  return (
    <section className="flex flex-col md:flex-row">
      {/* LEFT COLUMN — 52% */}
      <div className="w-full bg-grm-black px-8 py-12 md:w-[52%] md:px-16 md:py-[72px]">
        <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.2em] text-grm-teal">
          FOUNDING PARTNER &middot; LIMITED AVAILABILITY
        </p>
        <div className="mb-7 h-px w-8 bg-grm-teal" />
        <h2 className="font-merriweather text-[32px] font-bold leading-[1.2] text-white md:text-[42px]">
          Right now, there is a difference between being first and being next.
        </h2>
        <p className="mt-5 max-w-[420px] font-nunito text-[15px] leading-[1.75] text-white/70">
          Cover positions are limited to four per issue. Interior spots are
          filling. The businesses that come in now get terms, recognition,
          and access that will not be offered again after Issue 1 goes to
          print.
        </p>
        <a
          href="https://cal.com/ron-kolb-cdlgsw/30min"
          target="_blank"
          rel="noopener noreferrer"
          className="mt-9 inline-block rounded-[2px] bg-grm-teal px-10 py-4 font-nunito text-[15px] font-bold text-white transition-colors duration-200 hover:bg-[#3da0b5]"
        >
          Let&apos;s Talk About Advertising
        </a>
      </div>

      {/* RIGHT COLUMN — 48% */}
      <div className="flex w-full items-center bg-[#222222] px-8 py-12 md:w-[48%] md:px-14 md:py-[72px]">
        <div className="w-full">
          {BENEFITS.map((b, i) => (
            <div key={b.number}>
              <p className="mb-2 font-comfortaa text-[11px] font-bold tracking-[0.2em] text-grm-teal">
                {b.number}
              </p>
              <p className="font-merriweather text-[16px] font-bold leading-[1.4] text-white">
                {b.title}
              </p>
              <p className="mt-1.5 font-nunito text-[13px] leading-[1.6] text-white/60">
                {b.body}
              </p>
              {i < BENEFITS.length - 1 && (
                <div className="my-6 h-px w-full bg-white/10" />
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
