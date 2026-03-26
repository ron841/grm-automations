"use client";

import { useState } from "react";

const FAQS = [
  {
    question: "How do new homeowners get The Front Porch?",
    answer:
      "We mail it to every new homeowner in Marion County within their first 60 days, sourced from county property records. It arrives when they need it most, without them having to search for it.",
  },
  {
    question: "What does category-limited mean?",
    answer:
      "A few spots available per category, per year. If you\u2019re one of the HVAC companies in The Front Porch, your competitors have limited space to appear. First to sign gets the strongest position.",
  },
  {
    question: "How is this different from ValPak?",
    answer:
      "ValPak goes to 50,000 people who already have a dentist. The Front Porch goes to 1,500 to 2,000 new homeowners per issue who don\u2019t have anyone yet. No coupons. Your business as a trusted recommendation.",
  },
  {
    question: "I\u2019m a restaurant. Is this for me?",
    answer:
      "Every new resident asks where to eat within their first week. They\u2019re not loyal to anyone yet. The Front Porch is how they find you before they find your competitors.",
  },
  {
    question: "What if my category is already taken?",
    answer:
      "Then it\u2019s taken for the year. The businesses that move first get the strongest position. This is the urgency built into the model.",
  },
  {
    question: "Can I be in both publications?",
    answer:
      "Yes. Mortgage lenders, insurance companies, and home service providers often advertise in both. We offer combined pricing during your discovery call.",
  },
];

export default function FPFAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="bg-white px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-3xl">
        <p className="mb-4 text-center font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
          FREQUENTLY ASKED QUESTIONS
        </p>
        <div className="mx-auto mb-10 h-[3px] w-10 bg-grm-teal" />

        <div className="flex flex-col gap-3">
          {FAQS.map((faq, i) => (
            <div key={i} className="rounded-md bg-grm-cream">
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
