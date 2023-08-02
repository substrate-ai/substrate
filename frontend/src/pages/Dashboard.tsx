import { useEffect, useState } from "react";
import { supabaseClient } from "../config/supabase-client"
import { CreditCard } from 'tabler-icons-react';
import { Button } from "@/components/ui/button"
import BillingSection from "./dashboard-sections/BillingSection";

export default function Dashboard() {
    
    
    
    
    
    // const access_token = (await supabaseClient.auth.getSession()).data.session!.access_token
    
    // call the url on click
    return (   

        <BillingSection></BillingSection>

        )
        
        
    }