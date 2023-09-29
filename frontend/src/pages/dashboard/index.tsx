import {DashboardLayout} from "src/pages/dashboard/components/DashboardLayout";
import { Outlet } from "react-router-dom"


export default function Dashboard() {
    
    
    
    
    
    // const access_token = (await supabaseClient.auth.getSession()).data.session!.access_token
    
    // call the url on click
    return (   
        <DashboardLayout>
            {/* <BillingSection></BillingSection> */}
            <Outlet />
        </DashboardLayout>


        )
        
        
    }