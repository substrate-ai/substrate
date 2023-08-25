import { supabaseClient } from "src/config/supabase-client";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "src/hooks/Auth";
import axios from "axios";


export type GetTokenDTO = {
    token_name: string
}

export function useGetTokensQuery() {
    return useQuery(['tokens'], async () => {

        console.log(supabaseClient.auth.getSession())
        // todo fix RLS and this should work
        const {data, error} = await supabaseClient.from("token").select()

        if (error) {
            console.error("error getting tokens", error)
            throw new Error(error.message)
        }

        if (!data) {
            throw new Error("no data")
        } else {
            console.log("data", data)
        }

        return data
    }
    
    
    );
  }

export type CreateTokenDTO = {
    tokenName: string
}



export function usePostTokenQuery() {
    return useMutation(['tokens'], async (token: CreateTokenDTO) => {
        const session = useAuth()

        if (token.tokenName === "") {
            throw new Error("token name cannot be empty")
        }
        // do post request to supabase function via axios
        const response = await axios.post<CreateTokenDTO>(import.meta.env.VITE_SUPABASE_URL + "/token/token", {
            token_name: token.tokenName
        }, {
            headers: {
                Authorization: "Bearer " + session.session!.access_token
            }
        })

        if (response.status !== 200) {
            console.log("response", response)
            throw new Error("error creating token")
        }

        return response.data
    });
}


export function useDeleteToken() {

    const queryClient = useQueryClient()

    return useMutation(['tokens'], async (id: string) => {
        console.log(supabaseClient.auth.getSession())
        // todo fix RLS and this should work
        const {data, error} = await supabaseClient.from("token").delete().eq("id", id)

        if (error) {
            console.error("error getting tokens", error)
            throw new Error(error.message)
        }

        return data
    }, { onSuccess: (_data,variables) => {

       // filter out the deleted token
         queryClient.setQueryData(['tokens'], (oldData: any) => {
            return oldData.filter((token: any) => token.id !== variables)
        })

    }}
    
    
    );
}



// export async function getTokens(): Promise<GetTokenDTO[]> {
//     const {data, error} = await supabaseClient.from("token").select("token_name")
    
//     if (error) {
//         console.error("error getting tokens", error)
//         throw new Error(error.message)
//     }

//     if (!data) {
//         throw new Error("no data")
//     }

//     return data
// }


// export async function deleteToken(tokenName: string): Promise<boolean> {
//     const {data, error} = await supabaseClient.from("token").delete().eq("token_name", tokenName)
    
//     if (error) {
//         console.error("error getting tokens", error)
//         throw new Error(error.message)
//     }

//     if (!data) {
//         throw new Error("no data")
//     }

//     return data
// }

// const session = useAuth()

type typeCreateTokenResponse = {
    accessToken: string
}

export async function createToken(token_name: string): Promise<typeCreateTokenResponse> {
    const access_token = (await supabaseClient.auth.getSession()).data.session?.access_token
    // do post request to supabase function via axios
    const response = await axios.post(import.meta.env.VITE_SUPABASE_URL + "/functions/v1/token/token", {
        tokenName: token_name
    }, {
        headers: {
            Authorization: "Bearer " + access_token
        }
    })

    if (response.status !== 200) {
        throw new Error("error creating token")
    }

    const data = response.data

    return data

}