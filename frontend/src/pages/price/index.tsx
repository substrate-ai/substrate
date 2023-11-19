import { PricingTable } from "src/components/PricingTable"
import { Subscription } from "src/components/Subscription"


export default function Pricing() {

  return (
    <div className="flex flex-col space-y-7">
    <p className="text-center text-lg font-bold">
      Our plans
    </p>
    <Subscription></Subscription>
    <p className="text-center text-lg font-bold">
      Compute cost
    </p>
    <div className="">
      <div className="m-auto w-1/2 ">
          <PricingTable/>
      </div>

      
    </div>
    
    </div>
  )
}

