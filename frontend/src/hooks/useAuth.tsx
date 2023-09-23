import { useContext } from "react";
import { AuthContext } from "../contexts/UserAuthContext";

export const useAuth = () => {
    return useContext(AuthContext);
};