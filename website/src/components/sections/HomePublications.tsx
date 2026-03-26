import Image from "next/image";
import Link from "next/link";

const PUBLICATIONS = [
  {
    slug: "the-closing-table",
    image: "/images/publications/7-Closing-2.webp",
    imageAlt:
      "The Closing Table magazine on a professional real estate setting in Marion County",
    label: "MONTHLY MAGAZINE · JUNE 2026",
    scriptThe: true,
    titleCaps: "CLOSING TABLE",
    body: "The monthly magazine for Marion County\u2019s top real estate professionals.",
    stats:
      "850-1,000 copies · 12 issues per year · $2.8B in annual sales volume",
    cta: "See The Closing Table \u2192",
  },
  {
    slug: "the-front-porch",
    image: "/images/fp/2-Family-1.webp",
    imageAlt:
      "Family arriving at their new home in a Marion County neighborhood",
    label: "BI-MONTHLY GUIDE · JULY 2026",
    scriptThe: true,
    titleCaps: "FRONT PORCH",
    body: "The bi-monthly resource guide mailed to every new homeowner in Marion County within their first 60 days.",
    stats:
      "1,500-2,000 new homeowners per issue · 6 issues per year · 60-day decision window",
    cta: "See The Front Porch \u2192",
  },
];

export default function HomePublications() {
  return (
    <section className="bg-grm-cream px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-5xl">
        {/* Brand line */}
        <p className="mb-6 text-center font-merriweather text-[22px] italic text-grm-teal">
          Seen in the magazine. Found online. Chosen when the purchase happens.
        </p>

        {/* Cards */}
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
          {PUBLICATIONS.map((pub) => (
            <div
              key={pub.slug}
              className="overflow-hidden rounded-[4px] bg-white shadow-md transition-shadow duration-200 hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)]"
            >
              {/* Image — top 40% */}
              <div className="relative aspect-[5/3]">
                <Image
                  src={pub.image}
                  alt={pub.imageAlt}
                  fill
                  className="object-cover"
                  sizes="(max-width: 768px) 100vw, 50vw"
                />
              </div>

              {/* Content */}
              <div className="p-8">
                {/* Label */}
                <p className="mb-3 font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
                  {pub.label}
                </p>

                {/* Headline with script "The" */}
                <h3 className="mb-4">
                  <span className="font-grand-hotel text-[22px] font-normal text-grm-black">
                    The
                  </span>{" "}
                  <span className="font-comfortaa text-[24px] font-bold uppercase text-grm-black">
                    {pub.titleCaps}
                  </span>
                </h3>

                {/* Body */}
                <p className="mb-4 font-nunito text-base leading-relaxed text-grm-black">
                  {pub.body}
                </p>

                {/* Stats */}
                <p className="mb-6 font-nunito text-[13px] text-grm-teal">
                  {pub.stats}
                </p>

                {/* Button */}
                <Link
                  href={`/${pub.slug}`}
                  className="inline-block rounded-md bg-grm-teal px-6 py-3 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
                >
                  {pub.cta}
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
