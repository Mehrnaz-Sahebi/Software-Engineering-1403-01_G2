import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { SuggestionsProvider } from './contexts/SuggestionsContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SuggestionsProvider>
      <App />
    </SuggestionsProvider>
  </StrictMode>,
)
