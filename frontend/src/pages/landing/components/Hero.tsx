import terminal from "src/assets/images/terminal.png";
import { Link } from "react-router-dom";

export function Hero() {
    return (
        <section>
        <div className="container flex flex-col m-auto p-0 px-6 py-10 space-y-6 lg:h-[32rem] lg:py-16 lg:flex-row lg:items-center">
          <div className="flex-1 lg:py-24 flex flex-col items-center justify-center text-center lg:px-6">
            <p className="text-lg font-medium leading-8 text-indigo-600/95">
              Get your code up and running in the cloud in less than 5 minutes
            </p>
            <h1 className="mt-3 text-[3.5rem] font-bold leading-[4rem] tracking-tight text-white">
              Don't Waste Time on AI Infrastructure Anymore.
                
            </h1>
            <p className="mt-3 text-lg leading-relaxed text-slate-400">
              Effortlessly Develop on Cloud GPUs, Just Like Your Laptop
            </p>

            <div className="mt-6 flex items-center justify-center gap-4">
              <Link to="sign-up" className="transform rounded-md bg-indigo-600/95 px-5 py-3 font-medium text-white transition-colors hover:bg-indigo-700">
                Sign Up (for Beta)
              </Link>
              <Link to="https://docs.substrateai.com" className="transform rounded-md border border-slate-200 px-5 py-3 font-medium white-slate-900 transition-colors hover:bg-slate-700">
                View Documentation
              </Link>
            </div>
          </div>
  
          <div className="flex-1 flex items-center justify-center w-full h-64 lg:w-auto">
            <img className="object-contain w-full h-full rounded-md lg:max-w-2xl" src={terminal} alt="Terminal" />
          </div>
        </div>
      </section>
    )
}