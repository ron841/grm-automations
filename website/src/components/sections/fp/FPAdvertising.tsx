import Link from "next/link";

const VALUE_PROPS = [
  {
    title: "Your business in the hands of every new homeowner.",
    body: "Your ad in a guide designed to be kept. Premium paper. Clean design. Useful content. When the AC breaks in July, they don\u2019t Google. They grab The Front Porch.",
  },
  {
    title: "Category positioning that means something.",
    body: "A few spots available per category, per year. Once a category fills, it is closed for the year. The dentist a new family finds in month one is probably their dentist for the next decade.",
  },
  {
    title: "Social media that follows them every month.",
    body: "Your ad lands in their mailbox in the first 60 days. Then your campaign runs through our social pages every month after that. Seen in the guide. Found on their phone. Chosen when they\u2019re ready.",
  },
];

export default function FPAdvertising() {
  return (
    <section id="advertising" className="bg-white px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-4xl">
        <h2 className="mb-4 text-center font-comfortaa text-[18px] font-bold uppercase leading-relaxed tracking-wide text-grm-teal lg:text-[22px]">
          SEEN IN THE GUIDE. FOUND ONLINE. CHOSEN AT THE RIGHT MOMENT.
        </h2>

        <div className="mx-auto mb-12 h-[3px] w-10 bg-grm-teal" />

        <div className="flex flex-col gap-10">
          {VALUE_PROPS.map((prop) => (
            <div key={prop.title} className="border-l-[3px] border-fp-rose pl-6">
              <h3 className="mb-2 font-merriweather text-xl font-bold text-grm-black">
                {prop.title}
              </h3>
              <p className="font-nunito text-base leading-[1.7] text-grm-black">
                {prop.body}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-12 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Link
            href="/contact"
            className="rounded-md bg-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
          >
            Let&apos;s Talk
          </Link>
          <Link
            href="/contact"
            className="rounded-md border-2 border-grm-teal px-8 py-3.5 font-nunito text-sm font-bold text-grm-teal transition-colors hover:bg-grm-teal hover:text-white"
          >
            Request the Media Kit
          </Link>
        </div>
      </div>
    </section>
  );
}
