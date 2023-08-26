import { Application, Router } from 'oak'
import { supabaseAdmin, supabaseAnon } from '../_shared/supabaseClients.ts'
import getUserIdFromToken from "../_shared/tokenUtils.ts";
// import { STS, AssumeRoleCommand } from 'https://deno.land/x/aws_sdk@v3.32.0-1/client-sts/mod.ts'

console.log(Deno.env.get('SUPABASE_KEY'))


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

  // NOT WORKING
  // .post('/aws/get-credentials', async (ctx) => {
  //   // console.log('get credentials')
  //   // const result = ctx.request.body();
  //   // const value = await result.value;
  //   // const token = value.accessToken

  //   // const userId = await getUserIdFromToken(token)
  //   const userId = "user1"
  //   const roleArn = "arn:aws:iam::038700340820:user/CLI"

  //   const accessKeyId = Deno.env.get('AWS_ACCESS_KEY_ID')!
  //   const secretAccessKey = Deno.env.get('AWS_SECRET_ACCESS_KEY')!
  //   const region = Deno.env.get('AWS_REGION')!

  //   console.log("accessKeyId", accessKeyId)
  //   console.log("secretAccessKey", secretAccessKey)
  //   console.log("region", region)
  //   console.log("userId", userId)

  //   // use STS to get temporary credentials
  //   const sts = new STS({region: region, credentials: {accessKeyId: accessKeyId, secretAccessKey: secretAccessKey}})
  //   const params = {
  //     RoleArn: roleArn,
  //     RoleSessionName: userId,
  //     DurationSeconds: 900,
  //   }

  //   console.log("params", params)

  //   const command = new AssumeRoleCommand(params)

  //   console.log("command", command)
    
  //   const response = await sts.send(command)

  //   console.log("response", response)

  //   if (response.Credentials) {
  //     ctx.response.body = response.Credentials
  //   }
  //   else {
  //     ctx.response.status = 500
  //   }

  // })




const app = new Application()
app.use(router.routes())
app.use(router.allowedMethods())

await app.listen({ port: 8000 })