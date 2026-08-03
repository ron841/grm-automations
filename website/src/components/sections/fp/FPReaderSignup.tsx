"use client";

import { useState } from "react";

export default function FPReaderSignup() {
  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");
  const submitted = status === "success";

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);

    setStatus("submitting");
    try {
      const res = await fetch("https://formspree.io/f/meepogwz", {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" },
      });
      setStatus(res.ok ? "success" : "error");
    } catch {
      setStatus("error");
    }
  }

  return (
    <section id="reader-signup" className="bg-grm-cream px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-[480px]">
        <div className="border-l-[3px] border-grm-teal p-8 lg:p-10">
          <h2 className="mb-2 font-comfortaa text-[22px] font-bold uppercase tracking-wide text-grm-black">
            NEW TO MARION COUNTY?
          </h2>

          <p className="mb-2 font-nunito text-base text-grm-black">
            The Front Porch launches this November.
          </p>

          <p className="mb-8 font-nunito text-base leading-relaxed text-grm-black/70">
            Sign up and we&apos;ll mail it to you the day it ships.
          </p>

          {submitted ? (
            <div>
              <p className="font-merriweather text-[18px] italic leading-[1.6] text-grm-black">
                You&apos;re on the list. We&apos;ll have it in your mailbox when
                Issue 1 ships.
              </p>
              <div className="mt-6 h-px w-8 bg-grm-teal" />
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <input type="hidden" name="_subject" value="New Front Porch Signup — getrootedmedia.com" />
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
              {status === "error" && (
                <p role="alert" className="font-nunito text-sm text-[#b3261e]">
                  Something went wrong. Try again or email ron@getrootedmedia.com.
                </p>
              )}
              <button
                type="submit"
                disabled={status === "submitting"}
                className="mt-2 rounded-[2px] bg-grm-teal px-6 py-3 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90 disabled:opacity-60"
              >
                {status === "submitting" ? "Sending…" : "Sign Me Up"}
              </button>
            </form>
          )}
        </div>
      </div>
    </section>
  );
}
