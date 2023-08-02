import { SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = Deno.env.get('_SUPABASE_URL');
const supabaseKey = Deno.env.get('_SUPABASE_ANON_KEY');

if (!supabaseUrl || !supabaseKey) {
    throw new Error('Missing SUPABASE_URL or SUPABASE_KEY');
}

export const supabaseClient = new SupabaseClient(supabaseUrl, supabaseKey);



