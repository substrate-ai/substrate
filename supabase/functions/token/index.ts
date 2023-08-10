import { Application, Router } from 'oak'
import * as bcrypt from "https://deno.land/x/bcrypt/mod.ts";
import { getUserFromContext } from '../_shared/getUserFromRequest.ts';
import { Context } from 'oak';
import { supabaseAdmin } from "../_shared/supabaseClients.ts";


const router = new Router()
router
  // Note: path should be prefixed with function name
  .post('/token/verify-token', async (ctx: Context) => {
    const result = ctx.request.body();
    const value = await result.value;
    const token = value.accessToken
    const match = await verifyToken(token)
    ctx.response.body = { verified: match }
  })
  .get('/token/tokens', (ctx: Context) => {
    // This is done client-side
    ctx.response.status = 404
  })
  .post('/token/token', async (ctx: Context) => {
    const user = await getUserFromContext(ctx) 
    const supabaseId = user.id
    const result = ctx.request.body();
    const value = await result.value;
    const tokenName = value.tokenName

    const token = await createToken(tokenName, supabaseId)

    ctx.response.body = token
  })
  .delete('/token/token', (ctx: Context) => {
    // This is done client-side
    ctx.response.status = 404
  })

type Token = {
    accessToken: string
}

async function verifyToken(token: string): Promise<boolean> {

    console.log("token", token)

    const [uuid, password] = token.split(":")

    console.log("uuid", uuid)
    const {data, error} = await supabaseAdmin.from('token').select("encrypted_token").eq('id', uuid).single()

    if (error) {
        console.error("error getting token", error)
        throw new Error(error.message)
    }

    if (!data) {
        throw new Error("no data")
    }

    const encryptedToken = data.encrypted_token

    const match = bcrypt.compareSync(password, encryptedToken)

    return match

}

async function createToken(tokenName: string, supabaseId: string): Promise<Token> {


    // generate random string
    const randomString = crypto.getRandomValues(new Uint8Array(32));
    // convert to base64
    const base64String = btoa(String.fromCharCode(...randomString)).replace(':', '!');
    const password = base64String;

    const uuid = crypto.randomUUID()


    // hash the password
    const salt = bcrypt.genSaltSync(8);
    const hash =  bcrypt.hashSync(password, salt);


    // store the hash in the database
    const {data, error} = await supabaseAdmin.from('token').insert(
        { 
            supabase_id: supabaseId, 
            encrypted_token: hash, 
            token_name: tokenName,
            id: uuid
        }
    ).select("id").single()

    if (error) {
        console.log("error inserting token", error)
        console.log("error message inserting  token", error.message)
        throw new Error(error.message)
    }

    console.log("data", data)

    // const uuid = data.uuid

    const accesToken = uuid + ":" + password

    return { accessToken: accesToken }
    




    



}
  

const app = new Application()
app.use(router.routes())
app.use(router.allowedMethods())

await app.listen({ port: 8000 })