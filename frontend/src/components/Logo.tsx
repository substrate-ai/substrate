import logo from 'src/assets/images/logo.png';

type LogoProps = {
    size?: number
}

export default function Logo ({ size = 5 }: LogoProps) {
  return (
    <div className="logo">
      <img src={logo} alt="logo" className={`h-${size}`}/>
    </div>
  )
}