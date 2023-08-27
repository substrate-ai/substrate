import terms from "src/assets/markdowns/privacy.md";
import LegalPage from "./Legal";

export default function PrivacyPage() {
    return (
        <LegalPage termsLocation={terms}/>
    )
}