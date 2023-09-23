import { Application, Context, Router } from 'oak'
import { supabaseAdmin } from '../_shared/supabaseClients.ts'
import { LAGO_URL } from '../_shared/lagoUrl.ts';
import { oakCors } from "https://deno.land/x/cors@v1.2.2/mod.ts";
import {getUserIdFromToken} from "../_shared/tokenUtils.ts";


const router = new Router()
router
  // Note: path should be prefixed with function name
.post('/payment/job-done', async (ctx) => {
    await jobDoneHandler(ctx)
})
.get('/payment/user-status', async (ctx) => {
  let id = ""

  if (ctx.request.url.searchParams.has('token')) {
    const token = ctx.request.url.searchParams.get('token')

    try {
      const userId = await getUserIdFromToken(token!)
      id = userId
    } catch (error) {
      console.error('no user found with token or id provided', error);
      console.error('token', token)
      ctx.response.status = 404
      ctx.response.body = {detail: "no user found with token or id provided", error: error}
      return
    }
    
  } else if (ctx.request.url.searchParams.has('id')) {
    id = ctx.request.url.searchParams.get('id')!
  } else {
    ctx.response.status = 400
    ctx.response.body = {detail: "no token or id provided"}
    return
  }

  const {data, error} = await supabaseAdmin.from('user_data').select("payment_status").eq('id', id).single()

  if (error) {
    console.error('no user found with token or id provided', error);
    console.error('id', id)
    ctx.response.status = 404
    ctx.response.body = {detail: "no user found with token or id provided"}
    return
  }

  ctx.response.status = 200
  ctx.response.body = {paymentStatus: data.payment_status}

})





async function jobDoneHandler(ctx: Context) {
  const body = ctx.request.body()
  const value = await body.value
  const jobName = value.jobName

  const response = await supabaseAdmin.from('job').select().eq('job_name', jobName).single()

  if (response.error) {
    console.error('Error getting job', response.error)
    ctx.response.status = 500
    return
  }

  const job = response.data

  const {data, error} = await supabaseAdmin.from('user_data').select("payment_status").eq('id', job.supabase_id).single()

  if (error) {
    console.error('Error getting payment status for invoicing', error)
    ctx.response.status = 500
    return
  }

  if (data.payment_status === "admin") {
    console.log("job payment status is admin, not sending to lago")
    ctx.response.status = 200
    return
  }

  const seconds = Math.ceil((new Date(job.finished_at).getTime() - new Date(job.created_at).getTime()) / 1000)
  // const minutes = Math.ceil((new Date(job.finished_at).getTime() - new Date(job.created_at).getTime()) / 60000)
  console.log("seconds", seconds)

  // console.log("minutes", minutes)

  const userId = job.supabase_id

  // const user = await getUserDataFromId(userId)
  // const lagoId = user.lago_id

  const url = LAGO_URL + '/events'

  const freePlanLagoId = "49a28eb3-a558-4027-baa4-bcbcc292eb96"

  // check hardware 
  const hardware = job.hardware_type
  console.log("hardware billed", hardware)

  if (!["cpu", "gpu"].includes(hardware)) {
    console.error('Error getting hardware', hardware)
    ctx.response.status = 500
    return
  }

  const payload = {
    "event": {
      "lago_subscription_id": freePlanLagoId,
      "transaction_id": jobName,
      "external_customer_id": userId,
      // "external_subscription_id": "maybe we need to setup this, this is for each customer",
      "code": job.hardware_type,
      "properties": {
          "seconds": seconds
      }
    }
  }

  const response2 = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + Deno.env.get('LAGO_API_KEY')
    },
    body: JSON.stringify(payload)
})

  if (response2.status != 200) {
    console.error('Error sending event to lago', response2)
    console.error("associated payload", payload)
    ctx.response.status = 500
    return
  }

  const response3 = await supabaseAdmin.from('job').update({ payment_status: "sent_to_lago" }).eq('job_name', jobName)

  if (response3.error) {
    console.error('Error updating job', response3.error)
    ctx.response.status = 500
    return
  }

  console.log("job payment status updated to sent_to_lago")

  ctx.response.status = 200
}




const app = new Application()
app.use(oakCors());
app.use(router.routes())
app.use(router.allowedMethods())

await app.listen({ port: 8000 })

