import terms from "src/assets/markdowns/terms.md";
import LegalPage from "./Legal";

export default function PrivacyPage() {
    return (
        <LegalPage termsLocation={terms}/>
    )
}