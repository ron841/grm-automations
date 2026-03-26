import type { Metadata } from "next";
import Image from "next/image";

export const metadata: Metadata = {
  title: "Let's Talk | Get Rooted Media | Marion County, Florida",
  description:
    "Book 15 minutes with Ron or Cameron. We'll show you who reads it, what it costs, and whether it's the right fit.",
};

export default function ContactPage() {
  return (
    <main className="flex min-h-screen flex-col md:flex-row">
      {/* LEFT — dark with image (appears second on mobile) */}
      <div className="relative order-2 min-h-[50vh] w-full md:order-1 md:min-h-screen md:w-1/2">
        <Image
          src="/images/hero/4-Ocala-2.webp"
          alt="Tuscawilla Park in Ocala with Spanish moss and lake reflection at golden hour"
          fill
          priority
          className="object-cover object-center"
          sizes="(max-width: 768px) 100vw, 50vw"
        />
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(to bottom, rgba(0,0,0,0.45) 0%, rgba(0,0,0,0.65) 100%)",
          }}
        />
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(to right, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.1) 100%)",
          }}
        />

        <div className="relative z-10 flex h-full min-h-[50vh] flex-col justify-center px-8 py-10 md:min-h-screen md:px-14 md:py-16">
          <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.2em] text-grm-teal">
            GET ROOTED MEDIA
          </p>
          <div className="mb-7 h-px w-8 bg-grm-teal" />
          <p className="mb-12 max-w-[400px] font-merriweather text-[22px] italic leading-[1.4] text-white md:text-[28px]">
            We&apos;d rather show you than tell you. Fifteen minutes and
            you&apos;ll know exactly whether this is right for your business.
          </p>

          {/* Ron */}
          <div>
            <p className="font-merriweather text-[15px] font-bold text-white">
              Ron Kolb
            </p>
            <p className="mt-1 font-comfortaa text-[10px] font-bold uppercase tracking-[0.12em] text-grm-teal">
              FOUNDER AND PUBLISHER
            </p>
            <a
              href="mailto:ron@getrootedmedia.com"
              className="mt-1.5 inline-block font-nunito text-[13px] text-white/65 transition-colors hover:text-white/90"
            >
              ron@getrootedmedia.com
            </a>
          </div>

          <div className="my-5 h-px w-full max-w-[200px] bg-white/12" />

          {/* Cameron */}
          <div>
            <p className="font-merriweather text-[15px] font-bold text-white">
              Cameron Cowart
            </p>
            <p className="mt-1 font-comfortaa text-[10px] font-bold uppercase tracking-[0.12em] text-grm-teal">
              CO-FOUNDER &middot; DIRECTOR OF SALES
            </p>
            <a
              href="mailto:cameron@getrootedmedia.com"
              className="mt-1.5 inline-block font-nunito text-[13px] text-white/65 transition-colors hover:text-white/90"
            >
              cameron@getrootedmedia.com
            </a>
          </div>
        </div>
      </div>

      {/* RIGHT — cream booking column (appears first on mobile) */}
      <div className="order-1 flex min-h-[50vh] w-full items-center bg-grm-cream md:order-2 md:min-h-screen md:w-1/2">
        <div className="w-full px-8 py-10 md:px-14 md:py-16">
          <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.2em] text-grm-teal">
            LET&apos;S TALK
          </p>
          <div className="mb-7 h-px w-8 bg-grm-teal" />
          <h1 className="mb-5 font-merriweather text-[32px] font-bold leading-[1.2] text-grm-black md:text-[40px]">
            Book 15 minutes with Ron or Cameron.
          </h1>
          <p className="mb-10 max-w-[380px] font-nunito text-[16px] leading-[1.75] text-grm-black/65">
            We&apos;ll show you who reads it, what it costs, and whether
            it&apos;s the right fit. No pitch. No pressure.
          </p>
          <a
            href="https://cal.com/ron-kolb-cdlgsw/30min"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block rounded-[2px] bg-grm-teal px-12 py-4 font-nunito text-[15px] font-bold text-white transition-colors duration-200 hover:bg-[#3da0b5]"
          >
            Book a Call
          </a>
          <p className="mt-4 font-nunito text-[13px] text-grm-black/50">
            or email us directly &mdash;{" "}
            <a
              href="mailto:ron@getrootedmedia.com"
              className="text-grm-black/50 transition-colors hover:text-grm-black"
            >
              ron@getrootedmedia.com
            </a>
          </p>
        </div>
      </div>
    </main>
  );
}
