import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { sanityClient } from "../config/sanity-client";
import { PortableText } from '@portabletext/react'
import imageUrlBuilder from "@sanity/image-url";
import { SanityImageSource } from "@sanity/image-url/lib/types/types";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dark } from 'react-syntax-highlighter/dist/esm/styles/prism';


const serializers = {
  types: {
    code: ({value}: any) => { // eslint-disable-line @typescript-eslint/no-explicit-any
      // console.log(value)
      return (
        // <div className="not-prose">
          <SyntaxHighlighter 
              useInlineStyles={false} 
              language={value.language}
              style={dark}
              showLineNumbers
              >
              {/* style={vs} */}
              {/* showLineNumbers */}
              
            {value.code}
          </SyntaxHighlighter>
        // </div>
      )
    },
    image: ({value} : any) => <img src={urlFor(value.asset).url()} />, // eslint-disable-line @typescript-eslint/no-explicit-any
  },
}

const builder = imageUrlBuilder(sanityClient);
function urlFor(source: SanityImageSource) {
  return builder.image(source);
}

export default function OnePost() {
  const [postData, setPostData] = useState<any | null>(null); // eslint-disable-line @typescript-eslint/no-explicit-any
  const { slug } = useParams();

  useEffect(() => {
    sanityClient
      .fetch(
        `*[slug.current == "${slug}"]{
           title,
           slug,
           mainImage{
           asset->{
              _id,
              url
            }
          },
          body,
          "authorName": author->name,
          "authorImage": author->image,
          "authorTitle": author->title,
       }`
      )
      .then((data) => setPostData(data[0]))
      .catch(console.error);
  }, [slug]);

  console.log(postData)

  if (!postData) return <div>Loading...</div>;

  return (
<div className="mb-4 md:mb-0 w-full mx-auto relative flex flex-col items-center">
  <div className="px-10 lg:px-4">
    <h2 className="text-4xl font-semibold text-white leading-tight pt-10">
      {postData.title}
    </h2>
    <img
      // make it centered and not cropped
      className="w-full object-contain lg:rounded-t-lg"
      src={urlFor(postData.mainImage).url()}
      alt="Post image"
      style={{ height: "400px" }}
    />
  </div>

  <div className="px-16 lg:px-48 py-12 lg:py-20 prose-invert prose lg:prose-xl max-w-full">
    <PortableText
      value={postData.body}
      components={serializers}
    />
  </div>

  <div className="flex px-10 lg:px-4 mb-5">
    <img
      src={urlFor(postData.authorImage).url()}
      className="h-10 w-10 rounded-full mr-2 object-cover"
      alt="Author"
    />
    <div>
      <p className="font-semibold text-gray-200 text-sm"> {postData.authorName} </p>
      <p className="font-semibold text-gray-400 text-xs"> {postData.authorTitle} </p>
    </div>
  </div>
</div>






  );
}