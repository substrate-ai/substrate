import terms from "src/assets/markdowns/privacy.md";
import {LegalPage} from "./components/Legal";

export default function PrivacyPage() {
    return (
        <LegalPage termsLocation={terms}/>
    )
}