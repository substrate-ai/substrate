import { Button } from '@/components/ui/button';
import logo from 'src/assets/images/logo.png';
import { Mail } from "lucide-react"



export default function HelpPage() {

    const email = 'support@substrateai.com'

    return (
        <div className="flex h-screen">
        <div className="m-auto">
        
            <div className="container m-auto px-6 text-gray-600 md:px-12 xl:px-6">
                <div className="space-y-6 md:space-y-0 md:flex md:gap-6 lg:items-center lg:gap-12">
                    <div className="md:5/12 lg:w-5/12">
                    <img src={logo} alt="logo" loading="lazy" width="" height=""/>
                    </div>
                    <div className="md:7/12 lg:w-6/12">
                    <h2 className="text-2xl text-gray-100 font-bold md:text-4xl">SubstrateAI, accelerating your ml journey 🔥</h2>
                    <p className="mt-6 text-gray-400">Hey there! 🚀 We're SubstrateAI, a fresh and enthusiastic player in the tech world. Why did we kick off this adventure? 🌟 Because we know the struggle – battling for GPU access and wrestling with deployment complexities. 😫</p>
                    <p className="mt-4 text-gray-400">We've been there, and we get it. Our passion? Making GPU-powered code magic accessible to everyone. ✨ No more jargon, no more hoops. With our streamlined CLI, you'll run your ML code on the cloud with a single command. Yep, you read that right – one command! 💥</p>
                    <div className='py-3'></div>
                    <Button className='flex flex-row ' onClick={
                        (e) => {
                            window.location.href = `mailto:${email}`;
                            e.preventDefault();
                        }
                    }>
                        
                            <a href={`mailto:${email}`} className='flex text-white'>
                                <Mail className="mr-2 h-4 w-4 flex select-text" />
                                support@substrateai.com
                                
                            </a>
                        
                    </Button>
                    {/* <Link
                        to='#'
                        onClick={(e) => {
                            window.location.href = `mailto:${email}`;
                            e.preventDefault();
                        }}
                    >
                         <Mail className="mr-2 h-4 w-4" /> Contact us at2 support@substrateai.com
                       
                    </Link> */}
                    


                    </div>
                </div>
            </div>
        </div>
        </div>

    )
}