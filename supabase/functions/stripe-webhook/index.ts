import { Application, Router } from 'oak';
import { supabaseAdmin } from '../_shared/supabaseClients.ts';
import { LAGO_URL } from "../_shared/lagoUrl.ts";

const app = new Application();
const router = new Router();

router.post('/stripe-webhook', async (ctx) => {
  // handle stripe webhook payment_method.attached, payment_method.updated, payment_method.automatic_updated
  const body = await ctx.request.body().value;

  if (!body) {
    ctx.response.status = 400;
    ctx.response.body = { error: 'no body' };
    return;
  }

  switch (body.type) {
    case 'payment_method.attached':
      await handle_payment_method(body.data.object)
      break;
    case 'payment_method.updated':
      await handle_payment_method(body.data.object)
      break;
    case 'payment_method.automatic_updated':
      await handle_payment_method(body.data.object)
      break;
    default:
      console.error('Unhandled event type', body.type)
      break;
  }

  ctx.response.status = 200;
  ctx.response.body = { received: true };
});

async function handle_payment_method(event: any) {

    const stripeId = event.customer

    const {data, error} = await supabaseAdmin.from('user_data').select().eq('stripe_id', stripeId).single()

    if (error) {
      console.error('error getting user from stripe_id', error);
      console.error('stripeId', stripeId)
      return;
    }

    if (data.payment_status === "payment_failed") {
      handle_user_with_failed_payment(data.id)
    }

    const {data : data2, error: error2} = await supabaseAdmin.from('user_data').update({status: 'active'}).eq('stripe_id', stripeId).single()

    if (error2) {
      console.error('error updating user after new credit card', error2);
      return;
    }

}

async function handle_user_with_failed_payment(userId: string) {
  const invoices = await get_failed_invoice(userId)
  retry_failed_invoice(invoices)
}

function retry_failed_invoice(invoices: string[]) {

  invoices.forEach(async (invoice: any) => {

    const invoiceId = invoice.lago_id
    
    const response = await fetch(`${LAGO_URL}/invoices/${invoiceId}/retry_payment`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${Deno.env.get('LAGO_API_KEY')}`,
      },
    });

    if (response.status !== 200) {
      console.error('error retrying invoice', response);
      throw new Error('error retrying invoice')
    }

  })
}

async function get_failed_invoice(userId: string): Promise<string[]> {
  const invoices: string[] = [];
  const externalCustomerId = userId;
  const paymentStatus = 'failed';
  const perPage = 20;

  const query = `?external_customer_id=${externalCustomerId}&payment_status=${paymentStatus}&per_page=${perPage}`;

  const response = await fetch(`${LAGO_URL}/invoices${query}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${Deno.env.get('LAGO_API_KEY')}`,
    },
  });

  if (response.status !== 200) {
    console.error('Error retrying invoice', response);
    throw new Error('Error retrying invoice');
  }

  const body = await response.json();
  const pages = body.pages;

  invoices.push(...body.invoices);

  if (pages > 1) {
    for (let i = 2; i <= pages; i++) {
      const pageResponse = await fetch(`${LAGO_URL}/invoices${query}&page=${i}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${Deno.env.get('LAGO_API_KEY')}`,
        },
      });

      if (pageResponse.status !== 200) {
        console.error('Error retrying invoice', pageResponse);
        throw new Error('Error retrying invoice');
      }

      const pageBody = await pageResponse.json();
      invoices.push(...pageBody.invoices);
    }
  }

  return invoices;
}





    

app.use(router.routes());
app.use(router.allowedMethods());

await app.listen({ port: 8000 });