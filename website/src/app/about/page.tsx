import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

export const metadata: Metadata = {
  title: "About | Get Rooted Media | Marion County, Florida",
  description:
    "A father and son. Thirty years in publishing and a front-row seat to the fastest-growing county in America. Meet Ron Kolb and Cameron Cowart.",
};

export default function AboutPage() {
  return (
    <main>
      {/* ───── SECTION 1: HERO + OPENING ───── */}
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

      {/* ───── TEAM PHOTOS BELOW HERO ───── */}
      <section className="bg-grm-cream px-6 py-16 lg:px-8">
        <div className="mx-auto flex max-w-md justify-center gap-8">
          <div className="text-center">
            <div className="relative mx-auto h-[200px] w-[200px] overflow-hidden rounded border-[3px] border-grm-teal">
              <Image
                src="/images/team/DSC01296.webp"
                alt="Ron Kolb, Founder and Publisher of Get Rooted Media"
                fill
                className="object-cover"
                sizes="200px"
              />
            </div>
            <p className="mt-4 font-merriweather text-lg font-bold text-grm-black">
              Ron Kolb
            </p>
            <p className="font-nunito text-sm text-grm-black/60">Founder and Publisher</p>
          </div>
          <div className="text-center">
            <div className="relative mx-auto h-[200px] w-[200px] overflow-hidden rounded border-[3px] border-grm-teal">
              <Image
                src="/images/team/DSC01234.webp"
                alt="Cameron Cowart, Co-Founder and Sales Director of Get Rooted Media"
                fill
                className="object-cover"
                sizes="200px"
              />
            </div>
            <p className="mt-4 font-merriweather text-lg font-bold text-grm-black">
              Cameron Cowart
            </p>
            <p className="font-nunito text-sm text-grm-black/60">
              Sales Director
            </p>
          </div>
        </div>
      </section>

      {/* ───── ORIGIN STORY ───── */}
      <section className="bg-grm-cream px-6 pb-20 lg:px-8">
        <div className="mx-auto max-w-[680px]">
          <p className="mb-6 font-merriweather text-lg leading-[1.8] text-grm-black">
            The road into Ocala looks the same as it always did.
          </p>
          <p className="mb-6 font-merriweather text-lg leading-[1.8] text-grm-black">
            The oaks still close over the highway the way they do nowhere else
            in Florida. The horse farms still roll out past the fence lines. But
            pull off anywhere and count the new rooftops and you understand
            quickly that something has shifted. Marion County added more than
            16,000 people last year. No metro in the country grew faster.
          </p>
          <p className="mb-6 font-merriweather text-lg leading-[1.8] text-grm-black">
            Ron Kolb knows this county the way you know a place you helped
            build.
          </p>
          <p className="mb-6 font-merriweather text-lg leading-[1.8] text-grm-black">
            He arrived in 1997, part of the team that helped Linda Marks
            transform a twenty-year digest called Ocala Today into a full city
            lifestyle publication. Ocala Magazine became the Magazine of the Year
            in Florida by 2004. Ron learned publishing here. What it means to
            tell a community&apos;s story back to itself. What it takes to earn
            the trust of the people whose names go on the cover.
          </p>
          <p className="mb-6 font-merriweather text-lg leading-[1.8] text-grm-black">
            Then he left. He spent twenty years building things across the
            country. Big things. He worked with the people who defined Florida
            regional publishing. He cofounded businesses that scaled across
            hundreds of markets. He lived in fifteen cities.
          </p>
          <p className="mb-6 font-merriweather text-lg leading-[1.8] text-grm-black">
            He always knew where home was.
          </p>
          <p className="mb-6 font-merriweather text-lg leading-[1.8] text-grm-black">
            Cameron Cowart was born and raised in Marion County. He is one of
            the top twenty real estate agents in the county, co-founder of Get
            Rooted Media, married, with a new baby at home. He knows this market the
            way you know a place you never left. The neighborhoods, the agents,
            the families putting down roots every week. He wanted to build
            something that gives back to the community he grew up in.
          </p>
          <p className="font-merriweather text-lg leading-[1.8] text-grm-black">
            When Ron came home, they built it together.
          </p>
        </div>
      </section>

      {/* ───── SECTION 2: THE GAP ───── */}
      <section className="bg-white px-6 py-20 lg:px-8">
        <div className="mx-auto max-w-[680px] text-center">
          <p className="mb-6 font-merriweather text-lg leading-[1.8] text-grm-black">
            Get Rooted Media exists because this county deserved it.
          </p>
          <p className="mb-6 font-merriweather text-lg leading-[1.8] text-grm-black">
            The agents who close the deals had no magazine celebrating their
            work. No publication that put the full deal team in the spotlight
            they deserve. The lenders, inspectors, title companies,
            photographers. Every person behind every closing.
          </p>
          <p className="mb-10 font-merriweather text-lg leading-[1.8] text-grm-black">
            The new homeowners arriving every week had no guide waiting for
            them. No curated answer to the question they all ask within their
            first 60 days: who do you use for everything?
          </p>
          <p className="font-merriweather text-[24px] font-bold leading-tight text-grm-black">
            The gap was wide open.
          </p>
          <p className="mt-2 font-merriweather text-[24px] font-bold leading-tight text-grm-black">
            They filled it.
          </p>
        </div>
      </section>

      {/* ───── SECTION 3: THE MISSION ───── */}
      <section className="bg-grm-cream px-6 py-[100px] lg:px-8">
        <div className="mx-auto max-w-[720px]">
          <div className="border-l-[4px] border-grm-teal pl-8">
            <p className="font-merriweather text-[22px] leading-relaxed text-grm-black">
              Communities don&apos;t build themselves. Someone has to make the
              introduction. Between the agent and the lender who should know each
              other. Between the new homeowner and the HVAC company they&apos;ll
              call for the next twenty years. Between the family that just moved
              here and the neighborhood that&apos;s been waiting for them. That
              someone is us.
            </p>
          </div>
        </div>
      </section>

      {/* ───── SECTION 4: WHAT WE BELIEVE ───── */}
      <section className="bg-white px-6 py-20 lg:px-8">
        <div className="mx-auto flex max-w-[680px] flex-col gap-16">
          <div>
            <p className="mb-3 font-merriweather text-xl font-bold text-grm-black">
              Print opens the door. Digital keeps it open. Community makes it
              last.
            </p>
            <p className="font-nunito text-[17px] leading-[1.7] text-grm-black">
              Our model is built on all three. No single channel builds the kind
              of trust that turns a new resident into a rooted one.
            </p>
          </div>

          <div className="mx-auto h-[2px] w-10 bg-grm-teal" />

          <div>
            <p className="mb-3 font-merriweather text-xl font-bold text-grm-black">
              We are not building a magazine.
            </p>
            <p className="font-nunito text-[17px] leading-[1.7] text-grm-black">
              We are building something that makes this county work better for
              the people who live here. Marion County is where we start. But
              this model was built to travel.
            </p>
          </div>

          <div className="mx-auto h-[2px] w-10 bg-grm-teal" />

          <div>
            <p className="mb-3 font-merriweather text-xl font-bold text-grm-black">
              The best business still happens when people feel connected to where
              they live.
            </p>
            <p className="font-nunito text-[17px] leading-[1.7] text-grm-black">
              Not through algorithms. Not through ads that disappear in half a
              second. Through something you can hold in your hands, trust with
              your decisions, and keep on the counter because it actually helped
              you find your people.
            </p>
          </div>
        </div>
      </section>

      {/* ───── SECTION 5: THE TEAM BIOS ───── */}
      <section className="bg-grm-cream px-6 py-20 lg:px-8">
        <div className="mx-auto max-w-5xl">
          <p className="mb-10 text-center font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
            THE TEAM
          </p>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
            {/* Ron */}
            <div className="rounded bg-white p-10 shadow-sm">
              <div className="relative mx-auto mb-6 h-[200px] w-[200px] overflow-hidden rounded border-[3px] border-grm-teal">
                <Image
                  src="/images/team/DSC01296.webp"
                  alt="Ron Kolb, Founder and Publisher"
                  fill
                  className="object-cover"
                  sizes="200px"
                />
              </div>
              <h3 className="text-center font-merriweather text-xl font-bold text-grm-black">
                Ron Kolb
              </h3>
              <p className="mb-6 text-center font-nunito text-sm text-grm-black/60">
                Publisher
              </p>
              <p className="font-nunito text-base leading-[1.7] text-grm-black">
                Ron has spent his career in sales. Not the kind where you read a
                script. The kind where you sit across the table from a business
                owner, listen to what they actually need, and figure out how to
                make it work. He helped build Marion County&apos;s flagship
                publication from the ground up. He went out and built things at a
                different scale. He came home to build something worth staying
                for.
              </p>
            </div>

            {/* Cameron */}
            <div className="rounded bg-white p-10 shadow-sm">
              <div className="relative mx-auto mb-6 h-[200px] w-[200px] overflow-hidden rounded border-[3px] border-grm-teal">
                <Image
                  src="/images/team/DSC01234.webp"
                  alt="Cameron Cowart, Co-Founder and Sales Director"
                  fill
                  className="object-cover"
                  sizes="200px"
                />
              </div>
              <h3 className="text-center font-merriweather text-xl font-bold text-grm-black">
                Cameron Cowart
              </h3>
              <p className="mb-6 text-center font-nunito text-sm text-grm-black/60">
                Co-Founder and Sales Director
              </p>
              <p className="font-nunito text-base leading-[1.7] text-grm-black">
                Cameron grew up in this market. He knows the agents, the
                neighborhoods, the places that make Marion County worth moving
                to. He walks into a meeting with the conviction of someone who
                believes in what he is selling. You can tell it the
                moment he starts talking. He is here to connect every business that
                belongs in these magazines with the readers who need to find
                them.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ───── SECTION 6: FINAL CTA ───── */}
      <section className="bg-white px-6 py-20 lg:px-8">
        <div className="mx-auto max-w-[640px] text-center">
          <h2 className="mb-4 font-merriweather text-[28px] font-bold leading-tight text-grm-black">
            We&apos;d rather show you than tell you.
          </h2>
          <p className="mb-10 font-nunito text-lg text-grm-black/70">
            Book 15 minutes with Ron or Cameron. We&apos;ll walk you through the
            magazines, the audience, and exactly how it works for your business.
            No pitch. No pressure.
          </p>
          <Link
            href="/contact"
            className="inline-block rounded-md bg-grm-teal px-10 py-4 font-nunito text-base font-bold text-white transition-opacity hover:opacity-90"
          >
            Let&apos;s Talk
          </Link>
          <p className="mt-4">
            <Link
              href="/contact"
              className="font-nunito text-sm text-grm-teal no-underline transition-colors hover:underline"
            >
              or request our media kit
            </Link>
          </p>
        </div>
      </section>
    </main>
  );
}
