import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {sanityClient} from "src/clients/sanityClient"
import dayjs from "dayjs";
import LocalizedFormat from 'dayjs/plugin/localizedFormat'

dayjs.extend(LocalizedFormat)

export function Blog() {

  const [allPostsData, setAllPosts] = useState<any | null>(null); // eslint-disable-line @typescript-eslint/no-explicit-any

  useEffect(() => {
    sanityClient
    .fetch(
      `*[_type == "post"]{
        title,
        slug,
        mainImage{
        asset->{
          _id,
          url
        }
      },
    }`
    )
    .then((data) => setAllPosts(data))
    .catch(console.error);
  }, []);
  
  return (
    <section className="text-gray-600 body-font">
        <div className="container px-5 py-24 mx-auto">
          <div className="flex flex-wrap -m-4">
          {allPostsData &&
            allPostsData.map((post: any, index : number) => ( // eslint-disable-line @typescript-eslint/no-explicit-any
                <div className="p-4 md:w-1/3" key={index}>
                <div className="h-full rounded-xl shadow-cla-blue bg-gradient-to-r from-gray-700 to-slate-900 overflow-hidden">
                  <img className="lg:h-48 md:h-36 w-full object-cover object-center scale-110 transition-all duration-400 hover:scale-100" src={post.mainImage.asset.url} alt="blog"/>
                  <div className="p-6">
                    <h2 className="tracking-widest text-xs title-font font-medium text-gray-200 mb-1">{dayjs(post._date).format('LL')}</h2>
                    <h1 className="title-font text-lg font-medium text-gray-100 mb-3">{post.title}</h1>
                    <div className="flex items-center flex-wrap ">
                      <Link to={"/post/" + post.slug.current} className="bg-slate-800 hsover:scale-105 drop-shadow-md  shadow-cla-black px-4 py-1 rounded-lg text-slate-50">Read</Link>
                    </div>
                  </div>
                </div>
              </div>
            ))}            
          </div>
        </div>
      </section>
  );
}