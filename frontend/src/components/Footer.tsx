import { Separator } from "@/components/ui/separator";

export default function Footer() {

    return (
        <>
            <Separator />
            
            <footer className="bg-white dark:bg-gray-900">
                <div className="container flex flex-col items-center justify-between px-6 py-8 mx-auto lg:flex-row">
                    {/* <a href="#">
                        <img className="w-auto h-7" src="https://merakiui.com/images/full-logo.svg" alt=""/>
                    </a> */}

                    <div className="flex flex-wrap items-center justify-center gap-4 mt-6 lg:gap-6 lg:mt-0">
                        <a href="https://docs.substrateai.com/" className="text-sm text-gray-600 transition-colors duration-300 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-400">
                            Documentation
                        </a>

                        <a href="pricing" className="text-sm text-gray-600 transition-colors duration-300 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-400">
                            Pricing
                        </a>

                        <a href="legal/terms-and-conditions" className="text-sm text-gray-600 transition-colors duration-300 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-400">
                            Terms and Conditions
                        </a>

                        <a href="legal/privacy-policy" className="text-sm text-gray-600 transition-colors duration-300 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-400">
                            Privacy
                        </a>

                        <a href="contact" className="text-sm text-gray-600 transition-colors duration-300 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-400">
                            Help
                        </a>

                    </div>

                    <p className="mt-6 text-sm text-gray-500 lg:mt-0 dark:text-gray-400">© Copyright 2023 SubstrateAI. </p>
                </div>
            </footer>

        </>
    )


}