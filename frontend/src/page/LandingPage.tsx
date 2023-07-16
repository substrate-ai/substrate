import { Canvas } from '@react-three/fiber'
import TorusLogo from '../assets/TorusLogo'
import Hero from '../component/Hero'
import Navbar from '../component/Navbar'
import Box from '../component/Torus3D'

export default function LandingPage() {

    return (
       
          <div>
            <Navbar></Navbar>
            <p className="font-bold">test</p>
            {/* <TorusLogo dark></TorusLogo> */}
            <Hero></Hero>
          </div>
       
    )


}