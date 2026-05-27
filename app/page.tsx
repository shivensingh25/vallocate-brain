import { Nav } from "@/components/Nav";
import { Hero } from "@/components/Hero";
import { VBrain } from "@/components/VBrain";
import { Agents } from "@/components/Agents";
import { VAllocate } from "@/components/VAllocate";
import { HowItWorks } from "@/components/HowItWorks";
import { Audience } from "@/components/Audience";
import { CTASection } from "@/components/CTASection";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <main>
      <Nav />
      <Hero />
      <VBrain />
      <Agents />
      <VAllocate />
      <HowItWorks />
      <Audience />
      <CTASection />
      <Footer />
    </main>
  );
}
