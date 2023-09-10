import {createClient} from '@sanity/client'

export const sanityClient = createClient({
    projectId: 'wnz3vj3x',
    dataset: 'production',
    useCdn: true,
    apiVersion: '2023-05-03', 
})

export async function getPosts() {
  const posts = await sanityClient.fetch('*[_type == "post"]')
  console.log(posts)
  return posts
}


