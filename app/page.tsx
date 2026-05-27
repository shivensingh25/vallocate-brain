import { Nav } from "@/components/Nav";
import { Hero } from "@/components/Hero";
import { VBrain } from "@/components/VBrain";
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
      <VAllocate />
      <HowItWorks />
      <Audience />
      <CTASection />
      <Footer />
    </main>
  );
}
