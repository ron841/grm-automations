"use client";

import { useState } from "react";

export default function FPReaderSignup() {
  const [submitted, setSubmitted] = useState(false);

  return (
    <section id="reader-signup" className="bg-grm-cream px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-[480px]">
        <div className="border-l-[3px] border-grm-teal p-8 lg:p-10">
          <h2 className="mb-2 font-comfortaa text-[22px] font-bold uppercase tracking-wide text-grm-black">
            NEW TO MARION COUNTY?
          </h2>

          <p className="mb-2 font-nunito text-base text-grm-black">
            The Front Porch launches July 2026.
          </p>

          <p className="mb-8 font-nunito text-base leading-relaxed text-grm-black/70">
            Sign up to have it delivered to your mailbox when it ships.
            We&apos;ll send the guide as soon as it&apos;s off the press, plus a
            few local recommendations to hold you over in the meantime.
          </p>

          {submitted ? (
            <p className="font-nunito text-base font-semibold text-grm-teal">
              You&apos;re signed up. Welcome to Marion County.
            </p>
          ) : (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                setSubmitted(true);
              }}
              className="flex flex-col gap-4"
            >
              <input
                type="text"
                name="name"
                placeholder="Your Name"
                required
                className="rounded-md border border-grm-black/15 bg-grm-cream px-4 py-3 font-nunito text-sm text-grm-black placeholder:text-grm-black/40 focus:border-grm-teal focus:outline-none"
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                required
                className="rounded-md border border-grm-black/15 bg-grm-cream px-4 py-3 font-nunito text-sm text-grm-black placeholder:text-grm-black/40 focus:border-grm-teal focus:outline-none"
              />
              <input
                type="text"
                name="address"
                placeholder="Mailing Address"
                required
                className="rounded-md border border-grm-black/15 bg-grm-cream px-4 py-3 font-nunito text-sm text-grm-black placeholder:text-grm-black/40 focus:border-grm-teal focus:outline-none"
              />
              <button
                type="submit"
                className="mt-2 rounded-[2px] bg-grm-teal px-6 py-3 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
              >
                Sign Me Up
              </button>
            </form>
          )}
        </div>
      </div>
    </section>
  );
}
