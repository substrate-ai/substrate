import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';


type Props = {
    termsLocation: string
}


export function LegalPage({termsLocation} : Props) {

  const [terms, setTerms] = useState<string | null>(null);

  useEffect(() => {
    const fetchTerms = async () => {
      try {
        const response = await fetch(termsLocation);
        if (!response.ok) {
          throw new Error('Failed to fetch terms');
        }
        const termsText = await response.text();
        setTerms(termsText);
      } catch (error) {
        console.error(error);
      }
    };
  
    fetchTerms();
  }, [termsLocation]);
  
  return (
    <div className="flex h-screen bg-[#0d1117] overflow-scroll">
    <div className="m-auto w-10/12 lg:w-1/2 py-20 prose-invert prose lg:prose-xl">
    <article className="markdown-body">
      {terms && <ReactMarkdown children={terms} />}
    </article>
    </div>
    </div>
  );
}

