import { Session, User } from '@supabase/supabase-js';
import { useState, useEffect, createContext, ReactNode } from 'react';
import { supabaseClient } from 'src/clients/supabaseClient';


// create a context for authentication
export const AuthContext = createContext<{ session: Session | null | undefined, user: User | null | undefined, signOut: () => void }>({ session: null, user: null, signOut: () => {} });

declare global {
    interface Window {
        analytics:any; // eslint-disable-line @typescript-eslint/no-explicit-any
    }
}

interface AuthProviderProps {
    children: ReactNode;
  }

export const AuthProvider = ({ children }: AuthProviderProps) => { 
    const [user, setUser] = useState<User>()
    const [session, setSession] = useState<Session | null>();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const setData = async () => {
            const { data: { session }, error } = await supabaseClient.auth.getSession();
            if (error) throw error;
            setSession(session)
            setUser(session?.user)
            setLoading(false);

            if ('analytics' in window) {
                window.analytics.identify(session?.user?.id, {
                    name: session?.user?.user_metadata?.full_name,
                    email: session?.user?.email,
                });

                // console.log('analytics')
            }

            
        };

        const { data: listener } = supabaseClient.auth.onAuthStateChange((_event, session) => {
            setSession(session);
            setUser(session?.user)
            setLoading(false)
        });

        setData();

        return () => {
            listener?.subscription.unsubscribe();
        };



    }, []);

    const value = {
        session,
        user,
        signOut: () => supabaseClient.auth.signOut(),
    };

    // use a provider to pass down the value
    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};