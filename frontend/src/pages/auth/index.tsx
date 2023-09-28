import { Auth } from '@supabase/auth-ui-react'
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { supabaseClient } from 'src/clients/supabaseClient';
import { AuthView } from 'src/pages/auth/AuthViewEnum';

type Props = {
  view: AuthView
}

export function AuthPage({ view }: Props) {


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
          redirectTo={`${window.location.origin}/dashboard`}
          // redirectTo='/dashboard'
          view={view}
          /> 
          </div>
        
      </div>
      </div>
    )
        
}