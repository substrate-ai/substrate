import { get } from "http";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {getPosts, sanityClient} from "src/config/sanity-client"
import dayjs from "dayjs";
import LocalizedFormat from 'dayjs/plugin/localizedFormat'
import { redirect } from "react-router-dom";



dayjs.extend(LocalizedFormat)


export default function Blog() {
  const [allPostsData, setAllPosts] = useState<any | null>(null);

  useEffect(() => {
    async function retrievePosts() {

        const posts = await getPosts();
        console.log(posts);
        setAllPosts(posts);
    }
    retrievePosts();
  }, []);

  const redirectToSlug = (page:string) => {
    redirect(page)
  };

  return (
    <section className="text-gray-600 body-font">
        <div className="container px-5 py-24 mx-auto">
          <div className="flex flex-wrap -m-4">
          {allPostsData &&
            allPostsData.map((post: any, index : number) => (
                <div className="p-4 md:w-1/3" key={index}>
                <div className="h-full rounded-xl shadow-cla-blue bg-gradient-to-r from-gray-700 to-slate-900 overflow-hidden">
                  <img className="lg:h-48 md:h-36 w-full object-cover object-center scale-110 transition-all duration-400 hover:scale-100" src="https://images.unsplash.com/photo-1618172193622-ae2d025f4032?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1064&q=80" alt="blog"/>
                  <div className="p-6">
                    <h2 className="tracking-widest text-xs title-font font-medium text-gray-200 mb-1">{dayjs(post._date).format('LL')}</h2>
                    <h1 className="title-font text-lg font-medium text-gray-100 mb-3">{post.title}</h1>
                    <p className="leading-relaxed mb-3">
                        Description
                    </p>
                    <div className="flex items-center flex-wrap ">
                      <button className="bg-gradient-to-r from-cyan-400 to-blue-400 hover:scale-105 drop-shadow-md  shadow-cla-blue px-4 py-1 rounded-lg">Learn more</button>
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