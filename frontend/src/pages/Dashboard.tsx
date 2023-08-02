import { useEffect, useState } from "react";
import { supabaseClient } from "../config/supabase-client"

export default function Dashboard() {
    
    
    
    const [data, setData] = useState(null);
    useEffect(() => {
        async function getData () {
            const { data, error } = await supabaseClient.functions.invoke('stripe-checkout-url')
            setData(data);
        }
        getData();
    }, []);

    console.log(data)
    
    // const access_token = (await supabaseClient.auth.getSession()).data.session!.access_token
    
    // call the url on click
    return (
        <div>
        <button onClick={() => {
            console.log(data)
        }}>Click me</button>
        </div>
        )
        
        
    }