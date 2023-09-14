import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';


type Props = {
    termsLocation: string
}


export default function LegalPage({termsLocation} : Props) {

    async function fetchTerms() {
        const response = await fetch(termsLocation);
        const text = await response.text();
        return text;
      }

  const [terms, setTerms] = useState<string | null>(null);

  useEffect(() => {
    async function loadTerms() {
      const termsText = await fetchTerms();
      setTerms(termsText);
    }

    loadTerms();
  }, []);

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

