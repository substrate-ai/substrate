import { Application, Context, Router } from 'oak';
import { supabaseAdmin } from '../_shared/supabaseClients.ts';

const app = new Application();
const router = new Router();

router.post('/lago-webhook', async (ctx) => {
  const body = await ctx.request.body().value;

  const webhook_type = body.webhook_type;
  console.log('webhook_type', webhook_type);

  switch (webhook_type) {
    case 'invoice.payment_failure':
      await customerPaymentFailed(body, ctx);
      break;
    default:
      ctx.response.body = { detail: 'not implemented' };
      ctx.response.status = 200;
  }
});

async function customerPaymentFailed(body: any, ctx: Context) {
  const payment_provider_invoice_payment_error = body.payment_provider_invoice_payment_error
  const userId = payment_provider_invoice_payment_error.external_customer_id;
  const provider_error = payment_provider_invoice_payment_error.provider_error;

  if (provider_error.error_code == 'amount_too_small') {
    console.log("stripe amount too small, thus not charging customer")
    ctx.response.body = { detail: 'not charging customer for small jobs'};
    ctx.response.status = 200;
    return;
  }

  // block the user from creating new jobs
  const response = await supabaseAdmin.from('user_data')
    .update({ payment_status: 'payment_failed' })
    .eq('id', userId);

  if (response.error) {
    console.error('error updating user_data', response.error);
    ctx.response.body = { detail: 'error updating user_data' };
    ctx.response.status = 500;
  }

  ctx.response.body = { detail: 'ok' };
  
}

app.use(router.routes());
app.use(router.allowedMethods());

await app.listen({ port: 8000 });