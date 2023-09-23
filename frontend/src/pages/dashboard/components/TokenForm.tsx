import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
 
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { createToken } from "src/api/token"
import { useState } from "react"
import {ConfirmDialog} from "./ConfirmDialog"
import {ReadOnlyInput} from "./ReadOnlyInput"
import { useQueryClient } from "@tanstack/react-query"
import { ReloadIcon } from "@radix-ui/react-icons"

const FormSchema = z.object({
  tokenName: z.string().nonempty({ message: "Token name is required" })
})
 
export function TokenForm() {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
  })

  const [open, setOpen] = useState(false)
  const [newToken, setNewToken] = useState("")
  const queryClient = useQueryClient()
  const [loading, setLoading] = useState(false)
  
  async function onSubmit(data: z.infer<typeof FormSchema>) {
    setLoading(true)
    const response = await createToken(data.tokenName)
    setNewToken(response.accessToken)
    setOpen(true)
    setLoading(false)
    queryClient.invalidateQueries(["tokens"])
    

  }




  
 
  return (
    <>
      <ConfirmDialog open={open} setOpen={setOpen}>
        <ReadOnlyInput value={newToken}/> 
      </ConfirmDialog>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="w-2/3 flex flex-row space-x-4">
          <FormField
            control={form.control}
            name="tokenName"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <Input placeholder="cli" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          {loading ? 
          <Button disabled>
            <ReloadIcon className="mr-2 h-4 w-4 animate-spin" />
            Please wait
          </Button>
          : 
          <Button type="submit">Add Token</Button>
          }
          
        </form>
      </Form>
    </>
  )
}