import Image from "next/image";

export default function HomeStory() {
  return (
    <section id="our-story" className="flex flex-col md:flex-row">
      {/* LEFT COLUMN — dark with image (appears second on mobile) */}
      <div className="relative order-2 min-h-[380px] w-full md:order-1 md:min-h-[560px] md:w-[55%]">
        <Image
          src="/images/hero/4-Ocala-2.webp"
          alt="Downtown Ocala, Marion County"
          fill
          className="object-cover object-center"
          sizes="(max-width: 768px) 100vw, 55vw"
        />
        {/* Top-to-bottom overlay */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.3) 100%)",
          }}
        />
        {/* Left-to-right overlay */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(to right, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.1) 100%)",
          }}
        />

        {/* Content — upper-left */}
        <div className="relative z-10 flex h-full flex-col justify-start p-8 md:p-14">
          <div className="max-w-[480px]">
            <p className="mb-3.5 font-comfortaa text-[10px] font-bold uppercase tracking-[0.2em] text-grm-teal">
              OUR STORY
            </p>
            <div className="mb-7 h-px w-8 bg-grm-teal" />
            <h2 className="font-merriweather text-[28px] font-normal italic leading-[1.25] text-white md:text-[38px]">
              Here&apos;s what nobody tells you about buying a home.
            </h2>
            <p className="mt-6 font-nunito text-[15px] leading-[1.75] text-white/75">
              The agent finds you the house. The lender makes the numbers work.
              The title company handles the paperwork. And then one afternoon,
              you&apos;re standing in a kitchen that&apos;s yours, holding a set
              of keys. The entire team that got you there has moved on to their
              next deal.
            </p>
          </div>
        </div>
      </div>

      {/* RIGHT COLUMN — warm cream (appears first on mobile) */}
      <div className="order-1 flex min-h-[380px] w-full items-center bg-grm-cream md:order-2 md:min-h-[560px] md:w-[45%]">
        <div className="p-8 md:px-12 md:py-14">
          <p className="mb-7 font-merriweather text-[20px] font-bold leading-[1.5] text-grm-black md:text-[26px]">
            Now you need a doctor. Your kid needs a school. Your AC is going to
            run ten months a year in Florida and you don&apos;t know a single
            HVAC company. You need a dentist, a good restaurant for date night,
            a vet for your dog.
          </p>
          <p className="mb-7 font-merriweather text-[24px] font-bold italic leading-[1.3] text-grm-black md:text-[30px]">
            You don&apos;t know anyone yet.
          </p>
          <p className="mb-9 font-nunito text-[15px] leading-[1.75] text-grm-black/65">
            That&apos;s the moment The Front Porch exists for. And when your
            agent closes the deal, The Closing Table makes sure the whole
            professional network knows who made it happen.
          </p>
          <div className="mb-7 h-px w-12 bg-grm-teal" />
          <p className="font-comfortaa text-[11px] font-bold uppercase tracking-[0.15em] text-grm-teal">
            GET ROOTED MEDIA &middot; MARION COUNTY, FLORIDA
          </p>
        </div>
      </div>
    </section>
  );
}
