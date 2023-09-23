import {createClient} from '@sanity/client'

export const sanityClient = createClient({
    projectId: 'wnz3vj3x',
    dataset: 'production',
    useCdn: true,
    apiVersion: '2023-05-03', 
})


