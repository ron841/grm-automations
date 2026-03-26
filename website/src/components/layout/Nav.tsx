"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";

const NAV_LINKS = [
  { href: "/the-closing-table", label: "The Closing Table" },
  { href: "/the-front-porch", label: "The Front Porch" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
];

const CAL_URL = "https://cal.com/ron-kolb-cdlgsw/30min";

export default function Nav() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const pathname = usePathname();
  const isContactPage = pathname === "/contact";
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setMobileOpen(false);
  }, [pathname]);

  // Lock body scroll when mobile menu is open
  useEffect(() => {
    document.body.style.overflow = mobileOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileOpen]);

  return (
    <>
      <nav
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ease-in-out ${
          scrolled
            ? "bg-grm-black/95 backdrop-blur-sm shadow-sm"
            : "bg-transparent"
        }`}
      >
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-8">
          {/* Logo — always show reversed (white) version */}
          <Link href="/" className="relative shrink-0">
            <Image
              src="/logos/Logo_Get Rooted Media-REV.svg"
              alt="Get Rooted Media"
              width={180}
              height={60}
              priority
              className="h-10 w-auto"
            />
          </Link>

          {/* Desktop nav links — always white */}
          <div className="hidden items-center gap-8 lg:flex">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="font-nunito text-[15px] text-white transition-opacity duration-300 hover:opacity-80"
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Desktop CTA button — cal.com, new tab */}
          <a
            href={CAL_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="hidden rounded-md bg-grm-teal px-5 py-2.5 font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90 lg:block"
          >
            Let&apos;s Talk
          </a>

          {/* Mobile hamburger — always white */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="relative z-50 flex h-10 w-10 flex-col items-center justify-center gap-1.5 lg:hidden"
            aria-label={mobileOpen ? "Close menu" : "Open menu"}
          >
            <span
              className={`block h-0.5 w-6 transition-all duration-300 ${
                mobileOpen
                  ? "translate-y-2 rotate-45 bg-grm-black"
                  : "bg-white"
              }`}
            />
            <span
              className={`block h-0.5 w-6 transition-all duration-300 ${
                mobileOpen ? "opacity-0" : "bg-white"
              }`}
            />
            <span
              className={`block h-0.5 w-6 transition-all duration-300 ${
                mobileOpen
                  ? "-translate-y-2 -rotate-45 bg-grm-black"
                  : "bg-white"
              }`}
            />
          </button>
        </div>
      </nav>

      {/* Mobile menu overlay */}
      <div
        className={`fixed inset-0 z-40 bg-white transition-transform duration-300 lg:hidden ${
          mobileOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex h-full flex-col items-center justify-center gap-8 px-6">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              className="font-nunito text-xl text-grm-black transition-colors hover:text-grm-teal"
            >
              {link.label}
            </Link>
          ))}
          <a
            href={CAL_URL}
            target="_blank"
            rel="noopener noreferrer"
            onClick={() => setMobileOpen(false)}
            className="mt-4 rounded-md bg-grm-teal px-8 py-3 font-nunito text-base font-bold text-white transition-opacity hover:opacity-90"
          >
            Let&apos;s Talk
          </a>
        </div>
      </div>

      {/* Mobile fixed bottom CTA — hidden on /contact and when menu is open */}
      {!isContactPage && (
        <div
          className={`fixed bottom-0 left-0 right-0 z-40 border-t border-white/10 bg-grm-black p-4 lg:hidden ${
            mobileOpen ? "hidden" : ""
          }`}
        >
          <a
            href={CAL_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="block w-full rounded-md bg-grm-teal py-3 text-center font-nunito text-sm font-bold text-white transition-opacity hover:opacity-90"
          >
            Let&apos;s Talk
          </a>
        </div>
      )}
    </>
  );
}
