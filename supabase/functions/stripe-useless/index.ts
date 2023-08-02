import Stripe from 'stripe'
import { supabaseAdmin } from "../_shared/supabaseAdmin.ts";

console.log("Hello from Functions!")

Deno.serve(async (req: Request) => {


  const searchParams = new URLSearchParams();

  switch (searchParams.get('function')) {
    case 'createCustomer':
      return await createCustomerHandler(req)
    case 'createUsageRecord':
      return await createUsageRecordHandler(req)
    case 'createSubscription':
      return await createSubscriptionHandler(req)
    default:
      return new Response("Function not found", {status: 404})
  }
})

async function createUsageRecordHandler(req: Request) {
  // todo
  return new Response()
}

async function createSubscriptionHandler(req: Request) {
  // todo
  return new Response()
}

async function createCustomerHandler(req: Request) {

  const body = await req.json()

  const email = body.record.email

  console.log("email", email)

  console.log("stripe secret key", Deno.env.get('STRIPE_SECRET_KEY_2'))


  const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY_2') as string, {
    // This is needed to use the Fetch API rather than relying on the Node http
    // package.
    apiVersion: '2022-11-15',
    httpClient: Stripe.createFetchHttpClient(),
  })


  // TODO update the database of users to include foregin key instead of generated id



  console.log("stripe client created", stripe)

  console.log("customer", await stripe.customers.create({
    email: email
  }))

  const customer = await stripe.customers.create({
    email: email
  });

  console.log("customer created")

  const stripeId = customer.id

  console.log("stripeId", stripeId)

  const response = await supabaseAdmin.from('user')
  .update({ customer_id: stripeId})
  .eq('email', email)

  console.log("response", response)

  console.log("customer update database")


  return new Response()

}

// To invoke:
// curl -i --location --request POST 'http://localhost:54321/functions/v1/' \
//   --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \
//   --header 'Content-Type: application/json' \
//   --data '{"name":"Functions"}'
