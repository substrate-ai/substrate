import { Application, Router } from 'oak'
import { supabaseAdmin } from '../_shared/supabaseClients.ts'
import { getUserFromId } from "../_shared/userUtils.ts";

const router = new Router()
router
  // Note: path should be prefixed with function name
  .post('/payment/job-done', async (ctx) => {

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

    const userId = job.supabase_id

    const user = await getUserFromId(userId)
    const lagoId = user.lago_id

    const url = Deno.env.get('LAGO_API_URL') + '/v1/events'

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
        "code": "CPU",
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
  

  // update job payment  status to send to lago

  ctx.response.status = 200
})




const app = new Application()
app.use(router.routes())
app.use(router.allowedMethods())

await app.listen({ port: 8000 })

