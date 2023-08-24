import { Auth } from '@supabase/auth-ui-react'
import { useNavigate } from "react-router-dom";
import { createClient } from '@supabase/supabase-js';
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { supabaseClient } from 'src/config/supabase-client';

export default function AuthPage() {


    return(
      <div className="flex h-screen">
      <div className="m-auto">
          <div className='w-96'>
          <Auth
          supabaseClient={supabaseClient}
          appearance={{
            theme: ThemeSupa,
              variables: {
                default: {
                  colors: {
                    brand: 'black',
                    brandAccent: 'grey',
                  },
                },
              },
            }}
          theme="dark" 
          providers={['github']}
          redirectTo='/dashboard'
          /> 
          </div>
        
      </div>
      </div>
    )
        
}