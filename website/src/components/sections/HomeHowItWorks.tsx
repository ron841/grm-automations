const STEPS = [
  {
    number: "01",
    headline: "Print opens the door.",
    body: "Your business in a premium magazine that top agents and new homeowners actually read, share, and keep.",
  },
  {
    number: "02",
    headline: "Digital keeps it open.",
    body: "Your campaign runs as a collaboration through our social pages. Our audience. Your business. Third-party credibility no ad buy can replicate.",
  },
  {
    number: "03",
    headline: "Community makes it last.",
    body: "Events, features, and word-of-mouth turn one ad buy into something that compounds.",
  },
];

export default function HomeHowItWorks() {
  return (
    <section className="bg-white px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-[1100px]">
        {/* Label */}
        <p className="text-center font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
          THE MODEL
        </p>

        {/* Teal rule */}
        <div className="mx-auto mb-10 mt-4 h-[3px] w-10 bg-grm-teal" />

        {/* Three steps */}
        <div className="grid grid-cols-1 gap-12 md:grid-cols-3 md:gap-10">
          {STEPS.map((step) => (
            <div key={step.number} className="text-center md:text-left">
              <p className="font-merriweather text-[56px] font-bold leading-none text-grm-teal">
                {step.number}
              </p>
              <h3 className="mt-4 font-merriweather text-[22px] font-bold text-grm-black">
                {step.headline}
              </h3>
              <p className="mt-3 font-nunito text-base leading-[1.7] text-grm-black">
                {step.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
