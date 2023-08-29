import { Application, Router } from 'oak';
import { stripe } from '../_shared/stripeClient.ts';
import { getUserFromContext } from '../_shared/userUtils.ts';
import { oakCors } from "https://deno.land/x/cors@v1.2.2/mod.ts";
import { LAGO_URL } from "../_shared/lagoUrl.ts";

const router = new Router();
router.get('/stripe-checkout-url', async (ctx) => {  
  const supabaseUser = await getUserFromContext(ctx);
  const supabaseId = supabaseUser.id;

  const lagoResponse = await fetch(`${LAGO_URL}/customers/${supabaseId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${Deno.env.get('LAGO_API_KEY')}`,
    },
  });

  if (lagoResponse.status !== 200) {
    console.error('error getting customer', lagoResponse);
    console.error('supabaseId', supabaseId)
    ctx.response.status = 500;
    ctx.response.body = { error: 'error getting customer', response: lagoResponse };
    return;
  }

  const lagoCustomer = (await lagoResponse.json());
  const stripeId = lagoCustomer.customer.billing_configuration.provider_customer_id

  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    mode: 'setup',
    customer: stripeId,
    success_url: 'https://substrateai.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url: 'https://substrateai.com/cancel',
  });

  if (session.error) {
    console.error('error creating session', session.error);
    console.error('supabaseId', supabaseId)
    console.error('stripeId', stripeId)
    ctx.response.status = 401;
    ctx.response.body = { error: 'error creating session' };
    return;
  }

  ctx.response.status = 200;
  ctx.response.body = { checkoutUrl: session.url };
});

const app = new Application()
app.use(oakCors())
app.use(router.routes())
app.use(router.allowedMethods())
await app.listen({ port: 8000 });