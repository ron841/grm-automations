import Image from "next/image";
import Link from "next/link";

export default function FPHero() {
  return (
    <section className="relative min-h-screen bg-grm-cream">
      {/* Background image */}
      <Image
        src="/images/fp/2-Family-1.webp"
        alt="Family arriving at their new home in a Marion County neighborhood"
        fill
        priority
        className="object-cover"
        sizes="100vw"
      />

      {/* Warm gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-black/50 via-black/30 to-transparent" />

      <div className="relative z-10 flex min-h-screen items-center px-6 pt-[100px] lg:px-8 lg:pt-[120px]">
        <div className="mx-auto w-full max-w-7xl">
          <div className="max-w-xl text-center lg:text-left">
            <p className="mb-6 font-comfortaa text-[11px] font-bold uppercase tracking-[0.15em] text-white/70">
              A GET ROOTED MEDIA PUBLICATION &middot; BI-MONTHLY &middot; MARION
              COUNTY
            </p>

            <p className="mb-2 font-nunito text-lg text-white/80">
              The question every new resident asks:
            </p>

            <h1 className="mb-6 font-merriweather text-[36px] font-bold leading-tight text-white lg:text-[52px]">
              &ldquo;Who do you use for _______ ?&rdquo;
            </h1>

            <p className="mx-auto mb-10 max-w-[520px] font-nunito text-xl leading-relaxed text-white/85 lg:mx-0">
              The bi-monthly resource guide mailed to every new homeowner in
              Marion County within their first 60 days. Premium paper. Real
              editorial content. The guide people actually keep.
            </p>

            <div className="flex flex-col items-center gap-4 sm:flex-row lg:items-start">
              <Link
                href="/contact"
                className="rounded-md bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
              >
                Advertise in The Front Porch
              </Link>
            </div>

            {/* Anchor link for new residents */}
            <a
              href="#reader-signup"
              className="mt-6 inline-block font-nunito text-sm text-fp-sage transition-opacity hover:opacity-80"
            >
              New to Marion County? Skip to the resident section &darr;
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
