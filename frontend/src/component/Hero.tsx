import { Canvas } from "@react-three/fiber";
import Torus3D from "./Torus3D";


export default function Hero() {

    return (
        <div>
            <Canvas>
                <ambientLight />
                <pointLight position={[10, 10, 10]} />
                <Torus3D></Torus3D>
            </Canvas>
        </div>
    )


}