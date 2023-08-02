// import {supabase} from '@supabase/supabase-js'
import { Auth } from '@supabase/auth-ui-react'
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { useNavigate } from "react-router-dom";
import { createClient } from '@supabase/supabase-js';
import { supabaseClient } from '../supabase/SupabaseClient';




export default function AuthPage() {
    


    


    return(

        <Auth
        supabaseClient={supabaseClient}
        appearance={{ theme: ThemeSupa }}
        theme="dark"
        // magicLink
        providers={['github']}


        
    />)
        
}