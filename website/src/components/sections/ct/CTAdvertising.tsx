import Link from "next/link";

const VALUE_PROPS = [
  {
    title: "A premium print ad in every issue.",
    body: "Your ad in a magazine that sits on desks, gets passed around offices, and stays in the hands of the people who refer business. A social post disappears in 0.3 seconds. A magazine gets picked up four to five times.",
  },
  {
    title: "Social media collaboration through our pages.",
    body: "Your campaign runs through The Closing Table\u2019s Instagram and Facebook pages, not yours. When agents see your business in their feed, they see a recommendation from the publication they already trust.",
  },
  {
    title: "Two mixers and one annual awards gala.",
    body: "Every advertiser receives two complimentary tickets. Your brand on the invite, your name in the room with the top 500 agents and service companies in Marion and Sumter Counties.",
  },
];

export default function CTAdvertising() {
  return (
    <section className="bg-white px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-4xl">
        {/* Headline */}
        <h2 className="mb-4 text-center font-comfortaa text-[18px] font-bold uppercase leading-relaxed tracking-wide text-grm-teal lg:text-[22px]">
          SEEN IN THE MAGAZINE. FOUND ONLINE. CHOSEN AT THE TIME OF PURCHASE.
        </h2>

        <p className="mx-auto mb-12 max-w-xl text-center font-nunito text-lg text-grm-black">
          Print. Social. Events. All of it running through us, all year long.
        </p>

        {/* Value props */}
        <div className="flex flex-col gap-10">
          {VALUE_PROPS.map((prop) => (
            <div key={prop.title} className="border-l-[3px] border-grm-teal pl-6">
              <h3 className="mb-2 font-merriweather text-xl font-bold text-grm-black">
                {prop.title}
              </h3>
              <p className="font-nunito text-base leading-[1.7] text-grm-black">
                {prop.body}
              </p>
            </div>
          ))}
        </div>

        {/* Buttons */}
        <div className="mt-12 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Link
            href="/contact"
            className="rounded-md bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
          >
            Let&apos;s Talk About Advertising
          </Link>
          <Link
            href="/contact"
            className="rounded-md border-2 border-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-grm-teal transition-colors hover:bg-grm-teal hover:text-white"
          >
            Download the Media Kit
          </Link>
        </div>
      </div>
    </section>
  );
}
