import Stripe from "https://esm.sh/stripe@12.16.0?target=Deno"

export const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY') as string, {
    // This is needed to use the Fetch API rather than relying on the Node http package.
    apiVersion: '2022-11-15',
    httpClient: Stripe.createFetchHttpClient(),
  })