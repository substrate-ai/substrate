import { useSearchParams } from "react-router-dom";

export default function DashboardPage() {

    const [searchParams, setSearchParams] = useSearchParams();

    



    const access_token = searchParams.get("access_token")

    return (
        
        <div>
            <h1>Dashboard</h1>
        </div>

    )

}