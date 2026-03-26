"use client";

import Link from "next/link";
import { ImagesSlider } from "@/components/ui/images-slider";

const IMAGES = [
  "/images/fp-hero.webp",
  "/images/fp/3-Exterior-1.webp",
  "/images/fp/3-Exterior-2.webp",
];

export default function FPHero() {
  return (
    <ImagesSlider
      images={IMAGES}
      className="min-h-screen"
      overlayClassName="bg-gradient-to-t from-black/70 via-black/40 to-black/20"
      autoplay
      direction="up"
    >
      <div className="relative z-50 flex flex-col items-center justify-center px-6 text-center">
        <p className="mb-6 font-comfortaa text-[11px] font-bold uppercase tracking-[0.2em] text-grm-teal">
          A GET ROOTED MEDIA PUBLICATION &middot; BI-MONTHLY &middot; MARION
          COUNTY
        </p>

        <h1 className="mb-6 max-w-2xl font-merriweather text-[36px] font-bold leading-tight text-white lg:text-[56px]">
          &ldquo;Who do you use for _______ ?&rdquo;
        </h1>

        <p className="mb-10 max-w-[480px] font-nunito text-lg text-white/80">
          The bi-monthly resource guide mailed to every new homeowner in Marion
          County within their first 60 days.
        </p>

        <Link
          href="#advertising"
          className="rounded-[3px] bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
        >
          Advertise in The Front Porch
        </Link>

        <Link
          href="#reader-signup"
          className="mt-5 font-nunito text-sm text-white/70 no-underline transition-colors hover:text-white hover:underline"
        >
          New to Marion County? Find your resources below
        </Link>
      </div>
    </ImagesSlider>
  );
}
