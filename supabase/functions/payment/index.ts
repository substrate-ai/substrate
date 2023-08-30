import { Application, Context, Router } from 'oak'
import { supabaseAdmin } from '../_shared/supabaseClients.ts'
import { LAGO_URL } from '../_shared/lagoUrl.ts';
import { oakCors } from "https://deno.land/x/cors@v1.2.2/mod.ts";
import { getUserFromId } from "../_shared/userUtils.ts";
import getUserIdFromToken from "../_shared/tokenUtils.ts";


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

    const userId = await getUserIdFromToken(token!)

    id = userId
  } else if (ctx.request.url.searchParams.has('id')) {
    id = ctx.request.url.searchParams.get('id')!
  } else {
    ctx.response.status = 400
    return
  }

  const {data, error} = await supabaseAdmin.from('user_data').select().eq('id', id).single()

  if (error) {
    console.error('error getting user from id', error);
    console.error('id', id)
    ctx.response.status = 500
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

  const minutes = Math.ceil((new Date(job.finished_at).getTime() - new Date(job.created_at).getTime()) / 60000)

  console.log("minutes", minutes)

  const userId = job.supabase_id

  const user = await getUserFromId(userId)
  const lagoId = user.lago_id

  const url = LAGO_URL + '/v1/events'

  const freePlanLagoId = "9c3b45cb-7f6c-4d17-bb5d-181f9e540760"

  // check hardware 
  const hardware = job.hardware
  if (!["cpu", "gpu"].includes(hardware)) {
    console.error('Error getting hardware', hardware)
    ctx.response.status = 500
    return
  }

  const payload = {
    "event": {
      "lago_subscription_id": freePlanLagoId,
      "transaction_id": job.id,
      "external_customer_id": userId,
      // "external_subscription_id": "maybe we need to setup this, this is for each customer",
      "code": job.hardware,
      "properties": {
          "minutes": minutes
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

ctx.response.status = 200
}




const app = new Application()
app.use(oakCors());
app.use(router.routes())
app.use(router.allowedMethods())

await app.listen({ port: 8000 })

