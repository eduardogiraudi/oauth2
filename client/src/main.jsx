// import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from '@root/App.jsx'
import { GlobalStateProvider } from '@root/GlobalContext.jsx'


createRoot(document.getElementById('root')).render(
  <GlobalStateProvider>
    <App />
  </GlobalStateProvider>

)
