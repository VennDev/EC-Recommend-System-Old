import { CategoryMenu, Hero, Incentives, IntroducingSection, Newsletter, ProductsDiscounted, ProductsRecommend, ProductsSection } from "@/components";

export default function Home() {
  return (
    <>
      <Hero />
      <IntroducingSection />
      <CategoryMenu />
      {/* <ProductsDiscounted /> */}
      <ProductsRecommend />
      <ProductsSection />
    </>
  );
}
