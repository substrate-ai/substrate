# Supabase backend

This is the main backend, please use this one by default and only python-backend if something cannot be done in Supabase.
Supabase is a serverless framework

The functions folders list all of functions:
- aws:
    this is an aws-webhook, aws event-bridge calls this endpoint on certain events that happens on AWS. An example of such event is when a sagemaker job is done
- db-hook
    This function is supabase specific. The methods called in the functions are trigger when certain events happen in the database, such as a row that is added (for example on user sign-in)
- lago-webhook
    This is called by lago (invoicing and billing platform) (lago.substrateai.com), so that we can react on events link to billing. An example of such is when a user invoice payment fails, in that case we temporary suspent new user jobs
- payement
    Managed all payment logics.
- stripe-checkout-url
    When a user wants to add a credit card, we receive a checkout link from stripe for user to add its credit card
- stripe-webhook
    This is called by stripe (stripe.com). Strip generate events that we then react on. For example we want to retry failed invoices when a user update its payment method (credit card)
- token
    The cli relies on tokens for authentification (cf. `substrate-ai login`). This function handle all the authentification linked to cli user token. For example, how to get a certain user based on its token
- user
    To get info about a user, for example its payment status

The _shared folder contains a list of methods that are used by multiple functions


# Refractoring TODO
    - remove stripe-checkout-url folder and integrate it into another folder
    - rename aws to aws-webhook

# Commands

Please look at the supabase functions documentation on how to serve functions locally 

To configure secrets
`supabase secrets set --env-file /Users/baptiste/Git/substrate/supabase/functions/.env`