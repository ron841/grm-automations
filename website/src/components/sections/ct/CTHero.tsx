import Image from "next/image";
import Link from "next/link";

export default function CTHero() {
  return (
    <section className="min-h-screen bg-grm-cream lg:grid lg:grid-cols-[35%_1fr]">
      {/* Left — Copy column, narrow */}
      <div className="flex items-center px-6 py-16 pt-[100px] lg:px-10 lg:py-0 lg:pt-0">
        <div className="w-full max-w-sm">
          <p className="mb-5 font-comfortaa text-[11px] font-bold uppercase tracking-[0.15em] text-grm-teal">
            A GET ROOTED MEDIA PUBLICATION &middot; MONTHLY &middot; MARION
            COUNTY
          </p>

          <h1 className="mb-5 font-merriweather text-[32px] font-bold leading-tight text-grm-black lg:text-[40px]">
            No one gets to the closing table alone.
          </h1>

          <p className="mb-8 font-nunito text-lg leading-relaxed text-grm-black/80">
            The monthly magazine celebrating Marion County&apos;s top real
            estate professionals and the service companies who make every deal
            possible.
          </p>

          <div className="flex flex-col gap-3">
            <Link
              href="/contact"
              className="rounded-md bg-grm-teal px-6 py-3 text-center font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
            >
              Advertise in The Closing Table
            </Link>
            <Link
              href="/contact"
              className="rounded-md border-2 border-grm-teal px-6 py-3 text-center font-nunito text-sm font-bold text-grm-teal transition-colors hover:bg-grm-teal hover:text-white"
            >
              Request the Media Kit
            </Link>
          </div>

          <p className="mt-5 font-nunito text-[13px] text-grm-black/50">
            Seen. Found. Chosen.
          </p>
        </div>
      </div>

      {/* Right — Photo bleeds to edge, fills every pixel */}
      <div className="relative min-h-[50vh] lg:min-h-screen">
        <Image
          src="/images/ct-hero.webp"
          alt="The Closing Table magazine on a dark table with white flowers"
          fill
          priority
          className="object-cover"
          sizes="(max-width: 1024px) 100vw, 65vw"
        />
      </div>
    </section>
  );
}
