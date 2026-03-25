export default function CTIssuePreview() {
  return (
    <section className="bg-grm-black px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-3xl text-center">
        <p className="mb-4 font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
          ISSUE 1 &middot; JUNE 2026
        </p>
        <div className="mx-auto mb-10 h-[3px] w-10 bg-grm-teal" />

        <h2 className="mb-8 font-merriweather text-[28px] font-bold leading-tight text-white lg:text-[36px]">
          &ldquo;I Didn&apos;t Build a Team. I Built a Referral System.&rdquo;
        </h2>

        <p className="mb-6 font-nunito text-lg leading-relaxed text-white/80">
          She&apos;s closed more than $35 million in the last 18 months. No
          Facebook ads. No Zillow leads. No cold calls.
        </p>

        <p className="mb-10 font-nunito text-lg leading-relaxed text-white/80">
          What she does: she makes sure every lender, title rep, inspector, and
          attorney she works with knows exactly when she has a client who needs
          them. And they do the same for her.
        </p>

        {/* Pull quote */}
        <div className="mx-auto max-w-xl border-l-[3px] border-grm-teal py-2 pl-6 text-left">
          <p className="font-merriweather text-xl italic leading-relaxed text-grm-teal">
            &ldquo;I&apos;ve been in this market for 22 years. I&apos;ve never
            seen a publication that actually understood what we do until
            now.&rdquo;
          </p>
          <p className="mt-3 font-nunito text-sm text-white/60">
            A Marion County Top Producer
          </p>
        </div>

        <p className="mx-auto mt-10 max-w-md font-merriweather text-base italic text-white/60">
          People call it a referral network. I call it a closing table. Everyone
          has a seat. Everyone eats.
        </p>
      </div>
    </section>
  );
}
