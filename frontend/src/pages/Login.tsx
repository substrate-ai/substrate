import { Auth } from '@supabase/auth-ui-react'
import { useNavigate } from "react-router-dom";
import { createClient } from '@supabase/supabase-js';
import { supabaseClient } from '../config/supabase-client';
import { ThemeSupa } from '@supabase/auth-ui-shared'

export default function AuthPage() {
    return(
      <Auth
      supabaseClient={supabaseClient}
      appearance={{theme: ThemeSupa}}
      theme="dark" 
      providers={['github']}
    /> 
    )
        
}