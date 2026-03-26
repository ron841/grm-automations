import Image from "next/image";
import Link from "next/link";

export default function HomeHero() {
  return (
    <section className="relative h-[85vh] min-h-[600px] max-h-[90vh]">
      {/* Background image */}
      <Image
        src="/images/hero/1-Horse-Country-1.webp"
        alt="Two horses grazing at golden hour on a Marion County horse farm with Spanish moss trees in background"
        fill
        priority
        className="object-cover"
        sizes="100vw"
      />

      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/30 to-black/50" />

      {/* Content */}
      <div className="relative z-10 flex h-full flex-col justify-center px-6 lg:px-8">
        <div className="mx-auto w-full max-w-7xl text-center lg:text-left">
          {/* Kicker */}
          <p className="mb-4 font-comfortaa text-xs font-bold uppercase tracking-[0.15em] text-white/70">
            PRINT + DIGITAL. COMMUNITY FIRST.
          </p>

          {/* Headline */}
          <h1 className="mb-6 font-merriweather text-[40px] font-bold leading-tight text-white lg:text-[64px]">
            You&apos;re home.<br />
            But you&apos;re not rooted.
          </h1>

          {/* Subheadline */}
          <p className="mx-auto mb-10 max-w-[580px] font-nunito text-xl leading-relaxed text-white/85 lg:mx-0">
            Two publications. The businesses that built Marion County, and the
            people arriving every week who need them.
          </p>

          {/* Buttons */}
          <div className="flex flex-col items-center gap-4 sm:flex-row lg:items-start">
            <Link
              href="/contact"
              className="rounded-md bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
            >
              Advertise With Us
            </Link>
            <Link
              href="/about"
              className="rounded-md border border-white px-8 py-3.5 font-nunito text-sm font-bold text-white transition-colors hover:bg-white/10"
            >
              Our Story
            </Link>
          </div>
        </div>
      </div>

      {/* Animated bounce chevron */}
      <div className="absolute bottom-8 left-1/2 z-10 -translate-x-1/2 animate-bounce">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="text-white/50"
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </div>
    </section>
  );
}
