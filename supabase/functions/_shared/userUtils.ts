import {  Context} from 'oak'
import { User} from "@supabase/supabase-js"
import { supabaseAnon } from "./supabaseClients.ts";

export function getUserFromServe(req: Request): Promise<User> {
    const token = req.headers.get('Authorization')!

    return getUserFromAuthorizationHeader(token)
}

export function getUserFromContext(context: Context): Promise<User> {
    const header = context.request.headers.get('Authorization')!
    const token = header.split(" ")[1]

    return getUserFromAuthorizationHeader(token)
}

async function getUserFromAuthorizationHeader(authorizationToken: string): Promise<User> {
    const {data, error} = (await supabaseAnon.auth.getUser(authorizationToken))

    if (error) {
      console.error("error getting user", error)
      throw new Error(error.message)
    }
  
    return data.user
}

export async function getUserFromId(id: string): Promise<any> {
    const {data, error} = (await supabaseAnon.from('user_data').select().eq('id', id).single())

    if (error) {
      console.error("error getting user", error)
      throw new Error(error.message)
    }
  
    return data
}

