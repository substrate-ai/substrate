import torus from '/torus.svg'

type TorusLogoProps = { 
    dark?: boolean,
    size?: number
};

export default function TorusLogo({dark, size}: TorusLogoProps) {

    let torus_style = {
        width: size || 100,
        height: size || 100,
        filter: ""
    }

    if (!dark) {
        torus_style = {
            width: torus_style.width,
            height: torus_style.height,
            filter: "invert(100%) sepia(100%) saturate(0%) hue-rotate(288deg) brightness(102%) contrast(102%)",
        }
    } 
    // use a filter to change svg color

    return (
        <div>
            <img style={torus_style} src={torus} className="App-logo" alt="logo" />
        </div>
    )

}