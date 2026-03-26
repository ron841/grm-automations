export default function FP60DayWindow() {
  return (
    <section className="bg-grm-cream px-6 py-[100px] lg:px-8">
      <div className="mx-auto max-w-[680px] text-center">
        <p className="mb-4 font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
          THE 60-DAY WINDOW
        </p>
        <div className="mx-auto mb-10 h-[3px] w-10 bg-grm-teal" />

        <p className="mb-6 font-nunito text-lg leading-[1.8] text-grm-black">
          Every two months, 1,500 to 2,000 people buy a home in Marion County.
        </p>

        <p className="mb-6 font-nunito text-lg leading-[1.8] text-grm-black">
          In their first 60 days, they will choose a doctor, a dentist, an HVAC
          company, a landscaper, a pest control service, a gym, a restaurant for
          date night, and dozens of other businesses they&apos;ll use for years.
          Possibly decades.
        </p>

        <p className="mb-10 font-nunito text-lg leading-[1.8] text-grm-black">
          318 people moved here last week. And the week before that. And the week
          before that.
        </p>

        {/* Pull quote */}
        <div className="mx-auto max-w-lg border-l-[4px] border-grm-teal py-2 pl-6 text-left">
          <p className="font-merriweather text-[28px] font-bold leading-tight text-grm-black lg:text-[32px]">
            Google gives them 50 options. The Front Porch gives them yours.
          </p>
        </div>

        <p className="mt-10 font-merriweather text-xl italic text-grm-teal">
          Before Google. Before a neighbor&apos;s recommendation. Before anyone
          else.
        </p>
      </div>
    </section>
  );
}
