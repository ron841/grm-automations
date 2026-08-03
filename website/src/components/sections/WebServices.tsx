import Link from "next/link";

export default function WebServices() {
  return (
    <section className="bg-grm-black text-white">
      <div className="mx-auto max-w-3xl px-8 py-20 md:px-12 md:py-28">
        <div className="mb-7">
          <span className="font-comfortaa text-[12px] uppercase tracking-[0.18em] text-grm-teal">
            The Storefront · Marion County
          </span>
          <div className="mt-2 h-px w-8 bg-grm-teal" />
        </div>

        <h2 className="font-merriweather text-[32px] leading-[1.15] md:text-[44px] md:leading-[1.1]">
          The Storefront
        </h2>

        <p className="mt-6 font-merriweather italic text-[18px] leading-[1.5] text-white/85 md:text-[20px]">
          We build it. We host it. We update it. You answer the phone.
        </p>

        <div className="mt-9 space-y-6 font-nunito text-[16px] leading-[1.7] text-white/75 md:text-[17px]">
          <p>
            You spent thirty years building a real business in Marion County.
            Hundreds of five-star reviews. A name people in Ocala already trust.
            Then you look at your website and it was built in 2013 and never
            touched again.
          </p>

          <p>
            That is most local businesses here. Real reputations, bad
            websites, a phone book full of vendors who all sound the same and
            all build the same WordPress template at the same price.
          </p>

          <p>
            We build differently. Modern frameworks that load in under two
            seconds. SEO and GEO woven into the foundation so Google finds you
            and AI search recommends you. Migration done the right way so fifty
            years of Google equity moves with you instead of disappearing the
            day the new site goes live.
          </p>
        </div>

        <div className="mt-10">
          <Link
            href="/the-storefront"
            className="font-comfortaa text-[13px] uppercase tracking-[0.18em] text-grm-teal hover:text-white transition-colors"
          >
            See a free preview built for your business &rarr;
          </Link>
        </div>
      </div>
    </section>
  );
}
