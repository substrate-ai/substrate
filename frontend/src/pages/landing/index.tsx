import {Footer} from "src/components/Footer";
import { Hero } from "src/pages/landing/components/Hero";
import { ProductOverview } from "src/pages/landing/components/ProductOverview";

export function LandingPage() {
  return (
    <>
      <div className="">
      {/* issue if vh if 70 percent, take too much space on mobile */}
        <div className="min-h-[50vh] bg-gradient-to-tr from-gray-700 via-gray-900 to-black items-center">
          <Hero />
        </div>
        <ProductOverview/>
    </div>
    <Footer />
  </>
  );
}
