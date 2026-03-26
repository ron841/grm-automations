"use client";

import Image from "next/image";
import Link from "next/link";
import React, { useState } from "react";
import { cn } from "@/lib/utils";

const PUBLICATIONS = [
  {
    image: "/images/ct-hero.webp",
    imageAlt: "The Closing Table magazine on a dark table with white flowers",
    label: "MONTHLY MAGAZINE · JUNE 2026",
    title: "The Closing Table",
    description:
      "The monthly magazine for Marion County\u2019s top real estate professionals.",
    href: "/the-closing-table",
  },
  {
    image: "/images/fp-hero.webp",
    imageAlt: "Woman reading The Front Porch magazine at home",
    label: "BI-MONTHLY GUIDE · JULY 2026",
    title: "The Front Porch",
    description:
      "The bi-monthly resource guide mailed to every new homeowner in Marion County within their first 60 days.",
    href: "/the-front-porch",
  },
];

export default function HomePublications() {
  const [hovered, setHovered] = useState<number | null>(null);

  return (
    <section id="publications" className="bg-grm-cream px-6 py-20 lg:px-8">
      <p className="mb-10 text-center font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
        OUR PUBLICATIONS
      </p>

      <div className="mx-auto grid max-w-7xl grid-cols-1 md:grid-cols-2">
        {PUBLICATIONS.map((pub, index) => (
          <div
            key={pub.title}
            onMouseEnter={() => setHovered(index)}
            onMouseLeave={() => setHovered(null)}
            className={cn(
              "relative min-h-[600px] overflow-hidden transition-all duration-500 ease-out",
              hovered !== null && hovered !== index && "blur-sm scale-[0.98]"
            )}
          >
            {/* Full-bleed image */}
            <Image
              src={pub.image}
              alt={pub.imageAlt}
              fill
              className="object-cover"
              sizes="(max-width: 768px) 100vw, 50vw"
            />

            {/* Subtle gradient at rest */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />

            {/* Hover overlay with content */}
            <div
              className={cn(
                "absolute inset-0 flex flex-col justify-end bg-black/50 p-8 transition-opacity duration-300 lg:p-12",
                hovered === index ? "opacity-100" : "opacity-0"
              )}
            >
              <p className="mb-3 font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
                {pub.label}
              </p>

              <h3 className="mb-3 text-white">
                <span className="block font-grand-hotel text-[32px] leading-none lg:text-[38px]">
                  The
                </span>
                <span className="block font-merriweather text-2xl font-bold lg:text-3xl">
                  {pub.title.replace("The ", "")}
                </span>
              </h3>

              <p className="mb-5 max-w-sm font-nunito text-base leading-relaxed text-white/85">
                {pub.description}
              </p>

              <Link
                href={pub.href}
                className="font-nunito text-sm text-grm-teal no-underline transition-colors hover:underline"
              >
                Read More &rarr;
              </Link>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
