// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { corsHeaders } from "../_shared/cors.ts";
import { stripe } from "../_shared/stripeClient.ts";
import { supabaseClient } from "../_shared/supabaseClient.ts";

console.log("Hello from Functions!")

serve(async (req) => {

  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  console.log("req", req)

  const {data, error} = (await supabaseClient.auth.getUser(req.headers.get('Authorization')!))

  if (error) {
    console.error("error getting user", error)
    return new Response(
      JSON.stringify({ error: "error getting user" }),
      { headers: { "Content-Type": "application/json" }, status: 401 },
    )
  }

  const supabaseId = data.user.id

  const queryStripeId = await supabaseClient.from('user_data')
                            .select('stripe_id').eq('id', supabaseId).single()

  if (queryStripeId.error) {
    console.error("error getting stripe_id", queryStripeId.error)
    return new Response(
      JSON.stringify({ error: "error getting stripe_id" }),
      { headers: { "Content-Type": "application/json" }, status: 401 },
    )
  }

  const stripeId = queryStripeId.data.stripe_id

  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    mode: 'setup',
    customer: stripeId,
    success_url: 'https://substrateai.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url: 'https://substrateai.com/cancel',
  });

  if (session.error) {
    console.error("error creating session", session.error)
    return new Response(
      JSON.stringify({ error: "error creating session" }),
      { headers: { "Content-Type": "application/json" }, status: 401 },
    )
  }
  
  return new Response(JSON.stringify({"checkout_url": session.url}), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    status: 200,
  })
})

// To invoke:
// curl -i --location --request POST 'http://localhost:54321/functions/v1/' \
//   --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \
//   --header 'Content-Type: application/json' \
//   --data '{"name":"Functions"}'
