import {createClient} from '@sanity/client'

export const sanityClient = createClient({
    projectId: 'wnz3vj3x',
    dataset: 'production',
    useCdn: true, // set to `false` to bypass the edge cache
    apiVersion: '2023-09-10', // use current date (YYYY-MM-DD) to target the latest API version
  // token: process.env.SANITY_SECRET_TOKEN // Only if you want to update content with the client
})

export async function getPosts() {
  const posts = await sanityClient.fetch('*[_type == "post"]')
  return posts
}


