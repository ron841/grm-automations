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
    "Monthly print magazine for the top 500 agents and service companies in Marion and Sumter Counties. Issue 1 June 2026.",
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
