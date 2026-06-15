import type { Metadata } from "next";
import CTHero from "@/components/sections/ct/CTHero";
import CTAgentCallout from "@/components/sections/ct/CTAgentCallout";
import CTWhyThisWorks from "@/components/sections/ct/CTWhyThisWorks";
import CTWhatsInside from "@/components/sections/ct/CTWhatsInside";
import CTIssuePreview from "@/components/sections/ct/CTIssuePreview";
import CTAdvertising from "@/components/sections/ct/CTAdvertising";
import CTFAQ from "@/components/sections/ct/CTFAQ";
import CTFoundingPartner from "@/components/sections/ct/CTFoundingPartner";

export const metadata: Metadata = {
  title: "The Closing Table | Monthly Magazine for Marion County Real Estate",
  description:
    "The monthly magazine for top-producing real estate agents in Marion and Sumter Counties. A new Get Rooted Media title launching Spring 2027.",
  openGraph: {
    title: "The Closing Table | Monthly Magazine for Marion County Real Estate",
    description:
      "The monthly magazine for top-producing real estate agents in Marion and Sumter Counties. A new Get Rooted Media title launching Spring 2027.",
    type: "website",
    url: "https://getrootedmedia.com/the-closing-table",
    siteName: "Get Rooted Media",
    images: [{ url: "/images/ct-hero.webp" }],
  },
};

export default function ClosingTablePage() {
  return (
    <main>
      <CTHero />
      <CTAgentCallout />
      <CTWhyThisWorks />
      <CTWhatsInside />
      <CTIssuePreview />
      <CTAdvertising />
      <CTFAQ />
      <CTFoundingPartner />
    </main>
  );
}
