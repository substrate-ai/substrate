import { supabaseAdmin } from "./supabaseClients.ts";
import * as bcrypt from "https://deno.land/x/bcrypt@v0.4.1/mod.ts";


export async function getUserIdFromToken(token: string): Promise<string> {

    console.log("token", token)

    const [uuid, password] = token.split(":")

    console.log("uuid", uuid)
    const {data, error} = await supabaseAdmin.from('token').select("encrypted_token, supabase_id").eq('id', uuid).single()

    if (error) {
        console.error("error getting token", error)
        throw new Error(error.message)
    }

    if (!data) {
        console.error("no data")
        throw new Error("no data")
    }

    const encryptedToken = data.encrypted_token

    const match = bcrypt.compareSync(password, encryptedToken)

    if (!match) {
        console.error("token provided does not match saved token in db")
        throw new Error("token provided does not match saved token in db")
    }

    return data.supabase_id

}