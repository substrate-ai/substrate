import { supabaseClient } from "src/config/supabase-client";
import axios from "axios";
import { useAuth } from "src/hooks/Auth";


type GetTokenDTO = {
    token_name: string
}



async function getTokens(): Promise<GetTokenDTO[]> {
    const {data, error} = await supabaseClient.from("token").select("token_name")
    
    if (error) {
        console.error("error getting tokens", error)
        throw new Error(error.message)
    }

    if (!data) {
        throw new Error("no data")
    }

    return data
}


async function deleteToken(tokenName: string): Promise<boolean> {
    const {data, error} = await supabaseClient.from("token").delete().eq("token_name", tokenName)
    
    if (error) {
        console.error("error getting tokens", error)
        throw new Error(error.message)
    }

    if (!data) {
        throw new Error("no data")
    }

    return data
}

type CreateTokenDTO = {
    access_token: string
}

async function createToken(token_name: string): Promise<CreateTokenDTO> {

    const session = useAuth()
    // do post request to supabase function via axios
    const response = await axios.post(import.meta.env.VITE_SUPABASE_URL + "/token/token", {
        token_name: token_name
    }, {
        headers: {
            Authorization: "Bearer " + session.session!.access_token
        }
    })

    if (response.status !== 200) {
        throw new Error("error creating token")
    }

    const data = response.data

    return data

}