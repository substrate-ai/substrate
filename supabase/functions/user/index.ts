import { Application, Router, Context} from 'oak'
import * as bcrypt from "https://deno.land/x/bcrypt/mod.ts";
import { User, Session, createClient} from "@supabase/supabase-js"
import { getQuery } from 'https://deno.land/x/oak@v11.1.0/helpers.ts';
import { supabaseAnon } from "../_shared/supabaseClients.ts";


const router = new Router()
router
  // Note: path should be prefixed with function name
  .post('/user/sign-in', async (ctx: Context) => {
    const result = ctx.request.body();
    const value = await result.value;
    const email = value.email
    const password = value.password

    const session = await signIn(email, password)

    ctx.response.body = session
    console.log("session", session)
    ctx.response.status = 200
  })
  // get with params for user id
  .get('/user/payment_status/:supabase_id', async (ctx: Context) => {
    // parse query params

    const query = getQuery(ctx, { mergeParams: true })
    const supabaseId = query.supabase_id

    const paymentStatus = await checkPaymentStatus(supabaseId)

    ctx.response.body = { payment_status: paymentStatus }
  })




type paymentStatus = "not set" | "admin" | "active" | "payment_failed" // not sure if up to date

async function checkPaymentStatus(supabaseId: string): Promise<paymentStatus> {
  const { data, error } = await supabaseAnon.from('user_data').select("payment_status").eq('id', supabaseId).single()

  if (error) {
    console.error("error getting payment_status", error)
    throw new Error(error.message)
  }

  if (!data) {
    throw new Error("no data")
  }

  const paymentStatus = data.payment_status

  return paymentStatus

}
  
async function signIn(email: string, password: string): Promise<Session> {
  const { data: dataSignIn, error: errorSignIn } = await supabaseAnon.auth.signInWithPassword({
    email: email,
    password: password
  })

  if (errorSignIn ) {
    throw new Error(errorSignIn.message)
  }

  if (!dataSignIn) {
    throw new Error("no user data")
  }



  return dataSignIn.session

}
  

  

const app = new Application()
app.use(router.routes())
app.use(router.allowedMethods())

await app.listen({ port: 8000 })