import { Button } from '@/components/ui/button';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import python from 'react-syntax-highlighter/dist/esm/languages/hljs/python';
import bash from 'react-syntax-highlighter/dist/esm/languages/hljs/bash';
import yaml from 'react-syntax-highlighter/dist/esm/languages/hljs/yaml';
import stackoverflowDark from 'react-syntax-highlighter/dist/esm/styles/hljs/stackoverflow-dark';
import { useNavigate } from 'react-router-dom';
import ad from "src/assets/images/ad.png";
import textToSpeech from "src/assets/images/text-to-speech.png";
import textToImage from "src/assets/images/text-to-image.png";
import languageModels from "src/assets/images/language-model.png";
import caption from "src/assets/images/caption.png";
import huggingaceLogo from "src/assets/svg/huggingface-logo.svg";
import pytorchLogo from "src/assets/svg/pytorch-logo.svg";
import { PricingTable } from "src/components/PricingTable"
import { TimeUnit } from "src/types/enums";
import { CardProject } from "./CardProject";



SyntaxHighlighter.registerLanguage('python', python);
SyntaxHighlighter.registerLanguage('bash', bash);
SyntaxHighlighter.registerLanguage('yaml', yaml);

const substrateInstall = `$ pip install substrate-ai`


const substrateYaml = 
`# substrate.yaml
project_name: my-first-project
hardware:
      type: t4
main_file_location: ./your_code.py
`

const requirementsTxt = 
`# requirement.txt
- "torch==2.0.0"
`

const codebase = 
`# your_code.py
from diffusers import DiffusionPipeline
generator = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2")
image = generator("Image for a robot ad").images[0]
image.save("robot_ad.jpg")
`

const substrateRun = `$ substrate-ai run`

const useCases = [
  {"title": "Text-to-Image", "src": textToImage, "description": "Generate images from text with model such as StableDiffusion"},
  {"title": "Text-to-Speech", "src": textToSpeech, "description": "Generate speech from text with model such as CoquiTTS"},
  {"title": "Language Models", "src": languageModels, "description": "Generate text from text with model such as LLAMA"},
  {"title": "Speech Recognition", "src": caption, "description": "Generate text from speech with model such as Whisper"},
]


export function ProductOverview() {
  const navigate = useNavigate()

  return (
    <div className="my-10 space-y-6 mx-10 lg:mx-60">
    <div className="space-y-6">
      <h1 className="text-2xl">Run your code on the cloud</h1>
      <h2>Step 1: Install</h2>
      <SyntaxHighlighter language="bash" style={stackoverflowDark}>
        {substrateInstall}
      </SyntaxHighlighter>
      <h2>Step 2: Config</h2>
      <div className='flex flex-col lg:flex-row space-y-2 lg:space-x-10'>
        <div className="space-y-2">
          <p>Define the hardware you want to use</p>
          <SyntaxHighlighter language="yaml" style={stackoverflowDark} >
            {substrateYaml}
          </SyntaxHighlighter>
        </div>
        <div className="space-y-2">
          <p>We use your requirement.txt file so you can get started quickly, no need to rewrite your code</p>
          <SyntaxHighlighter language="python" style={stackoverflowDark} >
            {requirementsTxt}
          </SyntaxHighlighter>
        </div>
      </div>
      <h2>Step 3: Run</h2>
      <div className="space-y-2">
      <p>Your codebase</p>
      <SyntaxHighlighter language="python" style={stackoverflowDark} wrapLines={true}>
        {codebase}
      </SyntaxHighlighter>
      </div>
      <div className='flex flex-col lg:flex-row lg:space-x-20'>
        <div className="space-y-2">
          <p>Run your ML workflow on the cloud</p>
          <SyntaxHighlighter language="bash" style={stackoverflowDark} className="prose">
            {substrateRun}
          </SyntaxHighlighter>
        </div>
        <div className="space-y-2">
          <p>Enjoy your hard work</p>
          <img src={ad} alt="output of code" className="w-[250px] lg:w-1/3"></img>
        </div>
      </div>
    </div>

    <div className="space-y-4">
      <h1 className="text-2xl">Support your use cases</h1>
      {/* grid of 4x4 div use tailwind */}
      <div>
       
      <div className="grid grid-cols-2 gap-4">
      {/* Four columns on larger screens */}
        {useCases.map((useCase, index) => (
            <CardProject project={useCase} key={index} className="w-[150px] lg:w-[250px]"/>
            // <div className="flex flex-row space-x-5 w-1/3">
            //   <AspectRatio ratio={1} key={index}>
            //     <img
            //       src={useCase.src}
            //       alt={useCase.title}
            //       className="rounded-md object-cover"
            //     />
            //   </AspectRatio>
            //   <p>{useCase.title}</p>
            // </div>
        ))}
      </div>
      </div>
      {/* <p>And many more</p> */}
    </div>

    <div className="space-y-4">
      <p>Optimized for all your favourite tools</p>
      <div className='flex flex-col lg:flex-row lg:space-x-10 space-y-4 lg:space-y-0'>
          <img src={pytorchLogo} alt="pytorch-logo" className="w-28"/>
          <img src={huggingaceLogo} alt="huggingface-logo" className="w-36"/>
      </div>
    </div>


    <div className="space-y-5">
      <p className="text-2xl">Pay by the Second, Nothing More</p>
      <PricingTable view={TimeUnit.second} hideFooter></PricingTable>
    </div>
    <div className='flex lg:flex-row space-x-4 justify-center items-center'>
      {/* <p className='w-1/2 '> Our streamlined command-line interface and seamless cloud integration make running your code faster and simpler than ever. Join our beta program for an exclusive experience.</p> */}
      <Button size="lg" variant="outline" onClick={() => navigate("/sign-up")} className="bg-indigo-600/95">Sign up (for beta)</Button>
    </div>
    </div>
      )
    }
