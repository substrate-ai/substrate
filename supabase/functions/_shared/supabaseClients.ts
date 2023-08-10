import { SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = Deno.env.get('_SUPABASE_URL');
const supabaseAnonKey = Deno.env.get('_SUPABASE_ANON_KEY');
const supabaseServiceRoleKey = Deno.env.get('_SUPABASE_SERVICE_ROLE_KEY');


if (!supabaseUrl || !supabaseAnonKey || !supabaseServiceRoleKey) {
    throw new Error('Missing SUPABASE_URL or SUPABASE_KEY');
}

export const supabaseAnon = new SupabaseClient(supabaseUrl, supabaseAnonKey);
export const supabaseAdmin = new SupabaseClient(supabaseUrl, supabaseServiceRoleKey);

