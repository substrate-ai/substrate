import TorusLogo from "../assets/TorusLogo"

export default function Navbar() {
    return (
        <div className="flex justify-between backdrop-filter backdrop-blur-lg bg-opacity-30 bg-gray-500">
            {/* <div className="flex space-x-4 justify-self-center"> */}
                <div>
                    <a href="" className="flex items-center py-5 px-2">
                        <TorusLogo size={50}></TorusLogo>
                        <span className="px-3 text-lg font-bold">Substrate</span>
                    </a>
                </div>
                <div className="hidden md:flex items-center space-x-1">
                    {/* use logo as a link */}
                    
                    <a href="examples" className="py-5 px-3 hover:text-green-500">EXAMPLES</a>
                    <a href="pricing" className="py-5 px-3  hover:text-green-500">PRICING</a>
                    <a href="docs" className="py-5 px-3  hover:text-green-500">DOCS</a>
                </div>
                <div className="hidden md:flex items-center space-x-1 px-8">
                    <a href="login" className="py-5 px-3  hover:text-green-500">LOGIN</a>
                    <a href="signup" className="py-2 px-3 bg-green-500 hover:bg-green-600 text-white rounded transition duration-300">SIGN UP</a>
                </div>
            {/* </div> */}
        </div>
    )
}