import Link from "next/link";

export default function CTAgentCallout() {
  return (
    <section className="bg-grm-cream px-6 py-16 lg:px-8">
      <div className="mx-auto max-w-3xl">
        <div className="rounded-md border-2 border-grm-teal bg-grm-cream p-8 lg:p-12">
          <h2 className="mb-4 font-comfortaa text-[22px] font-bold uppercase tracking-wide text-grm-black lg:text-[26px]">
            ARE YOU A TOP-PRODUCING AGENT?
          </h2>

          <p className="mb-4 font-nunito text-lg leading-relaxed text-grm-black">
            We&apos;re selecting cover stories and agent profiles for Issue 1.
          </p>

          <p className="mb-8 font-nunito text-lg leading-relaxed text-grm-black">
            If you&apos;re one of Marion County&apos;s top producers and you
            want your story told as a real editorial piece about how you built
            your business, we want to hear from you.
          </p>

          <Link
            href="/contact"
            className="inline-block rounded-md border-2 border-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-grm-teal transition-colors hover:bg-grm-teal hover:text-white"
          >
            Tell Us Your Story
          </Link>
        </div>
      </div>
    </section>
  );
}
