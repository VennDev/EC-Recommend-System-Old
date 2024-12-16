import { CategoryMenu, Hero, Incentives, IntroducingSection, Newsletter, ProductsDiscounted, ProductsSection } from "@/components";

export default function Home() {
  return (
    <>
      <Hero />
      <IntroducingSection />
      <CategoryMenu />
      <ProductsDiscounted />
      <ProductsSection />
    </>
  );
}
