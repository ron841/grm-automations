import Link from "next/link";

const BENEFITS = [
  "Rate lock. Your monthly rate never increases as long as you remain an advertiser.",
  "Founding Partner recognition in Issue 1. The one people keep.",
  "First right of renewal. No one takes your position before you get the first call.",
  "Featured in the launch story. Everywhere Issue 1 goes.",
];

export default function CTFoundingPartner() {
  return (
    <section className="bg-grm-black px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-[640px] text-center">
        <p className="mb-4 font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
          FOUNDING PARTNER BENEFITS
        </p>
        <div className="mx-auto mb-10 h-[3px] w-10 bg-grm-teal" />

        <p className="mb-8 font-nunito text-lg text-white/80">
          Right now, there is a difference between being first and being next.
          Cover positions are limited to four per issue. Interior spots are
          filling.
        </p>

        <p className="mb-8 font-nunito text-lg text-white/80">
          Founding partners receive four commitments not available after Issue 1:
        </p>

        <div className="mb-10 flex flex-col gap-4 text-left">
          {BENEFITS.map((benefit, i) => (
            <div key={i} className="flex gap-3">
              <span className="mt-1 shrink-0 font-merriweather text-lg font-bold text-grm-teal">
                {i + 1}.
              </span>
              <p className="font-nunito text-base leading-relaxed text-white/80">
                {benefit}
              </p>
            </div>
          ))}
        </div>

        <p className="mb-10 font-merriweather text-xl italic text-white">
          The founding partner window closes when Issue 1 goes to print.
        </p>

        <Link
          href="/contact"
          className="inline-block rounded-md bg-grm-teal px-10 py-4 font-nunito text-base font-bold text-white transition-opacity hover:opacity-90"
        >
          Let&apos;s Talk
        </Link>

        <p className="mt-4 font-nunito text-sm text-white/50">
          15 minutes. No pitch. A conversation about whether this is right for
          your business.
        </p>
      </div>
    </section>
  );
}
