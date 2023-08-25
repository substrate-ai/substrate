import { supabaseAdmin } from "./supabaseClients.ts";
import * as bcrypt from "https://deno.land/x/bcrypt/mod.ts";


export default async function getUserIdFromToken(token: string): Promise<string> {

    console.log("token", token)

    const [uuid, password] = token.split(":")

    console.log("uuid", uuid)
    const {data, error} = await supabaseAdmin.from('token').select("encrypted_token, supabase_id").eq('id', uuid).single()

    if (error) {
        console.error("error getting token", error)
        throw new Error(error.message)
    }

    if (!data) {
        throw new Error("no data")
    }

    const encryptedToken = data.encrypted_token

    const match = bcrypt.compareSync(password, encryptedToken)

    if (!match) {
        throw new Error("token does not match")
    }

    return data.supabase_id

}