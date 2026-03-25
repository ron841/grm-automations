import HomeHero from "@/components/sections/HomeHero";
import HomeStory from "@/components/sections/HomeStory";
import HomePublications from "@/components/sections/HomePublications";
import HomeStats from "@/components/sections/HomeStats";
import HomeHowItWorks from "@/components/sections/HomeHowItWorks";
import HomeFinalCTA from "@/components/sections/HomeFinalCTA";

export default function Home() {
  return (
    <main>
      <HomeHero />
      <HomeStory />
      <HomePublications />
      <HomeStats />
      <HomeHowItWorks />
      <HomeFinalCTA />
    </main>
  );
}
