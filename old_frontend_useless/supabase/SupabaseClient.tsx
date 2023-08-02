// import { SupabaseClient, createClient } from '@supabase/supabase-js'
// import { create } from 'zustand'

// interface SupabaseContext {
//     supabase: SupabaseClient
//   }

// export const useSupabase = create<SupabaseContext>()(() => ({
//     // todo remove the keys
//     supabase: createClient("", "")
//     // useEffect(() => {
//     //     const { data } = supabase.auth.onAuthStateChange((event, session) => {
//     //       if (event === "SIGNED_IN") {
//     //         setUser(session.user);
//     //         setAuth(true);
//     //       }
//     //     });
//     //     return () => {
//     //       data.subscription.unsubscribe();
//     //     };
//     //   }, [.supabase]);

// }))

import { createClient } from '@supabase/supabase-js'

const supabaseUrl = ""
const supabaseAnonKey = ""
// const options = {
//     // db: {
//     //   schema: 'public',
//     // },
//     auth: {
//       autoRefreshToken: true,
//       persistSession: true,
//       detectSessionInUrl: true,
//       storage: localStorage,
//     },
//     // global: {
//     //   headers: { 'x-my-custom-header': 'my-app-name' },
//     // },
//   }

export const supabaseClient = createClient(supabaseUrl, supabaseAnonKey)



