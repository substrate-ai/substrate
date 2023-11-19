export  function Subscription() {
  return (
    <div className="flex flex-col items-center justify-center  text-white">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl p-4">
        <div className="flex flex-col bg-gray-800 shadow-lg rounded-lg overflow-hidden">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-200">Free</h3>
            <p className="mt-1 text-4xl font-semibold text-gray-200">$0 <span className="text-sm text-gray-400"> + Compute</span></p>
            <p className="mt-2 text-base font-medium text-gray-500">Per Month</p>
            <ul className="mt-4 space-y-4">
              <li className="flex items-start">
                <div className="flex-shrink-0">
                  <svg
                    className=" h-6 w-6 text-green-500"
                    fill="none"
                    height="24"
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    width="24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </div>
                <p className="ml-3 text-sm leading-5 text-gray-400">10 hours of platform usage</p>
              </li>
            </ul>
          </div>
          {/* <div className="px-4 py-4 sm:px-6">
            <Button variant="default">Choose Free</Button>
          </div> */}
        </div>
        <div className="flex flex-col bg-gray-800 shadow-lg rounded-lg overflow-hidden">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-200">Pro</h3>
            <p className="mt-1 text-4xl font-semibold text-gray-200">$20 <span className="text-sm text-gray-400"> + Compute</span></p>
            <p className="mt-2 text-base font-medium text-gray-500">Per Month</p>
            <ul className="mt-4 space-y-4">
              <li className="flex items-start">
                <div className="flex-shrink-0">
                  <svg
                    className=" h-6 w-6 text-green-500"
                    fill="none"
                    height="24"
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    width="24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </div>
                <p className="ml-3 text-sm leading-5 text-gray-400">Unlimited platform usage</p>
              </li>
            </ul>
          </div>
          {/* <div className="px-4 py-4 sm:px-6">
            <Button variant="default">Choose Pro</Button>
          </div> */}
        </div>
        <div className="flex flex-col bg-gray-800 shadow-lg rounded-lg overflow-hidden">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-200">Enterprise</h3>
            <p className="mt-2 text-lg leading-6 font-medium text-gray-500">Coming Soon</p>
          </div>
          <div className="px-4 py-4 sm:px-6">
            {/* <Button disabled variant="default">
              Coming Soon
            </Button> */}
          </div>
        </div>
      </div>
    </div>
  )
}