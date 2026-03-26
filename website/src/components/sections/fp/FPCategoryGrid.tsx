const CATEGORIES = [
  {
    group: "MEDICAL",
    items: ["Dentists", "Primary Care", "Pediatrics", "Eye Care", "Mental Health", "Med Spas"],
  },
  {
    group: "HOME SERVICES",
    items: ["HVAC", "Plumbing", "Electrical", "Pest Control", "Landscaping", "Pool Service"],
  },
  {
    group: "LIFESTYLE",
    items: ["Restaurants", "Gyms", "Salons", "Pet Services", "Auto Repair", "Dry Cleaners"],
  },
  {
    group: "FAMILY",
    items: ["Daycares", "Private Schools", "Tutoring", "Children\u2019s Activities", "Pediatric Dentist"],
  },
  {
    group: "MARION COUNTY",
    items: ["Equestrian Supply", "Farm Stores", "Golf Communities", "Outdoor Recreation"],
  },
];

export default function FPCategoryGrid() {
  return (
    <section className="bg-grm-cream px-6 py-20 lg:px-8">
      <div className="mx-auto max-w-5xl">
        <p className="mb-4 text-center font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
          WHO ADVERTISES IN THE FRONT PORCH
        </p>
        <div className="mx-auto mb-10 h-[3px] w-10 bg-grm-teal" />

        {/* Top row: 3 blocks */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {CATEGORIES.slice(0, 3).map((cat) => (
            <div
              key={cat.group}
              className="border-l-4 border-grm-teal bg-white py-5 pl-5 pr-4"
            >
              <h3 className="mb-3 font-comfortaa text-[12px] font-bold uppercase tracking-widest text-grm-black">
                {cat.group}
              </h3>
              <div className="flex flex-col gap-1.5">
                {cat.items.map((item) => (
                  <p
                    key={item}
                    className="font-nunito text-[15px] font-semibold text-grm-black/70"
                  >
                    {item}
                  </p>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Bottom row: 2 blocks centered */}
        <div className="mt-6 flex flex-col items-center gap-6 sm:flex-row sm:justify-center">
          {CATEGORIES.slice(3).map((cat) => (
            <div
              key={cat.group}
              className="w-full border-l-4 border-grm-teal bg-white py-5 pl-5 pr-4 sm:w-[calc(50%-12px)] lg:w-[calc(33.333%-16px)]"
            >
              <h3 className="mb-3 font-comfortaa text-[12px] font-bold uppercase tracking-widest text-grm-black">
                {cat.group}
              </h3>
              <div className="flex flex-col gap-1.5">
                {cat.items.map((item) => (
                  <p
                    key={item}
                    className="font-nunito text-[15px] font-semibold text-grm-black/70"
                  >
                    {item}
                  </p>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
