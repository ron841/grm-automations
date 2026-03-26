import Image from "next/image";
import Link from "next/link";

export default function HomePublications() {
  return (
    <section id="publications">
      {/* Section label */}
      <div className="bg-grm-cream pt-16 pb-10">
        <p className="text-center font-comfortaa text-[11px] font-bold uppercase tracking-[0.2em] text-grm-teal">
          OUR PUBLICATIONS
        </p>
        <div className="mx-auto mt-4 h-px w-8 bg-grm-teal" />
      </div>

      {/* Two-panel spread */}
      <div className="grid grid-cols-1 md:grid-cols-2">
        {/* LEFT PANEL — The Closing Table */}
        <div className="relative min-h-[60vh] md:min-h-[85vh] overflow-hidden">
          <Image
            src="/images/ct-hero.webp"
            alt="The Closing Table magazine on a dark table with white flowers"
            fill
            className="object-cover object-center"
            sizes="(max-width: 768px) 100vw, 50vw"
          />
          <div
            className="absolute inset-0"
            style={{
              background:
                "linear-gradient(to bottom right, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.45) 100%)",
            }}
          />
          <div className="absolute inset-0 flex flex-col justify-end p-7 md:p-12">
            <p className="font-comfortaa text-[10px] font-bold uppercase tracking-[0.18em] text-grm-teal">
              MONTHLY MAGAZINE &middot; JUNE 2026
            </p>
            <div className="mt-3">
              <span className="block font-grand-hotel text-[44px] leading-none text-white md:text-[44px]">
                The
              </span>
              <span className="block font-merriweather text-[48px] font-bold leading-none text-white md:text-[64px]">
                Closing Table
              </span>
            </div>
            <div className="my-5 h-px w-8 bg-grm-teal" />
            <p className="max-w-[320px] font-nunito text-[13px] leading-relaxed text-white/80 md:text-[14px]">
              The monthly magazine for Marion County&apos;s top real estate
              professionals. 500 agents. $2.8 billion in annual home sales.
              They read this.
            </p>
            <Link
              href="/the-closing-table"
              className="mt-5 inline-block font-nunito text-[13px] text-grm-teal no-underline transition-colors hover:underline"
            >
              Read more &rarr;
            </Link>
          </div>
        </div>

        {/* RIGHT PANEL — The Front Porch */}
        <div className="relative min-h-[60vh] md:min-h-[85vh] overflow-hidden">
          <Image
            src="/images/fp-hero.webp"
            alt="Woman reading The Front Porch magazine at home"
            fill
            className="object-cover object-right-center"
            sizes="(max-width: 768px) 100vw, 50vw"
          />
          <div
            className="absolute inset-0"
            style={{
              background:
                "linear-gradient(to bottom left, rgba(250,248,244,0.65) 0%, rgba(250,248,244,0.35) 100%)",
            }}
          />
          <div className="absolute inset-0 flex flex-col items-end justify-end p-7 text-right md:p-12">
            <p className="font-comfortaa text-[10px] font-bold uppercase tracking-[0.18em] text-grm-teal">
              BI-MONTHLY GUIDE &middot; JULY 2026
            </p>
            <div className="mt-3">
              <span className="block text-right font-grand-hotel text-[44px] leading-none text-grm-black md:text-[44px]">
                The
              </span>
              <span className="block text-right font-merriweather text-[48px] font-bold leading-none text-grm-black md:text-[64px]">
                Front Porch
              </span>
            </div>
            <div className="my-5 ml-auto h-px w-8 bg-grm-teal" />
            <p className="max-w-[320px] font-nunito text-[13px] leading-relaxed text-grm-black/75 md:text-[14px]">
              The bi-monthly resource guide mailed to every new homeowner in
              Marion County within their first 60 days. The dentist they find
              now is probably their dentist for the next decade.
            </p>
            <Link
              href="/the-front-porch"
              className="mt-5 inline-block font-nunito text-[13px] text-grm-teal no-underline transition-colors hover:underline"
            >
              Read more &rarr;
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
