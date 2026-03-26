import type { Metadata } from "next";
import Image from "next/image";

export const metadata: Metadata = {
  title: "About | Get Rooted Media | Marion County, Florida",
  description:
    "A father and son. Thirty years in publishing and a front-row seat to the fastest-growing county in America. Meet Ron Kolb and Cameron Cowart.",
};

export default function AboutPage() {
  return (
    <main>
      {/* ───── HERO ───── */}
      <section className="relative min-h-[70vh] bg-grm-black">
        <Image
          src="/images/hero/4-Ocala-2.webp"
          alt="Tuscawilla Park in Ocala with Spanish moss and lake reflection at golden hour"
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/40 to-black/60" />
        <div className="relative z-10 flex min-h-[70vh] items-end px-6 pb-20 pt-[120px] lg:px-8">
          <div className="mx-auto max-w-3xl text-center">
            <p className="mb-4 font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
              LOCALLY ROOTED. PROFESSIONALLY GROWN.
            </p>
            <h1 className="font-merriweather text-[36px] font-bold leading-tight text-white lg:text-[48px]">
              We&apos;re a father and son.
            </h1>
            <p className="mt-4 font-nunito text-xl text-white/80">
              Between us, thirty years in publishing and a front-row seat to the
              fastest-growing county in America.
            </p>
          </div>
        </div>
      </section>

      {/* ───── SECTION 1: RON — photo left, story right ───── */}
      <section className="flex flex-col md:flex-row">
        <div className="relative min-h-[380px] w-full md:min-h-[520px] md:w-[52%]">
          <Image
            src="/images/team/DSC01569.webp"
            alt="Ron Kolb, Founder and Publisher of Get Rooted Media"
            fill
            className="object-cover object-top"
            sizes="(max-width: 768px) 100vw, 52vw"
          />
          <div
            className="absolute inset-0"
            style={{
              background:
                "linear-gradient(to right, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.55) 100%)",
            }}
          />
          <div className="absolute bottom-0 left-0 p-8 md:p-10">
            <p className="font-merriweather text-[28px] font-bold text-white">
              Ron Kolb
            </p>
            <p className="mt-2 font-comfortaa text-[11px] font-bold uppercase tracking-[0.15em] text-grm-teal">
              Founder and Publisher
            </p>
          </div>
        </div>

        <div className="flex w-full items-center bg-grm-cream md:w-[48%]">
          <div className="p-8 md:px-12 md:py-14">
            <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.2em] text-grm-teal">
              THE PUBLISHER
            </p>
            <div className="mb-6 h-px w-8 bg-grm-teal" />
            <p className="mb-4 font-merriweather text-[16px] leading-[1.8] text-grm-black">
              Ron Kolb knows this county the way you know a place you helped
              build.
            </p>
            <p className="mb-4 font-merriweather text-[16px] leading-[1.8] text-grm-black">
              He arrived in 1997, part of the team that helped Linda Marks
              transform a twenty-year digest called Ocala Today into a full city
              lifestyle publication. Ocala Magazine became the Magazine of the
              Year in Florida by 2004. Ron learned publishing here. What it
              means to tell a community&apos;s story back to itself. What it
              takes to earn the trust of the people whose names go on the cover.
            </p>
            <p className="font-merriweather text-[16px] leading-[1.8] text-grm-black">
              Then he left. He spent twenty years building things across the
              country. He always knew where home was.
            </p>
          </div>
        </div>
      </section>

      {/* ───── SECTION 2: CAMERON — story left, photo right ───── */}
      <section className="flex flex-col md:flex-row">
        <div className="flex w-full items-center bg-grm-cream md:w-[48%]">
          <div className="p-8 md:px-12 md:py-14">
            <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.2em] text-grm-teal">
              THE DIRECTOR OF SALES
            </p>
            <div className="mb-6 h-px w-8 bg-grm-teal" />
            <p className="mb-4 font-merriweather text-[16px] leading-[1.8] text-grm-black">
              Cameron Cowart was born and raised in Marion County. He is one of
              the top twenty real estate agents in the county. He knows this
              market the way you know a place you never left. The neighborhoods,
              the agents, the families putting down roots every week.
            </p>
            <p className="font-merriweather text-[16px] leading-[1.8] text-grm-black">
              He wanted to build something that gives back to the community he
              grew up in. He walks into a meeting with the conviction of someone
              who believes in what he is selling. You can tell it the moment he
              starts talking.
            </p>
          </div>
        </div>

        <div className="relative min-h-[380px] w-full md:min-h-[480px] md:w-[52%]">
          <Image
            src="/images/team/DSC01209.webp"
            alt="Cameron Cowart, Co-Founder and Director of Sales at Get Rooted Media"
            fill
            className="object-cover object-top"
            sizes="(max-width: 768px) 100vw, 52vw"
          />
          <div
            className="absolute inset-0"
            style={{
              background:
                "linear-gradient(to left, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.55) 100%)",
            }}
          />
          <div className="absolute bottom-0 right-0 p-8 text-right md:p-10">
            <p className="font-merriweather text-[28px] font-bold text-white">
              Cameron Cowart
            </p>
            <p className="mt-2 font-comfortaa text-[11px] font-bold uppercase tracking-[0.15em] text-grm-teal">
              Co-Founder and Director of Sales
            </p>
          </div>
        </div>
      </section>

      {/* ───── SECTION 3: WHY WE BUILT THIS ───── */}
      <section className="bg-grm-black px-8 py-16 md:px-20 md:py-20">
        <div className="mx-auto max-w-5xl text-center">
          <p className="mb-4 font-comfortaa text-[10px] font-bold uppercase tracking-[0.2em] text-grm-teal">
            WHY WE BUILT THIS
          </p>
          <div className="mx-auto mb-12 h-px w-10 bg-grm-teal" />

          <p className="mx-auto mb-12 max-w-[760px] font-merriweather text-[24px] italic leading-[1.4] text-white md:text-[32px]">
            Get Rooted Media exists because this county deserved it.
          </p>

          <div className="mx-auto grid max-w-4xl grid-cols-1 gap-8 text-left md:grid-cols-2 md:gap-12">
            <p className="font-nunito text-[15px] leading-[1.8] text-white/70">
              The agents who close the deals had no magazine celebrating their
              work. No publication that put the full deal team in the spotlight
              they deserve. The lenders, inspectors, title companies,
              photographers. Every person behind every closing.
            </p>
            <p className="font-nunito text-[15px] leading-[1.8] text-white/70">
              The new homeowners arriving every week had no guide waiting for
              them. No real answer to the question they all ask within their
              first 60 days: who do you use for everything?
            </p>
          </div>
        </div>
      </section>

      {/* ───── SECTION 4: CLOSING CTA ───── */}
      <section className="bg-grm-black px-8 pb-[100px] pt-0 md:px-20">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mx-auto mb-14 h-px w-20 bg-white/10" />

          <h2 className="mx-auto mb-5 max-w-[640px] font-merriweather text-[32px] font-bold leading-[1.2] text-white md:text-[42px]">
            We&apos;d rather show you than tell you.
          </h2>
          <p className="mx-auto mb-10 max-w-[480px] font-nunito text-[16px] leading-[1.75] text-white/65">
            Book 15 minutes with Ron or Cameron. We&apos;ll walk you through
            the magazines, the audience, and exactly how it works for your
            business. No pitch. No pressure.
          </p>
          <a
            href="https://cal.com/ron-kolb-cdlgsw/30min"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block rounded-[2px] bg-grm-teal px-12 py-4 font-nunito text-[15px] font-bold text-white transition-colors duration-200 hover:bg-[#3da0b5]"
          >
            Let&apos;s Talk
          </a>
          <p className="mt-4">
            <span className="cursor-pointer font-nunito text-[13px] text-grm-teal no-underline transition-colors hover:underline">
              or request our media kit
            </span>
          </p>
        </div>
      </section>
    </main>
  );
}
