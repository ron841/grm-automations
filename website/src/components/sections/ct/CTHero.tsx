import Image from "next/image";
import Link from "next/link";

export default function CTHero() {
  return (
    <section className="relative h-screen w-full overflow-hidden">
      {/* Background image */}
      <Image
        src="/images/ct-hero.webp"
        alt="The Closing Table magazine on a dark table with white flowers"
        fill
        priority
        className="object-cover"
      />

      {/* Two-axis overlay: top-to-bottom + left-to-right */}
      <div
        className="absolute inset-0"
        style={{
          background: [
            "linear-gradient(to right, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.35) 50%, rgba(0,0,0,0.1) 100%)",
            "linear-gradient(to bottom, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.2) 100%)",
          ].join(", "),
        }}
      />

      {/* Content — lower-left quadrant */}
      <div className="absolute inset-0 flex items-end pb-[20vh] px-8 md:px-20">
        <div className="max-w-xl">
          {/* Eyebrow */}
          <p className="mb-4 font-comfortaa text-[11px] font-bold uppercase tracking-[0.2em] text-grm-teal">
            A GET ROOTED MEDIA PUBLICATION &middot; MONTHLY &middot; MARION
            COUNTY
          </p>

          {/* Publication name — script "The" + serif "Closing Table" */}
          <div className="mb-6">
            <span className="block font-grand-hotel text-[52px] text-white leading-none">
              The
            </span>
            <h1 className="block font-merriweather text-[56px] md:text-[88px] font-bold text-white leading-none">
              Closing Table
            </h1>
          </div>

          {/* Headline */}
          <p className="max-w-[520px] font-merriweather text-[20px] md:text-[24px] font-normal text-white leading-relaxed">
            No one gets to the closing table alone.
          </p>

          {/* CTA buttons */}
          <div className="mt-9 flex flex-wrap items-center gap-4">
            <Link
              href="#advertising"
              className="rounded-[3px] bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
            >
              See Advertising Options
            </Link>
            <Link
              href="/about"
              className="rounded-[3px] border border-white px-8 py-3.5 font-nunito text-sm font-bold text-white transition-colors hover:bg-white/10"
            >
              Read the founding story
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
