import { useEffect, useState } from "react";
import { CreditCard } from 'tabler-icons-react';
import { Button } from "@/components/ui/button"
import { useNavigate } from "react-router-dom";
import { supabaseClient } from "src/config/supabase-client";
import { Loader2 } from "lucide-react"


export default function BillingSection() {

    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState<any>(null);

    useEffect(() => {
        async function getData () {
            const { data, error } = await supabaseClient.functions.invoke('stripe-checkout-url', {
                method: 'GET'}
                )
            setData(data);
            setError(error);
            if (!error) {
                setLoading(false)
            }
        }
        getData();
    }, []);

    if (error || data?.checkoutUrl === null) {
        console.error(error)
        return (
            <div>
                There was a server error preventing you from adding a payment method. Please contact support or try again later.
            </div>
        )
    }

    return (
        <>
        
        
            <Button onClick={() => {

                window.location.replace(data?.checkoutUrl)
                return null
            }} disabled={loading}>
                {loading ? <Loader2 className="animate-spin" size={24} /> : null}
                <CreditCard size={32} />
                Add a payment method
            </Button>


            {/* TODO LIST OF INVOICES */}

        </>
    )
}