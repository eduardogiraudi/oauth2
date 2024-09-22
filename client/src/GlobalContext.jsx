import  { createContext, useState } from 'react';


const GlobalStateContext = createContext();

const GlobalStateProvider = ({ children }) => {
    return (
        <GlobalStateContext.Provider value={{  }}>
            {children}
        </GlobalStateContext.Provider>
    );
};
export {GlobalStateContext, GlobalStateProvider}
