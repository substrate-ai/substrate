import { Application, Router } from 'oak'
import { supabaseAdmin, supabaseAnon } from '../_shared/supabaseClients.ts'
import getUserIdFromToken from "../_shared/tokenUtils.ts";

const router = new Router()
router
  // Note: path should be prefixed with function name
  .post('/aws/job-done', async (ctx) => {
      console.log('Job done 3')
      if (!ctx.request.hasBody) {
        ctx.throw(400, 'Body is required')
      }
      
      const body = ctx.request.body()
      const value = await body.value
      const details = value.detail
      const trainingJobStatus = details.TrainingJobStatus
      const trainingJobName = details.TrainingJobName
      // const time = details.TrainingEndTime
      const time = ((new Date()).toISOString()).toLocaleString()

      // Todo do payment stuff here


      const {data, error} = await supabaseAdmin.from('job').update({ status: trainingJobStatus, finished_at: time }).eq('job_name', trainingJobName)

      if (error) {
        console.error('Error updating job', error)
        ctx.response.status = 500
        return
      }

      await supabaseAnon.functions.invoke('payment/job-done', {body: {jobName: trainingJobName}})

      // return 200

      ctx.response.status = 200

      


  })
  .post('/aws/get-jobs', async (ctx) => {
    const result = ctx.request.body();
    const value = await result.value;
    const token = value.accessToken

    const userId = await getUserIdFromToken(token)

    const {data, error} = await supabaseAdmin.from('job').select('job_name, created_at, finished_at, hardware, status').eq('supabase_id', userId).order('created_at', {ascending: false})

    if (error) {
      console.error('Error getting jobs', error)
      ctx.response.status = 500
      return
    }

    ctx.response.body = data    
  })




const app = new Application()
app.use(router.routes())
app.use(router.allowedMethods())

await app.listen({ port: 8000 })