import { zodResolver } from "@hookform/resolvers/zod"
import { set, useForm } from "react-hook-form"
import * as z from "zod"
 
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { toast } from "@/components/ui/use-toast"
import { createToken, usePostTokenQuery } from "src/api/token"
import { useState } from "react"
import axios from "axios"
import ConfirmDialog from "./ConfirmDialog"
import ReadOnlyInput from "./ReadOnlyInput"
 
const FormSchema = z.object({
  tokenName: z.string().nonempty({ message: "Token name is required" })
})


 
export function InputForm() {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
  })

  const [open, setOpen] = useState(false)
  const [newToken, setNewToken] = useState("")

  
//   mutate({tokenName: newToken})
  // TODO add loading state after submit + ideally handle everything with reatc query
  async function onSubmit(data: z.infer<typeof FormSchema>) {
    console.log("token name", data.tokenName)
    const response = await createToken(data.tokenName)
    console.log("response", response)
    setOpen(true)
    setNewToken(response.accessToken)
    console.log("newToken", newToken)
    

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
          <Button type="submit">Add Token</Button>
        </form>
      </Form>
    </>
  )
}