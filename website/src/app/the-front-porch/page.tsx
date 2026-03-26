import type { Metadata } from "next";
import FPHero from "@/components/sections/fp/FPHero";
import FP60DayWindow from "@/components/sections/fp/FP60DayWindow";
import FPComparison from "@/components/sections/fp/FPComparison";
import FPCategoryGrid from "@/components/sections/fp/FPCategoryGrid";
import FPAdvertising from "@/components/sections/fp/FPAdvertising";
import FPReaderSignup from "@/components/sections/fp/FPReaderSignup";
import FPFAQ from "@/components/sections/fp/FPFAQ";
import FPFoundingPartner from "@/components/sections/fp/FPFoundingPartner";

export const metadata: Metadata = {
  title:
    "The Front Porch | Bi-Monthly Resource Guide for Marion County New Homeowners",
  description:
    "The bi-monthly resource guide mailed to every new homeowner in Marion County within their first 60 days. Issue 1 July 2026.",
};

export default function FrontPorchPage() {
  return (
    <main>
      <FPHero />
      <FP60DayWindow />
      <FPComparison />
      <FPCategoryGrid />
      <FPAdvertising />
      <FPReaderSignup />
      <FPFAQ />
      <FPFoundingPartner />
    </main>
  );
}
