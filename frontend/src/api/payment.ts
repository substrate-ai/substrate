import { useQuery } from "@tanstack/react-query";
import { useAuth } from "src/hooks/Auth";
import axios from "axios";




export function useGetPaymentStatusQuery() {
    const id = useAuth().session!.user.id

    return useQuery(['payment_status'], async () => {
        const payload = {   
            id: id
        }
        
        const headers = { 'Authorization': `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}` }
        

        const response = await axios.get(import.meta.env.VITE_SUPABASE_URL + "/functions/v1/payment/user-status", {
            headers: headers,
            params: payload
        })
        

        if (response.status !== 200) {
            console.log("response", response)
            throw new Error("error getting payment status")
        }

        return response.data

    });
  }

