import { Button } from "@/components/ui/button";
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
import { GetTokenDTO, useGetTokensQuery } from "src/api/token";
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



    return (

        <>

            <InputForm/>

            <div className="h-5"/>
        

            <Table>
                <TableHeader>
                <TableRow>
                    <TableHead className="w-[100px]">Token name</TableHead>
                    <TableHead>Value</TableHead>
                    <TableHead className="text-right"></TableHead>
                </TableRow>
                </TableHeader>
                <TableBody>
                {tokens.map((tokens, i) => (
                    <TableRow key={i}>
                    <TableCell className="font-medium">{tokens.token_name}</TableCell>
                    <TableCell>***********</TableCell>
                    <TableCell className="text-right">
                        <Button onClick={() => console.log("deleted")}>Delete me</Button>
                        </TableCell>
                    </TableRow>
                ))}
                </TableBody>
            </Table>
      </>
    )
  }

