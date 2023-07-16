import { Canvas, MeshProps, useFrame } from "@react-three/fiber"
import { useRef } from "react"
import { Mesh } from "three"

export default function Torus3D() {
    const ref = useRef<Mesh>(null)
    useFrame(() => (ref.current!.rotation.x = ref.current!.rotation.y += 0.01))

    return (
    
        <mesh
            scale={[2, 2, 2]}
            ref={ref}
            onClick={e => console.log('click')}
            onPointerOver={e => console.log('hover')}
            onPointerOut={e => console.log('unhover')}>
            <torusGeometry args={[1, 0.5, 16, 20]} />
            <meshStandardMaterial color="0xffff00" wireframe />
        </mesh>
    )
  }