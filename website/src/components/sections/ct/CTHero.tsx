"use client";

import Link from "next/link";
import { ImagesSlider } from "@/components/ui/images-slider";

const IMAGES = [
  "/images/ct-hero.webp",
  "/images/publications/7-Closing-1.webp",
  "/images/publications/7-Closing-2.webp",
  "/images/publications/6-Mag-Lifestyle-2.webp",
];

export default function CTHero() {
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
          A GET ROOTED MEDIA PUBLICATION &middot; MONTHLY &middot; MARION COUNTY
        </p>

        <h1 className="mb-6 max-w-2xl font-merriweather text-[36px] font-bold leading-tight text-white lg:text-[56px]">
          No one gets to the closing table alone.
        </h1>

        <p className="mb-10 max-w-[480px] font-nunito text-lg text-white/80">
          The monthly magazine for Marion County&apos;s top real estate
          professionals.
        </p>

        <Link
          href="#advertising"
          className="rounded-[3px] bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
        >
          See Advertising Options
        </Link>

        <Link
          href="/about"
          className="mt-5 font-nunito text-sm text-white/70 no-underline transition-colors hover:text-white hover:underline"
        >
          Read the founding story
        </Link>
      </div>
    </ImagesSlider>
  );
}
