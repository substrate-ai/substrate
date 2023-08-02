import Stripe from "https://esm.sh/stripe@12.16.0?target=Deno"

// todo fix stripe has no type definition (submit a github issue)
export const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY_2') as string, {
    // This is needed to use the Fetch API rather than relying on the Node http
    // package.
    apiVersion: '2022-11-15',
    httpClient: Stripe.createFetchHttpClient(),
  })