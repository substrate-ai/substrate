import { createClient } from '@supabase/supabase-js';

// import from SUPABASE_URL and SUPABASE_ANON_KEY
const supabaseUrl: string = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey: string = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const supabaseClient = createClient(supabaseUrl, supabaseAnonKey);