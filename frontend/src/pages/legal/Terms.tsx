import terms from "src/assets/markdowns/terms.md";
import {LegalPage} from "./components/Legal";

export default function TermsPage() {
    return (
        <LegalPage termsLocation={terms}/>
    )
}