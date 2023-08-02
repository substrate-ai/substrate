import { SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = Deno.env.get('_SUPABASE_URL');
const supabaseKey = Deno.env.get('_SUPABASE_SERVICE_ROLE_KEY');

if (!supabaseUrl || !supabaseKey) {
    throw new Error('Missing SUPABASE_URL or SUPABASE_KEY');
}

export const supabaseAdmin = new SupabaseClient(supabaseUrl, supabaseKey);



