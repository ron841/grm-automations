import Link from "next/link";

export default function HomeFinalCTA() {
  return (
    <section className="bg-grm-cream px-6 py-[120px] lg:px-8">
      <div className="mx-auto max-w-[640px] text-center">
        <p className="mb-4 font-nunito text-xl text-grm-black">
          The first issue is being built right now.
        </p>
        <p className="mb-4 font-nunito text-xl text-grm-black">
          The businesses who come in now are not just buying ad space.
        </p>
        <p className="font-nunito text-xl text-grm-black">
          After Issue 1, you&apos;re an advertiser.
        </p>

        <p className="mt-8 font-merriweather text-[28px] font-bold leading-tight text-grm-black">
          Right now, you&apos;re a founding partner.
        </p>

        <Link
          href="/contact"
          className="mt-10 inline-block rounded-md bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
        >
          Let&apos;s Talk
        </Link>
      </div>
    </section>
  );
}
