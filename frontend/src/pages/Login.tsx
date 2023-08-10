import { Auth } from '@supabase/auth-ui-react'
import { useNavigate } from "react-router-dom";
import { createClient } from '@supabase/supabase-js';
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { supabaseClient } from 'src/config/supabase-client';

export default function AuthPage() {


    return(
      <Auth
      supabaseClient={supabaseClient}
      appearance={{theme: ThemeSupa}}
      theme="dark" 
      providers={['github']}
      redirectTo='/dashboard'
    /> 
    )
        
}