import Footer from "src/components/Footer";
import terminal from "src/assets/images/terminal.png";


function WelcomePage() {
  return (
    <>
      <section className="flex h-screen bg-gradient-to-tr from-gray-700 via-gray-900 to-black">
      
      <div className="container flex flex-col m-auto p-0 px-6 py-10 mx-auto space-y-6 lg:h-[32rem] lg:py-16 lg:flex-row lg:items-center ">
        <div className="py-24 flex items-center min-h-screen justify-center ">
          <div className="mx-auto max-w-[43rem]">
            <div className="text-center">
              <p className="text-lg font-medium leading-8 text-indigo-600/95">The easiest way to run your ML workflow at scale</p>
              <h1 className="mt-3 text-[3.5rem] font-bold leading-[4rem] tracking-tight text-white">Accelerate your ML training &nbsp;by using cloud GPUs</h1>
              <p className="mt-3 text-lg leading-relaxed text-slate-400"> Streamline your machine learning workflows by eliminating the hassle of manual deployment</p>
            </div>

            <div className="mt-6 flex items-center justify-center gap-4">
              <a href="dashboard" className="transform rounded-md bg-indigo-600/95 px-5 py-3 font-medium text-white transition-colors hover:bg-indigo-700">Get started for free</a>
              <a href="https://docs.substrateai.com" className="transform rounded-md border border-slate-200 px-5 py-3 font-medium white-slate-900 transition-colors hover:bg-slate-700"> View Documentation </a>
            </div>
          </div>
        
          
        </div>
        <div className="flex items-center justify-center w-full h-96 lg:w-1/2">
            <img className="object-cover w-full h-full mx-auto rounded-md lg:max-w-2xl"  src={terminal}/>
        </div>
      </div>
      </section>

      <Footer/>
     </>
     
  );
}

export default WelcomePage;
