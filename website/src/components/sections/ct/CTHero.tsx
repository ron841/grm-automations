import Image from "next/image";
import Link from "next/link";

export default function CTHero() {
  return (
    <section className="bg-grm-cream">
      <div className="grid min-h-screen grid-cols-1 lg:grid-cols-2">
        {/* Left — Image fills full height */}
        <div className="relative min-h-[50vh] lg:min-h-screen">
          <Image
            src="/images/ct-hero.webp"
            alt="The Closing Table magazine on a dark table with white flowers"
            fill
            priority
            className="object-cover"
            sizes="(max-width: 1024px) 100vw, 50vw"
          />
        </div>

        {/* Right — Copy on light background */}
        <div className="flex items-center px-8 py-16 pt-8 lg:px-16 lg:py-0 lg:pt-[120px]">
          <div className="max-w-lg">
            <p className="mb-6 font-comfortaa text-[11px] font-bold uppercase tracking-[0.15em] text-grm-teal">
              A GET ROOTED MEDIA PUBLICATION &middot; MONTHLY &middot; MARION
              COUNTY
            </p>

            <h1 className="mb-6 font-merriweather text-[36px] font-bold leading-tight text-grm-black lg:text-[48px]">
              No one gets to the closing table alone.
            </h1>

            <p className="mb-10 max-w-[480px] font-nunito text-xl leading-relaxed text-grm-black/80">
              The monthly magazine celebrating Marion County&apos;s top real
              estate professionals and the service companies who make every deal
              possible.
            </p>

            <div className="flex flex-col items-start gap-4 sm:flex-row">
              <Link
                href="/contact"
                className="rounded-md bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
              >
                Advertise in The Closing Table
              </Link>
              <Link
                href="/contact"
                className="rounded-md border-2 border-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-grm-teal transition-colors hover:bg-grm-teal hover:text-white"
              >
                Request the Media Kit
              </Link>
            </div>

            <p className="mt-6 font-nunito text-[13px] text-grm-black/50">
              Seen. Found. Chosen.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
