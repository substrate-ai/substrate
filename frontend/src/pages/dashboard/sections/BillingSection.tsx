import { useEffect, useState } from "react";
import { CreditCard } from 'tabler-icons-react';
import { Button } from "@/components/ui/button"
import { supabaseClient } from "src/clients/supabaseClient";
import { Loader2 } from "lucide-react"
import { useGetPaymentStatusQuery } from "src/api/payment";
 
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"


export default function BillingSection() {

    const [loading, setLoading] = useState(true);
    const [checkoutUrl, setCheckoutUrl] = useState<string | null>(null);
    const [errorCheckoutUrl, setCheckoutUrlError] = useState<any>(null); // eslint-disable-line @typescript-eslint/no-explicit-any
 
    const {data, isSuccess, isError, error} = useGetPaymentStatusQuery();

    if (isError) {
        console.error(error)
    }

    useEffect(() => {
        async function getData () {
            const { data, error } = await supabaseClient.functions.invoke('stripe-checkout-url', {
                method: 'GET'}
                )
            setCheckoutUrl(data?.checkoutUrl);
            setCheckoutUrlError(error);
            if (!error) {
                setLoading(false)
            }
        }
        getData();
    }, []);

    if (errorCheckoutUrl) {
        console.error(errorCheckoutUrl)
        return (
            <>
            <p>
                Could not get checkout url
            </p>
            <p>
                Error message: {errorCheckoutUrl.message}
            </p>
            </>
        )
    }

    return (
        <>
            { isSuccess ?
                <Alert>
                    <AlertTitle>Payment status</AlertTitle>
                    <AlertDescription>
                        {data.paymentStatus}
                    </AlertDescription>
                </Alert>
                : null
            }

            <div className="h-9"></div>
        
        
            <Button onClick={() => {

                window.location.replace(checkoutUrl!)
                return null
            }} disabled={loading}>
                {loading ? <Loader2 className="animate-spin" size={24} /> : null}
                <CreditCard size={32} />
                Add a payment method
            </Button>

        </>
    )
}