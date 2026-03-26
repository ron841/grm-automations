import Image from "next/image";
import Link from "next/link";

export default function FPHero() {
  return (
    <section className="min-h-screen bg-grm-cream lg:grid lg:grid-cols-[35%_1fr]">
      {/* Left — Copy column */}
      <div className="flex items-center px-6 py-16 pt-[100px] lg:px-10 lg:py-0 lg:pt-0">
        <div className="w-full max-w-sm">
          <p className="mb-5 font-comfortaa text-[11px] font-bold uppercase tracking-[0.15em] text-grm-teal">
            A GET ROOTED MEDIA PUBLICATION &middot; BI-MONTHLY &middot; MARION
            COUNTY
          </p>

          <p className="mb-2 font-nunito text-base text-grm-black/70">
            The question every new resident asks:
          </p>

          <h1 className="mb-5 font-merriweather text-[32px] font-bold leading-tight text-grm-black lg:text-[40px]">
            &ldquo;Who do you use for _______ ?&rdquo;
          </h1>

          <p className="mb-8 font-nunito text-lg leading-relaxed text-grm-black/80">
            The bi-monthly resource guide mailed to every new homeowner in
            Marion County within their first 60 days. Premium paper. Real
            editorial content. The guide people actually keep.
          </p>

          <Link
            href="/contact"
            className="inline-block rounded-md bg-grm-teal px-6 py-3 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
          >
            Advertise in The Front Porch
          </Link>

          <a
            href="#reader-signup"
            className="mt-5 block font-nunito text-sm text-fp-sage transition-opacity hover:opacity-80"
          >
            New to Marion County? Skip to the resident section &darr;
          </a>
        </div>
      </div>

      {/* Right — Photo bleeds to edge, fills every pixel */}
      <div className="relative min-h-[50vh] lg:min-h-screen">
        <Image
          src="/images/fp-hero.webp"
          alt="Woman reading The Front Porch magazine in Marion County"
          fill
          priority
          className="object-cover"
          sizes="(max-width: 1024px) 100vw, 65vw"
        />
      </div>
    </section>
  );
}
