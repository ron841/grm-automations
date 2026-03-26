"use client";

import React from "react";
import {
  motion,
  useScroll,
  useTransform,
  useSpring,
  MotionValue,
} from "framer-motion";
import Image from "next/image";
import Link from "next/link";

const IMAGES = [
  // Row 1
  { title: "Horse Country", thumbnail: "/images/hero/1-Horse-Country-1.webp" },
  { title: "Downtown Ocala", thumbnail: "/images/hero/4-Ocala-1.webp" },
  { title: "Equestrian Life", thumbnail: "/images/hero/5-Equestrian-1.webp" },
  { title: "Marion County Home", thumbnail: "/images/fp/3-Exterior-1.webp" },
  { title: "Family Roots", thumbnail: "/images/fp/2-Family-1.webp" },
  // Row 2
  { title: "Tuscawilla Park", thumbnail: "/images/hero/4-Ocala-2.webp" },
  { title: "Horse Farm", thumbnail: "/images/hero/1-Horse-Country-2.webp" },
  { title: "New Homeowners", thumbnail: "/images/fp/2-Family-2.webp" },
  { title: "Equestrian County", thumbnail: "/images/hero/5-Equestrian-2.webp" },
  { title: "Marion County Living", thumbnail: "/images/fp/3-Exterior-2.webp" },
];

export default function HomeHero() {
  const firstRow = IMAGES.slice(0, 5);
  const secondRow = IMAGES.slice(5, 10);
  const ref = React.useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });

  const springConfig = { stiffness: 300, damping: 30, bounce: 100 };

  const translateX = useSpring(
    useTransform(scrollYProgress, [0, 1], [0, 1000]),
    springConfig
  );
  const translateXReverse = useSpring(
    useTransform(scrollYProgress, [0, 1], [0, -1000]),
    springConfig
  );
  const rotateX = useSpring(
    useTransform(scrollYProgress, [0, 0.2], [15, 0]),
    springConfig
  );
  const opacity = useSpring(
    useTransform(scrollYProgress, [0, 0.2], [0.2, 1]),
    springConfig
  );
  const rotateZ = useSpring(
    useTransform(scrollYProgress, [0, 0.2], [20, 0]),
    springConfig
  );
  const translateY = useSpring(
    useTransform(scrollYProgress, [0, 0.2], [-300, 500]),
    springConfig
  );

  return (
    <div
      ref={ref}
      className="h-[200vh] overflow-hidden bg-grm-black py-40 antialiased relative flex flex-col self-auto [perspective:1000px] [transform-style:preserve-3d]"
    >
      {/* GRM Header */}
      <div className="max-w-7xl relative mx-auto py-10 md:py-20 px-6 w-full left-0 top-0">
        <p className="font-comfortaa text-xs font-bold uppercase tracking-[0.2em] text-grm-teal mb-6">
          MARION COUNTY&apos;S MEDIA COMPANY
        </p>
        <h1 className="font-merriweather text-4xl md:text-6xl lg:text-7xl font-bold text-grm-cream leading-tight">
          Locally Rooted.
          <br />
          Professionally Grown.
        </h1>
        <p className="max-w-2xl font-nunito text-base md:text-lg mt-8 text-grm-cream/70">
          The publications Marion County&apos;s real estate professionals and
          new homeowners actually read.
        </p>
        <Link
          href="#publications"
          className="mt-8 inline-block rounded-md bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
        >
          See Our Publications
        </Link>
      </div>

      {/* Parallax image rows */}
      <motion.div
        style={{ rotateX, rotateZ, translateY, opacity }}
      >
        <motion.div className="flex flex-row-reverse space-x-reverse space-x-20 mb-20">
          {firstRow.map((img) => (
            <ParallaxCard
              key={img.title}
              image={img}
              translate={translateX}
            />
          ))}
        </motion.div>
        <motion.div className="flex flex-row mb-20 space-x-20">
          {secondRow.map((img) => (
            <ParallaxCard
              key={img.title}
              image={img}
              translate={translateXReverse}
            />
          ))}
        </motion.div>
      </motion.div>
    </div>
  );
}

function ParallaxCard({
  image,
  translate,
}: {
  image: { title: string; thumbnail: string };
  translate: MotionValue<number>;
}) {
  return (
    <motion.div
      style={{ x: translate }}
      whileHover={{ y: -20 }}
      className="group/product h-96 w-[30rem] relative flex-shrink-0"
    >
      <div className="block">
        <Image
          src={image.thumbnail}
          height={600}
          width={600}
          className="object-cover object-center absolute h-full w-full inset-0 rounded-sm"
          alt={image.title}
        />
      </div>
      <div className="absolute inset-0 h-full w-full opacity-0 group-hover/product:opacity-60 bg-grm-black rounded-sm pointer-events-none transition-opacity" />
      <h2 className="absolute bottom-4 left-4 opacity-0 group-hover/product:opacity-100 text-white font-nunito text-sm transition-opacity">
        {image.title}
      </h2>
    </motion.div>
  );
}
