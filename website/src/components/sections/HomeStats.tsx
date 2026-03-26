"use client";

import { useEffect, useRef, useState } from "react";

const STATS = [
  { number: "16,567+", label: "Net new residents, 2024" },
  { number: "~10,000", label: "Homes sold every year" },
  { number: "$4.3B", label: "Equine industry impact" },
  { number: "#1", label: "Fastest-growing metro in America" },
];

function AnimatedStat({
  number,
  label,
  visible,
}: {
  number: string;
  label: string;
  visible: boolean;
}) {
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    if (!visible) return;

    // Only animate pure integers (like 16,567+ or ~10,000)
    // Skip animation for decimals ($4.3B) and symbols (#1)
    const cleanNumber = number.replace(/[^0-9]/g, "");
    const hasDecimal = /\d\.\d/.test(number);
    const target = parseInt(cleanNumber, 10);

    if (isNaN(target) || target < 10 || hasDecimal) {
      setDisplayed(number);
      return;
    }

    const prefix = number.match(/^[^0-9]*/)?.[0] || "";
    const suffix = number.match(/[^0-9]*$/)?.[0] || "";

    const duration = 1200;
    const steps = 40;
    const stepTime = duration / steps;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      const progress = step / steps;
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(target * eased);

      const formatted = current.toLocaleString("en-US");
      setDisplayed(prefix + formatted + suffix);

      if (step >= steps) {
        clearInterval(timer);
        setDisplayed(number);
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [visible, number]);

  return (
    <div className="text-center">
      <p className="font-merriweather text-[40px] font-bold text-grm-teal sm:text-[56px]">
        {visible ? displayed : number}
      </p>
      <p className="mt-2 font-nunito text-sm text-white/70">{label}</p>
    </div>
  );
}

export default function HomeStats() {
  const sectionRef = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = sectionRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.3 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <section ref={sectionRef} className="bg-grm-black px-6 pt-12 pb-12 lg:px-8">
      <div className="mx-auto max-w-5xl">
        {/* Stats grid */}
        <div className="grid grid-cols-2 gap-10 lg:grid-cols-4">
          {STATS.map((stat) => (
            <AnimatedStat
              key={stat.label}
              number={stat.number}
              label={stat.label}
              visible={visible}
            />
          ))}
        </div>

        {/* Body copy */}
        <p className="mx-auto mt-10 max-w-[600px] text-center font-nunito text-lg leading-relaxed text-white/80">
          Marion County is not just growing. It is the fastest-growing metro in
          America. Nobody was connecting the businesses that serve this community
          with the people who need them most. Until now.
        </p>
      </div>
    </section>
  );
}
