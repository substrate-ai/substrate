import { useEffect, useState } from "react";
import { CreditCard } from 'tabler-icons-react';
import { Button } from "@/components/ui/button"
import { useNavigate } from "react-router-dom";
import { supabaseClient } from "src/config/supabase-client";

export default function BillingSection() {

    const navigate = useNavigate();
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState<any>(null);
    useEffect(() => {
        async function getData () {
            const { data, error } = await supabaseClient.functions.invoke('stripe-checkout-url')
            setData(data);
            setError(error);
        }
        getData();
    }, []);

    if (error) {
        console.error(error)
        return (
            <>
            <div>There was an with adding a payment method</div>
            </>
        )
    }

    return (
        <>
        
        
        <Button onClick={() => navigate(data?.checkoutUrl)} >
            <CreditCard size={48} />
            Add payment method
        </Button>

        <div>
            TODO LIST OF INVOICES
        </div>
        </>
    )
}