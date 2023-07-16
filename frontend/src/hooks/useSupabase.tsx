import { createClient } from '@supabase/supabase-js'

export default function useSupabase() {


    const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_KEY!)
}