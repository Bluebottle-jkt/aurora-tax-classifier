import React from 'react'
import ReactDOM from 'react-dom/client'
import { ClerkProvider } from '@clerk/clerk-react'
import App from './App.tsx'
import './index.css'

// Get Clerk publishable key from environment variables
const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!PUBLISHABLE_KEY) {
  // Show error in DOM instead of throwing
  const root = document.getElementById('root')
  if (root) {
    root.innerHTML = `
      <div style="padding: 40px; font-family: system-ui; max-width: 800px; margin: 0 auto;">
        <h1 style="color: #dc2626;">⚠️ Configuration Error</h1>
        <p>Missing Clerk Publishable Key.</p>
        <p>Please add <code>VITE_CLERK_PUBLISHABLE_KEY</code> to your <code>.env</code> file.</p>
        <p style="margin-top: 20px; padding: 12px; background: #fef2f2; border-left: 4px solid #dc2626;">
          <strong>Steps to fix:</strong><br/>
          1. Go to https://dashboard.clerk.com<br/>
          2. Copy your Publishable Key (pk_test_...)<br/>
          3. Add it to .env file<br/>
          4. Restart the dev server
        </p>
      </div>
    `
  }
  throw new Error('Missing Clerk Publishable Key')
}

try {
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
      <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
        <App />
      </ClerkProvider>
    </React.StrictMode>,
  )
} catch (error) {
  console.error('Failed to render app:', error)
  const root = document.getElementById('root')
  if (root) {
    root.innerHTML = `
      <div style="padding: 40px; font-family: system-ui; max-width: 800px; margin: 0 auto;">
        <h1 style="color: #dc2626;">⚠️ Application Error</h1>
        <p>Failed to initialize application.</p>
        <pre style="padding: 12px; background: #f3f4f6; overflow: auto;">${error}</pre>
        <p style="margin-top: 20px;">Check the browser console for more details.</p>
      </div>
    `
  }
}
