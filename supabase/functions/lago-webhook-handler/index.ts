// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

import { verify } from "https://deno.land/x/djwt@v2.9.1/mod.ts"
import { supabaseAdmin } from "../_shared/supabaseClients.ts";





serve(async (req) => {

  const body = await req.json()

  const webhook_type = body.webhook_type

  switch (webhook_type) {
    case "customer.checkout_url_generated":
      return ignoreHandler()
    case "customer.payment_provider_created":
      return await customerCreatedHandler(body)
    default:
      console.error("not implemented webhook_type", webhook_type)
      return new Response(
        JSON.stringify({ error: "not implemented" }),
        { headers: { "Content-Type": "application/json" }, status: 501 },
      )
  }

})

function ignoreHandler(): Response {
  return new Response()
}

async function customerCreatedHandler(req: Request): Promise<Response> {
  console.log("checkout_url_generated")

  const body = await req.json()

  const supabaseId = body.customer.external_id
  const stripeId = body.customer.billing_configuration.payment_provider_id
  const lagoId = body.customer.lago_id

  const response = await supabaseAdmin.from('user_data')
  .update({ stripe_id: stripeId, lago_id: lagoId})
  .eq('id', supabaseId)

  if (response.error) {
    console.error("error updating user_data", response.error)
    return new Response(
      JSON.stringify({ error: "error updating user_data" }),
      { headers: { "Content-Type": "application/json" }, status: 501 },
    )
  }

  return new Response()
}
