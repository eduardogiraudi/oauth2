// Hook per usare il contesto
import { useContext } from "react";
import { GlobalStateContext } from "@root/GlobalContext";
const useGlobalContext = () => {
    return useContext(GlobalStateContext);
};

export {useGlobalContext}