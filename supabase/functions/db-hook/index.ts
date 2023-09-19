import { Application, Context, Router } from 'oak';
import { supabaseAdmin } from '../_shared/supabaseClients.ts';
import { LAGO_URL } from "../_shared/lagoUrl.ts";

const app = new Application();
const router = new Router();


router.post('/db-hook', async (ctx) => {
  const parameter = ctx.request.url.searchParams.get('method');

  switch (parameter) {
    case 'create-lago-customer':
      await createLagoCustomer(ctx);
      break;

    default:
      ctx.response.status = 400;
      ctx.response.body = { error: 'no method' };
      break;
  }

})


async function createLagoCustomer(ctx: Context) {
  const body = await ctx.request.body().value;


  if (!body) {
    ctx.response.status = 400;
    ctx.response.body = { error: 'no body' };
    return;
  }


  const email = body.record.email
  const supabaseId = body.record.id

  const payloadCreateCustomer = {
    customer: {
      email: email,
      name: email,
      external_id: supabaseId,
      billing_configuration: {
        payment_provider: 'stripe',
        sync: true,
        sync_with_provider: true,
        provider_payment_methods: ['card']
      }
    }

  };

  const responseCreateCustomer = await fetch(`${LAGO_URL}/customers`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${Deno.env.get('LAGO_API_KEY')}`,
    },
    body: JSON.stringify(payloadCreateCustomer),
  });

  if (responseCreateCustomer.status !== 200) {
    console.error('error creating customer', responseCreateCustomer);
    console.error('payloadCreateCustomer', payloadCreateCustomer)
    ctx.response.status = 500;
    ctx.response.body = { error: 'error creating customer', response: responseCreateCustomer };
    return;
  }


  const lagoBody = (await responseCreateCustomer.json())

  const payloadSupabase = {
    lago_id: lagoBody.customer.lago_id,
    stripe_id: lagoBody.customer.billing_configuration.provider_customer_id
  };

  const { data, error } = await supabaseAdmin.from('user_data').update(payloadSupabase).eq('id', supabaseId);

  if (error) {
    console.error('error saving lago id to supabase', error);
    console.error('payload', payloadSupabase)
    console.error('supabaseId', supabaseId)
    ctx.response.status = 500;
    ctx.response.body = { error: 'error saving lago id to supabase', response: error };
    return;
  }

  const uuid = crypto.randomUUID();
  const planCode = 'free';

  const payloadAssignPlan = {
    subscription: {
      external_customer_id: supabaseId,
      plan_code: planCode,
      external_id: `sub_id_${uuid}`,
    }
  };


  const responseAssignPlan = await fetch(`${LAGO_URL}/subscriptions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${Deno.env.get('LAGO_API_KEY')}`,
    },
    body: JSON.stringify(payloadAssignPlan),
  });

  if (responseAssignPlan.status !== 200) {
    console.error('error assigning plan', responseAssignPlan);
    console.error('payloadAssignPlan', payloadAssignPlan)
    ctx.response.status = 500;
    ctx.response.body = { error: 'error assigning plan', response: responseAssignPlan };
    return;
  }

  ctx.response.status = 200;
}

app.use(router.routes());
app.use(router.allowedMethods());

await app.listen({ port: 8000 });