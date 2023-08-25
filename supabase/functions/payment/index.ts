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

    const userId = job.supabase_id

    const user = await getUserFromId(userId)
    const lagoId = user.lago_id

    const url = Deno.env.get('LAGO_API_URL') + '/v1/events'
    const payload = {
      "lago_id": lagoId,
      "event_type": "job_finished",
      "event_data": {
        "job_name": jobName,
        "hardware": job.hardware,
        "status": job.status,
        "created_at": job.created_at,
        "finished_at": job.finished_at
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
    ctx.response.status = 500
    return
  }

  ctx.response.status = 200
})




const app = new Application()
app.use(router.routes())
app.use(router.allowedMethods())

await app.listen({ port: 8000 })

