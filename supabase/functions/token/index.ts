import { Application, Router } from 'oak'
import * as bcrypt from "https://deno.land/x/bcrypt/mod.ts";


const router = new Router()
router
  // Note: path should be prefixed with function name
  .post('/token/verify-token', (context) => {
    
  })
  .get('/token/tokens', async (context) => {
    
  })
  .post('/token/token', (context) => {
    
  })
  .delete('/token/token', (context) => {

  })

function createToken(tokenName: string) {

    const user = context.state.user;

    const myUUID = crypto.randomUUID();
    // generate random string
    const randomString = crypto.getRandomValues(new Uint8Array(32));
    // convert to base64
    const base64String = btoa(String.fromCharCode(...randomString));
    const password = base64String;

    const token = myUUID + ":" + tokenName

    // hash the password
    const hash =  bcrypt.hashSync(password);



    // store the hash in the database
    SupabaseClient.from('tokens').insert([
        { token: token, hash: hash },
    ]).then(response => {
        console.log(response)
    }
    




    



}
  

const app = new Application()
app.use(router.routes())
app.use(router.allowedMethods())

await app.listen({ port: 8000 })