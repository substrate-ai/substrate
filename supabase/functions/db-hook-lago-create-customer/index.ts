import { serve } from "https://deno.land/std@0.168.0/http/server.ts"


serve(async (req) => {
  const body = await req.json()

  const email = body.email
  const supabaseId = body.id

  const payloadCreateCustomer = {
    email: email,
    external_id: supabaseId,

    billing_configuration: {
      payment_provider: "stripe",
      sync: true,
      sync_with_provider: true,
      provider_payment_methods: [
        "card",
      ]
    }
  }

  // create customer in lago
  const responseCreateCustomer = await fetch(`${Deno.env.get('LAGO_URL')}/customers`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${Deno.env.get('LAGO_API_KEY')}`
    },
    body: JSON.stringify(payloadCreateCustomer),
  })

  if (responseCreateCustomer.status !== 200) {
    console.error("error creating customer", responseCreateCustomer)
    return new Response(
      JSON.stringify({ error: "error creating customer", response: responseCreateCustomer }),
      { headers: { "Content-Type": "application/json" }, status: 401 },
    )
  }

  const uuid = crypto.randomUUID();


  const payloadAssignPlan = {
    external_customer_id: supabaseId,
    plan_code: "free",
    external_id: `sub_id_${uuid}`
  }

  // assign plan to customer in lago
  const responseAssignPlan = await fetch(`${Deno.env.get('LAGO_URL')}/subscriptions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${Deno.env.get('LAGO_API_KEY')}`
    },
    body: JSON.stringify(payloadAssignPlan),
  })

  if (responseAssignPlan.status !== 200) {
    console.error("error assigning plan", responseAssignPlan)
    return new Response(
      JSON.stringify({ error: "error assigning plan", response: responseAssignPlan }),
      { headers: { "Content-Type": "application/json" }, status: 401 },
    )
  }

  return new Response()





  
})
