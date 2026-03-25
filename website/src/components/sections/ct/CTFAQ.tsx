"use client";

import { useState } from "react";

const FAQS = [
  {
    question: "How is this different from Real Producers?",
    answer:
      "Real Producers mails only to agents. The Closing Table mails to agents and the 500+ service companies who support real estate in Marion County. Your ad reaches both sides of the referral relationship.",
  },
  {
    question: "I\u2019m a lender. Will agents actually see my ad?",
    answer:
      "Every issue is mailed to the top 350 producing agents in Marion County, sourced from Stellar MLS transaction data. Not a random list. The agents closing the most deals. Your ad appears next to cover stories about their peers.",
  },
  {
    question: "What if I don\u2019t have print-ready artwork?",
    answer:
      "For $200 our designer builds your ad using your logo, photos, and website. One round of revisions included. Most advertisers use this service.",
  },
  {
    question: "What\u2019s the commitment?",
    answer:
      "Annual agreements, billed monthly. Magazine advertising works through consistency. Recognition builds over 6 to 12 months, not from a single issue.",
  },
  {
    question: "When does Issue 1 come out?",
    answer:
      "June 2026. Businesses who come in now are founding partners. After Issue 1, you\u2019re an advertiser. Right now, you\u2019re part of the beginning.",
  },
];

export default function CTFAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="bg-grm-cream px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-3xl">
        <p className="mb-4 text-center font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
          FREQUENTLY ASKED QUESTIONS
        </p>
        <div className="mx-auto mb-10 h-[3px] w-10 bg-grm-teal" />

        <div className="flex flex-col gap-3">
          {FAQS.map((faq, i) => (
            <div
              key={i}
              className="rounded-md bg-white"
            >
              <button
                onClick={() => setOpenIndex(openIndex === i ? null : i)}
                className="flex w-full items-center justify-between p-6 text-left"
              >
                <span className="pr-4 font-nunito text-base font-semibold text-grm-black">
                  {faq.question}
                </span>
                <span
                  className={`shrink-0 text-grm-teal transition-transform duration-200 ${
                    openIndex === i ? "rotate-45" : ""
                  }`}
                >
                  <svg
                    width="20"
                    height="20"
                    viewBox="0 0 20 20"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <line x1="10" y1="4" x2="10" y2="16" />
                    <line x1="4" y1="10" x2="16" y2="10" />
                  </svg>
                </span>
              </button>
              <div
                className={`overflow-hidden transition-all duration-200 ${
                  openIndex === i ? "max-h-96 pb-6" : "max-h-0"
                }`}
              >
                <p className="px-6 font-nunito text-base leading-[1.7] text-grm-black">
                  {faq.answer}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
