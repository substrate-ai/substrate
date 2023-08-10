import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { stripe } from "../_shared/stripeClient.ts"
import { corsHeaders } from '../_shared/cors.ts'
import { getUserFromServe } from "../_shared/getUserFromRequest.ts";
import { supabaseAnon } from "../_shared/supabaseClients.ts";


// Tp be called from frontend
serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  const supabaseUser = await getUserFromServe(req)
  const supabaseId = supabaseUser.id

  const queryStripeId = await supabaseAnon.from('user_data')
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