import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Let's Talk | Get Rooted Media | Marion County, Florida",
  description:
    "Book 15 minutes with Ron or Cameron. We'll walk you through the magazines, the audience, and exactly how it works for your business.",
};

export default function ContactPage() {
  return (
    <main>
      {/* ───── HEADLINE ───── */}
      <section className="bg-white px-6 pt-[120px] pb-12 lg:px-8 lg:pt-[140px]">
        <div className="mx-auto max-w-2xl text-center">
          <p className="mb-4 font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
            LET&apos;S TALK
          </p>
          <h1 className="mb-4 font-merriweather text-[32px] font-bold leading-tight text-grm-black lg:text-[40px]">
            Book 15 minutes with Ron or Cameron.
          </h1>
          <p className="font-nunito text-lg text-grm-black/70">
            We&apos;ll walk you through the magazines, the audience, and exactly
            how it works for your business. No pitch. No pressure.
          </p>
        </div>
      </section>

      {/* ───── CALENDLY PLACEHOLDER ───── */}
      <section className="bg-white px-6 pb-20 lg:px-8">
        <div className="mx-auto max-w-3xl">
          <div
            id="calendly-embed"
            className="flex min-h-[600px] items-center justify-center rounded-md bg-grm-cream"
          >
            <p className="px-6 text-center font-nunito text-base italic text-grm-teal">
              Calendly booking widget — configure before launch
            </p>
          </div>
        </div>
      </section>

      {/* ───── DIRECT CONTACT ───── */}
      <section className="bg-grm-cream px-6 py-16 lg:px-8">
        <div className="mx-auto max-w-2xl">
          <div className="grid grid-cols-1 gap-10 sm:grid-cols-2">
            <div className="text-center">
              <a
                href="mailto:ron@getrootedmedia.com"
                className="font-nunito text-lg font-semibold text-grm-teal transition-opacity hover:opacity-80"
              >
                ron@getrootedmedia.com
              </a>
              <p className="mt-2 font-merriweather text-base font-bold text-grm-black">
                Ron Kolb
              </p>
              <p className="font-nunito text-sm text-grm-black/60">
                Founder and Publisher
              </p>
            </div>
            <div className="text-center">
              <a
                href="mailto:cameron@getrootedmedia.com"
                className="font-nunito text-lg font-semibold text-grm-teal transition-opacity hover:opacity-80"
              >
                cameron@getrootedmedia.com
              </a>
              <p className="mt-2 font-merriweather text-base font-bold text-grm-black">
                Cameron Cowart
              </p>
              <p className="font-nunito text-sm text-grm-black/60">
                Co-Founder and Sales Director
              </p>
            </div>
          </div>

          {/* Media kit links */}
          <p className="mt-12 text-center font-nunito text-base text-grm-black/70">
            Prefer a media kit first? Download{" "}
            <Link
              href="/contact"
              className="text-grm-teal no-underline hover:underline"
            >
              The Closing Table media kit
            </Link>{" "}
            or{" "}
            <Link
              href="/contact"
              className="text-grm-teal no-underline hover:underline"
            >
              The Front Porch media kit
            </Link>
            .
          </p>
        </div>
      </section>
    </main>
  );
}
