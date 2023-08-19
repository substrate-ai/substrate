import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table"
import { useState } from "react";
import { GetTokenDTO, useDeleteToken, useGetTokensQuery } from "src/api/token";
import { InputForm } from "src/components/InputForm";
   
   
export default function TokenSection() {

    // const [tokens, setTokens] = useState<GetTokenDTO[]>([]);


    const { 
        data, 
        isLoading, 
        isError 
    } = useGetTokensQuery();

    console.log("data", data)
    console.log("isLoading", isLoading)
    console.log("isError", isError)
    const tokens = data ?? []

    const {mutate} = useDeleteToken()





    return (

        <>

            <InputForm/>

            <div className="h-5"/>
        
            {/* <ScrollArea className="rounded-md border"> */}

                <Table>
                    <TableHeader>
                    <TableRow>
                        <TableHead >Token name</TableHead>
                        <TableHead>Value</TableHead>
                        <TableHead className="text-right"></TableHead>
                    </TableRow>
                    </TableHeader>
                    <TableBody>
                    {tokens.map((tokens) => (
                        <TableRow key={tokens.id}>
                        <TableCell className="font-medium">{tokens.token_name}</TableCell>
                        <TableCell>***********</TableCell>
                        <TableCell className="text-right">
                            <Button variant="outline" onClick={() => mutate(tokens.id)}>Delete me</Button>
                            </TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
            {/* </ScrollArea> */}

      </>
    )
  }

