import {CopyToClipboard} from 'react-copy-to-clipboard';
import { IconCopy } from '@tabler/icons-react';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { useState } from 'react';

type ReadOnlyInputProps = {
    value: string
}

export function ReadOnlyInput({value}: ReadOnlyInputProps) {

    const [copied, setCopied] = useState(false)

    function handleCopy() {
        setCopied(true)
        setTimeout(() => {
            setCopied(false)
        }, 1000)
    }

  return (
    <div className="relative mb-3 flex flex-row space-x-2" data-te-input-wrapper-init>
        <input
            type="text"
            className="overflow-x-scroll peer block min-h-[auto] w-full rounded border-0 bg-neutral-100 px-3 py-[0.32rem] leading-[1.6] outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 peer-focus:text-primary data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none dark:bg-neutral-700 dark:text-neutral-200 dark:placeholder:text-neutral-200 dark:peer-focus:text-primary [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0"
            id="exampleFormControlInput50"
            value={value}
            aria-label="readonly input example"
            readOnly />
        {/* <label
            htmlFor="exampleFormControlInput50"
            className="pointer-events-none absolute left-3 top-0 mb-0 max-w-[90%] origin-[0_0] truncate pt-[0.37rem] leading-[1.6] text-neutral-500 transition-all duration-200 ease-out peer-focus:-translate-y-[0.9rem] peer-focus:scale-[0.8] peer-focus:text-primary peer-data-[te-input-state-active]:-translate-y-[0.9rem] peer-data-[te-input-state-active]:scale-[0.8] motion-reduce:transition-none dark:text-neutral-200 dark:peer-focus:text-primary"
            >Readonly input
        </label> */}
        <TooltipProvider>
            <Tooltip open={copied}>
                <TooltipTrigger>
                    <CopyToClipboard text={value} onCopy={handleCopy}>
                        <IconCopy/>
                    </CopyToClipboard>
                </TooltipTrigger>
                <TooltipContent>
                <p>Copied</p>
                </TooltipContent>
            </Tooltip>
            </TooltipProvider>
        
    </div>
  )
}