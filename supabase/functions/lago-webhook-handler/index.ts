import { Application, Router } from 'oak';
import { supabaseAdmin } from '../_shared/supabaseClients.ts';

const app = new Application();
const router = new Router();

router.post('/', async (ctx) => {
  const body = await ctx.request.body().value;

  const webhook_type = body.webhook_type;

  switch (webhook_type) {
    // case 'customer.payment_provider_created':
    //   ctx.response.body = await customerCreatedHandler(body);
    //   break;
    case 'invoice.payment_failure':
      ctx.response.body = await customerPaymentFailed(body);
      break;
    default:
      console.error('not implemented webhook_type', webhook_type);
      ctx.response.body = JSON.stringify({ error: 'not implemented' });
      ctx.response.status = 501;
  }
});

async function customerPaymentFailed(body: any) {
  const userId = body.payment_provider_invoice_payment_error.external_customer_id;

  const response = await supabaseAdmin.from('user_data')
    .update({ status: 'payment_failed' })
    .eq('id', userId);

  if (response.error) {
    console.error('error updating user_data', response.error);
    return JSON.stringify({ error: 'error updating user_data' });
  }

  return '';
}

async function customerCreatedHandler(body: any) {
  console.log('checkout_url_generated');

  const supabaseId = body.customer.external_id;
  const stripeId = body.customer.billing_configuration.payment_provider_id;
  const lagoId = body.customer.lago_id;

  const response = await supabaseAdmin.from('user_data')
    .update({ stripe_id: stripeId, lago_id: lagoId })
    .eq('id', supabaseId);

  if (response.error) {
    console.error('error updating user_data', response.error);
    return JSON.stringify({ error: 'error updating user_data' });
  }

  return '';
}

app.use(router.routes());
app.use(router.allowedMethods());

await app.listen({ port: 8000 });