import { Separator } from "@/components/ui/separator";
import {Link} from "react-router-dom";

export function Footer() {

    return (
        <>
            <Separator />
            
            <footer className="bg-white dark:bg-gray-900">
                <div className="container flex flex-col items-center justify-between px-6 py-8 mx-auto lg:flex-row">
                    {/* <a href="#">
                        <img className="w-auto h-7" src="https://merakiui.com/images/full-logo.svg" alt=""/>
                    </a> */}

                    <div className="flex flex-wrap items-center justify-center gap-4 mt-6 lg:gap-6 lg:mt-0">
                        <Link to="https://docs.substrateai.com/" className="text-sm text-gray-600 transition-colors duration-300 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-400">
                            Documentation
                        </Link>

                        <Link to="pricing" className="text-sm text-gray-600 transition-colors duration-300 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-400">
                            Pricing
                        </Link>

                        <Link to="legal/terms-and-conditions" className="text-sm text-gray-600 transition-colors duration-300 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-400">
                            Terms and Conditions
                        </Link>

                        <Link to="legal/privacy-policy" className="text-sm text-gray-600 transition-colors duration-300 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-400">
                            Privacy
                        </Link>

                        <Link to="contact" className="text-sm text-gray-600 transition-colors duration-300 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-400">
                            Help
                        </Link>

                    </div>

                    <p className="mt-6 text-sm text-gray-500 lg:mt-0 dark:text-gray-400">© Copyright 2023 SubstrateAI. </p>
                </div>
            </footer>

        </>
    )


}