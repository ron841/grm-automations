export default function HomeStory() {
  return (
    <section className="bg-white px-6 pt-[120px] pb-20 lg:px-8">
      <div className="mx-auto max-w-[680px] text-center">
        {/* Label */}
        <p className="font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
          OUR STORY
        </p>

        {/* Teal rule */}
        <div className="mx-auto mb-4 mt-4 h-[3px] w-10 bg-grm-teal" />

        {/* Headline */}
        <h2 className="mb-10 font-merriweather text-[32px] font-bold leading-tight text-grm-black">
          Here&apos;s what nobody tells you about buying a home.
        </h2>

        {/* Body */}
        <p className="mb-6 font-nunito text-lg leading-[1.8] text-grm-black">
          The agent finds you the house. The lender makes the numbers work. The
          inspector gives you the green light. The title company handles the
          paperwork. And then one afternoon, you&apos;re standing in a kitchen
          that&apos;s yours, holding a set of keys. The entire team that got you
          there has moved on to their next deal.
        </p>

        <p className="font-nunito text-lg leading-[1.8] text-grm-black">
          Now you need a doctor. Your kid needs a school. Your AC is going to run
          ten months a year in Florida and you don&apos;t know a single HVAC
          company. You need a dentist, a good restaurant for date night, a vet
          for your dog.
        </p>

        {/* Final line */}
        <p className="mt-8 font-merriweather text-[28px] font-bold leading-tight text-grm-black">
          You don&apos;t know anyone yet.
        </p>
      </div>
    </section>
  );
}
