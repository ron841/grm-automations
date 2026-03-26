import Image from "next/image";
import Link from "next/link";

export default function CTHero() {
  return (
    <section className="relative min-h-screen bg-grm-black">
      {/* Background image at full opacity */}
      <Image
        src="/images/hero/4-Ocala-1.webp"
        alt="Downtown Ocala Square at golden hour in Marion County"
        fill
        priority
        className="object-cover"
        sizes="100vw"
      />

      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/30 to-black/50" />

      <div className="relative z-10 flex min-h-screen items-center px-6 pt-[100px] lg:px-8 lg:pt-[120px]">
        <div className="mx-auto w-full max-w-7xl">
          <div className="max-w-xl text-center lg:text-left">
            <p className="mb-6 font-comfortaa text-[11px] font-bold uppercase tracking-[0.15em] text-white/60">
              A GET ROOTED MEDIA PUBLICATION &middot; MONTHLY &middot; MARION
              COUNTY
            </p>

            <h1 className="mb-6 font-merriweather text-[40px] font-bold leading-tight text-white lg:text-[56px]">
              No one gets to the closing table alone.
            </h1>

            <p className="mx-auto mb-10 max-w-[520px] font-nunito text-xl leading-relaxed text-white/85 lg:mx-0">
              The monthly magazine celebrating Marion County&apos;s top real
              estate professionals and the service companies who make every deal
              possible.
            </p>

            <div className="flex flex-col items-center gap-4 sm:flex-row lg:items-start">
              <Link
                href="/contact"
                className="rounded-md bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
              >
                Advertise in The Closing Table
              </Link>
              <Link
                href="/contact"
                className="rounded-md border border-white px-8 py-3.5 font-nunito text-sm font-bold text-white transition-colors hover:bg-white/10"
              >
                Request the Media Kit
              </Link>
            </div>

            <p className="mt-6 font-nunito text-[13px] text-white/60">
              Seen. Found. Chosen.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
