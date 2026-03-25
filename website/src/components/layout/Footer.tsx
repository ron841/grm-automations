import Link from "next/link";
import Image from "next/image";

export default function Footer() {
  return (
    <footer className="bg-grm-black">
      {/* Main footer content */}
      <div className="mx-auto max-w-7xl px-6 py-20 lg:px-8">
        <div className="grid grid-cols-1 gap-12 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8">
          {/* Column 1 — Brand */}
          <div className="flex flex-col gap-4">
            <Link href="/">
              <Image
                src="/logos/Logo_Get Rooted Media-REV.svg"
                alt="Get Rooted Media"
                width={180}
                height={60}
                className="h-12 w-auto"
              />
            </Link>
            <p className="font-merriweather text-sm italic leading-relaxed text-white">
              Locally rooted. Professionally grown.
            </p>
            <p className="font-nunito text-[13px] text-white/60">
              Marion County, FL
            </p>
          </div>

          {/* Column 2 — Publications */}
          <div className="flex flex-col gap-4">
            <h3 className="font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
              Publications
            </h3>
            <nav className="flex flex-col gap-3">
              <Link
                href="/the-closing-table"
                className="font-nunito text-sm text-white transition-colors hover:text-grm-teal"
              >
                The Closing Table
              </Link>
              <Link
                href="/the-front-porch"
                className="font-nunito text-sm text-white transition-colors hover:text-grm-teal"
              >
                The Front Porch
              </Link>
            </nav>
          </div>

          {/* Column 3 — Connect */}
          <div className="flex flex-col gap-4">
            <h3 className="font-comfortaa text-[11px] font-bold uppercase tracking-widest text-grm-teal">
              Connect
            </h3>
            <nav className="flex flex-col gap-3">
              <a
                href="https://instagram.com/getrootedmedia"
                target="_blank"
                rel="noopener noreferrer"
                className="font-nunito text-sm text-white transition-colors hover:text-grm-teal"
              >
                @GetRootedMedia
              </a>
              <a
                href="https://instagram.com/closingtable.mag"
                target="_blank"
                rel="noopener noreferrer"
                className="font-nunito text-sm text-white transition-colors hover:text-grm-teal"
              >
                @ClosingTable.mag
              </a>
              <a
                href="https://instagram.com/frontporch.mag"
                target="_blank"
                rel="noopener noreferrer"
                className="font-nunito text-sm text-white transition-colors hover:text-grm-teal"
              >
                @FrontPorch.mag
              </a>
              <a
                href="mailto:ron@getrootedmedia.com"
                className="font-nunito text-sm text-white transition-colors hover:text-grm-teal"
              >
                ron@getrootedmedia.com
              </a>
            </nav>
          </div>

          {/* Column 4 — CTA */}
          <div className="flex flex-col gap-4">
            <Link
              href="/contact"
              className="block w-full rounded-md bg-grm-teal py-3 text-center font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
            >
              Let&apos;s Talk
            </Link>
            <Link
              href="#media-kit"
              className="font-nunito text-sm text-white no-underline transition-colors hover:underline hover:text-grm-teal"
            >
              or download our media kit
            </Link>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-white/10">
        <div className="mx-auto max-w-7xl px-6 py-6 lg:px-8">
          <p className="text-center font-nunito text-xs text-white/50">
            &copy; 2026 Get Rooted Media LLC &middot; Marion County, Florida
          </p>
        </div>
      </div>
    </footer>
  );
}
