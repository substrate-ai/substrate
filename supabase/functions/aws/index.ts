import { Application, Router } from 'oak'
import { supabaseAdmin } from '../_shared/supabaseClients.ts'

const router = new Router()
router
  // Note: path should be prefixed with function name
  .post('/aws/job-done', async (context) => {
      console.log('Job done 3')
      if (!context.request.hasBody) {
        context.throw(400, 'Body is required')
      }
      
      const body = context.request.body()
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
        context.response.status = 500
        return
      }
        
      
      // return 200

      context.response.status = 200

      


  })
  .post('/aws/get-running-jobs', async (context) => {
    
  })
  .get('/aws/stop-job/{id}', (context) => {
    
  })

const app = new Application()
app.use(router.routes())
app.use(router.allowedMethods())

await app.listen({ port: 8000 })