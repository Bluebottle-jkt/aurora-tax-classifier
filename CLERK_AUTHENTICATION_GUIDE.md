# Clerk Authentication Guide - AURORA Tax Classifier

Complete guide to setting up and using Clerk authentication in the AURORA Tax Classifier application.

**Created**: December 24, 2025
**Status**: Authentication System Implemented
**Framework**: Clerk + React

---

## Table of Contents

1. [Overview](#overview)
2. [What Was Implemented](#what-was-implemented)
3. [Getting Started](#getting-started)
4. [Configuration](#configuration)
5. [User Flows](#user-flows)
6. [Protected Routes](#protected-routes)
7. [Customization](#customization)
8. [Backend Integration](#backend-integration)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

---

## Overview

Clerk provides complete user authentication for AURORA Tax Classifier including:

✅ **User Registration** - Email, social providers
✅ **Sign In** - Secure authentication
✅ **Profile Management** - User settings, password changes
✅ **Session Management** - Automatic token refresh
✅ **Protected Routes** - Access control
✅ **Beautiful UI** - Customized to match AURORA branding

---

## What Was Implemented

### Files Created

| File | Purpose |
|------|---------|
| `frontend/src/pages/SignInPage.tsx` | Sign in page with Clerk component |
| `frontend/src/pages/SignUpPage.tsx` | Sign up page with Clerk component |
| `frontend/src/pages/UserProfilePage.tsx` | User profile management page |
| `frontend/src/components/ProtectedRoute.tsx` | Route protection component |

### Files Modified

| File | Changes |
|------|---------|
| `frontend/src/main.tsx` | Added ClerkProvider wrapper |
| `frontend/src/App.tsx` | Added auth routes and protected routes |
| `frontend/src/pages/LandingPage.tsx` | Updated CTA button to sign-up |
| `.env.example` | Added Clerk configuration variables |

### Routes Configured

**Public Routes:**
- `/` - Landing page
- `/sign-in` - Sign in page
- `/sign-up` - Sign up page

**Protected Routes** (require authentication):
- `/upload` - File upload page
- `/direct-analysis` - Direct text analysis
- `/results/:jobId` - Results view
- `/profile` - User profile management

**Legacy Routes** (redirected):
- `/app/upload` → `/upload`
- `/app/direct-analysis` → `/direct-analysis`
- `/app/results/:jobId` → `/results/:jobId`

---

## Getting Started

### Step 1: Create Clerk Account

1. Go to https://clerk.com/
2. Sign up for a free account
3. Create a new application
4. Name it "AURORA Tax Classifier"

### Step 2: Get API Keys

In your Clerk dashboard:

1. Go to **API Keys** section
2. Copy the **Publishable Key** (starts with `pk_test_`)
3. Copy the **Secret Key** (starts with `sk_test_`)

### Step 3: Configure Environment Variables

Create or update your `.env` file in the project root:

```bash
# Frontend - Vite requires VITE_ prefix
VITE_CLERK_PUBLISHABLE_KEY=pk_test_your_actual_key_here

# Backend - For API verification (optional)
CLERK_SECRET_KEY=sk_test_your_actual_secret_key_here
```

**Important Notes:**
- Frontend variables MUST start with `VITE_` for Vite to expose them
- Never commit actual keys to Git (`.env` is in `.gitignore`)
- Use different keys for development and production

### Step 4: Configure Clerk Dashboard

In Clerk dashboard, configure:

**1. Sign-In Settings:**
- Navigate to: **User & Authentication** > **Email, Phone, Username**
- Enable: Email addresses
- Optional: Add social providers (Google, GitHub, etc.)

**2. URLs:**
- Navigate to: **Settings** > **Paths**
- Sign-in URL: `/sign-in`
- Sign-up URL: `/sign-up`
- After sign-in URL: `/upload`
- After sign-up URL: `/upload`

**3. Session Settings:**
- Navigate to: **Settings** > **Sessions**
- Recommended: 7 days session lifetime
- Enable: Multi-session support (optional)

### Step 5: Test the Integration

1. Start the development server:
   ```bash
   cd frontend
   npm run dev
   ```

2. Visit http://localhost:3000

3. Click "Get Started" → redirects to sign-up

4. Create test account

5. Should redirect to `/upload` after successful sign-up

---

## Configuration

### Clerk Provider Setup

The `ClerkProvider` wraps the entire application in [main.tsx](frontend/src/main.tsx:1):

```typescript
import { ClerkProvider } from '@clerk/clerk-react'

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <App />
    </ClerkProvider>
  </React.StrictMode>,
)
```

### Custom Appearance

All Clerk components use custom styling to match AURORA branding:

```typescript
appearance={{
  elements: {
    card: "bg-slate-800 shadow-2xl",
    headerTitle: "text-white",
    formButtonPrimary: "bg-gradient-to-r from-blue-500 to-purple-600",
    formFieldInput: "bg-slate-700 border-slate-600 text-white",
    // ... more customizations
  }
}}
```

**Colors Used:**
- Background: Slate 800 (`bg-slate-800`)
- Primary gradient: Blue 500 → Purple 600
- Text: White with gray secondary
- Borders: Slate 600

---

## User Flows

### Sign Up Flow

1. User clicks "Get Started" on landing page
2. Redirects to `/sign-up`
3. User enters email and password
4. Clerk sends verification email
5. User verifies email
6. Redirects to `/upload` (protected route)

### Sign In Flow

1. User navigates to `/sign-in` or clicks sign-in link
2. Enters credentials
3. Clerk validates and creates session
4. Redirects to `/upload`

### Profile Management

1. User navigates to `/profile`
2. Can update:
   - Name
   - Email
   - Password
   - Profile photo
   - Security settings

### Sign Out

User can sign out from:
- User button (top right of protected pages)
- Profile page
- Clerk automatically clears session

---

## Protected Routes

### How It Works

The `ProtectedRoute` component ([ProtectedRoute.tsx](frontend/src/components/ProtectedRoute.tsx:1)):

```typescript
export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isLoaded, isSignedIn } = useAuth()

  // Wait for Clerk to load
  if (!isLoaded) {
    return <LoadingSpinner />
  }

  // Redirect if not signed in
  if (!isSignedIn) {
    return <Navigate to="/sign-in" replace />
  }

  // Render protected content
  return <>{children}</>
}
```

### Usage in Routes

```typescript
<Route
  path="/upload"
  element={
    <ProtectedRoute>
      <UploadPage />
    </ProtectedRoute>
  }
/>
```

### Adding New Protected Routes

To protect a new route:

```typescript
import ProtectedRoute from './components/ProtectedRoute'

<Route
  path="/new-protected-page"
  element={
    <ProtectedRoute>
      <YourNewPage />
    </ProtectedRoute>
  }
/>
```

---

## Customization

### Changing Theme Colors

Edit the `appearance` prop in Sign In/Sign Up pages:

```typescript
appearance={{
  elements: {
    formButtonPrimary: "bg-gradient-to-r from-YOUR-COLOR to-YOUR-COLOR",
    // ... other elements
  }
}}
```

### Adding Social Providers

1. **In Clerk Dashboard:**
   - Go to **User & Authentication** > **Social Connections**
   - Enable providers (Google, GitHub, Microsoft, etc.)
   - Configure OAuth credentials

2. **No Code Changes Needed:**
   - Clerk automatically shows enabled providers
   - Buttons appear in sign-in/sign-up forms

### Custom Sign Up Fields

1. **In Clerk Dashboard:**
   - Go to **User & Authentication** > **Email, Phone, Username**
   - Add custom fields (e.g., company name, job title)

2. **In Code:**
   - Access via `user.unsafeMetadata` or `user.publicMetadata`

```typescript
import { useUser } from '@clerk/clerk-react'

const { user } = useUser()
console.log(user?.publicMetadata.companyName)
```

---

## Backend Integration

### Verifying User Tokens

Install Clerk SDK for backend:

```bash
cd backend
pip install clerk-sdk-python
```

### Protect API Endpoints

```python
from clerk_sdk import Clerk

clerk = Clerk(api_key=os.getenv("CLERK_SECRET_KEY"))

@app.get("/api/protected-endpoint")
async def protected_endpoint(
    authorization: str = Header(None)
):
    # Extract token
    token = authorization.replace("Bearer ", "")

    # Verify with Clerk
    try:
        session = clerk.sessions.verify_session(token)
        user_id = session.user_id

        # Proceed with authenticated request
        return {"message": "Authenticated", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
```

### Getting User Information

```python
# Get user details
user = clerk.users.get(user_id)

print(user.email_addresses[0].email_address)
print(user.first_name, user.last_name)
```

### Webhooks (Optional)

Set up webhooks to sync user events:

1. **In Clerk Dashboard:**
   - Go to **Webhooks** > **Add Endpoint**
   - URL: `https://your-backend.com/api/webhooks/clerk`
   - Events: `user.created`, `user.updated`, `user.deleted`

2. **In Backend:**
   ```python
   @app.post("/api/webhooks/clerk")
   async def clerk_webhook(request: Request):
       payload = await request.json()
       event_type = payload["type"]

       if event_type == "user.created":
           # Create user in your database
           pass
       elif event_type == "user.updated":
           # Update user in your database
           pass
   ```

---

## Testing

### Manual Testing Checklist

- [ ] Sign up with new email works
- [ ] Email verification works
- [ ] Sign in with correct credentials works
- [ ] Sign in with wrong credentials fails
- [ ] Protected routes redirect to sign-in when not authenticated
- [ ] Protected routes accessible when authenticated
- [ ] Sign out clears session
- [ ] Profile page loads user information
- [ ] Password change works
- [ ] Session persists across browser refresh

### Automated Testing

Using React Testing Library:

```typescript
import { render, screen } from '@testing-library/react'
import { ClerkProvider } from '@clerk/clerk-react'
import SignInPage from './SignInPage'

test('renders sign in page', () => {
  render(
    <ClerkProvider publishableKey="pk_test_xxx">
      <SignInPage />
    </ClerkProvider>
  )

  expect(screen.getByText('AURORA')).toBeInTheDocument()
})
```

### Test Accounts

Create test accounts in Clerk dashboard:
- **User & Authentication** > **Users** > **Create User**
- Email: `test@example.com`
- Password: Set test password
- Use for development testing

---

## Troubleshooting

### Issue: "Missing Clerk Publishable Key"

**Symptom:** Error on startup: `Missing Clerk Publishable Key`

**Solution:**
1. Check `.env` file exists
2. Verify `VITE_CLERK_PUBLISHABLE_KEY` is set
3. Restart dev server (`npm run dev`)
4. Clear browser cache

### Issue: Infinite Redirect Loop

**Symptom:** Page keeps redirecting between `/sign-in` and protected route

**Solution:**
1. Check ClerkProvider is wrapping App component
2. Verify publishable key is correct
3. Check browser cookies are enabled
4. Clear browser storage and cookies

### Issue: Session Not Persisting

**Symptom:** User gets logged out on page refresh

**Solution:**
1. Check Clerk dashboard session settings
2. Verify cookies are not being blocked
3. Check browser is not in incognito mode
4. Ensure HTTPS in production

### Issue: Styling Not Applied

**Symptom:** Clerk components look different than expected

**Solution:**
1. Verify Tailwind CSS is loaded
2. Check `appearance` prop is correctly structured
3. Ensure CSS classes are not being purged by Tailwind
4. Add Clerk classes to Tailwind safelist if needed

### Issue: Can't Access Protected Routes

**Symptom:** Always redirected to sign-in even when signed in

**Solution:**
1. Check `useAuth()` hook is working: `console.log(isSignedIn)`
2. Verify ClerkProvider is properly configured
3. Check browser console for Clerk errors
4. Try signing out and signing in again

### Issue: Backend Can't Verify Tokens

**Symptom:** API returns 401 even with valid session

**Solution:**
1. Verify `CLERK_SECRET_KEY` in backend `.env`
2. Check token is being sent in Authorization header
3. Ensure backend Clerk SDK is installed
4. Verify API key matches Clerk dashboard

---

## Advanced Features

### Multi-Tenancy

Separate users by organization:

```typescript
import { useOrganization } from '@clerk/clerk-react'

const { organization } = useOrganization()
```

### Custom Metadata

Store additional user data:

```typescript
import { useUser } from '@clerk/clerk-react'

const { user } = useUser()

// Update metadata
await user.update({
  publicMetadata: {
    role: 'admin',
    department: 'Finance'
  }
})
```

### Session Tokens

Get JWT for API calls:

```typescript
import { useAuth } from '@clerk/clerk-react'

const { getToken } = useAuth()

const token = await getToken()
// Use in API Authorization header
```

---

## Production Checklist

Before deploying to production:

- [ ] Use production Clerk keys (starts with `pk_live_` and `sk_live_`)
- [ ] Update environment variables on hosting platform
- [ ] Configure production URLs in Clerk dashboard
- [ ] Enable HTTPS
- [ ] Set up custom domain for Clerk (optional)
- [ ] Configure email templates in Clerk dashboard
- [ ] Set up webhooks for user sync
- [ ] Test all authentication flows in production
- [ ] Set up monitoring for auth errors
- [ ] Configure CORS properly for API calls

---

## Resources

**Clerk Documentation:**
- Main Docs: https://clerk.com/docs
- React Guide: https://clerk.com/docs/quickstarts/react
- API Reference: https://clerk.com/docs/reference/backend-api

**AURORA Project Documentation:**
- [README.md](README.md) - Project overview
- [SETUP_COMPLETE.md](SETUP_COMPLETE.md) - Setup guide
- [PROJECT_EXPANSION_STATUS.md](PROJECT_EXPANSION_STATUS.md) - Current status

**Support:**
- Clerk Support: https://clerk.com/support
- Clerk Discord: https://clerk.com/discord
- Project Issues: Create issue in GitHub repository

---

## Summary

Clerk authentication is now fully integrated into AURORA Tax Classifier with:

✅ User registration and sign-in
✅ Protected application routes
✅ Profile management
✅ Session handling
✅ Custom AURORA branding
✅ Production-ready configuration

**Next Steps:**
1. Get Clerk API keys from dashboard
2. Add to `.env` file
3. Test authentication flows
4. Customize as needed
5. Deploy to production

---

**Created**: December 24, 2025
**Status**: Complete and Ready to Use
**Version**: 1.0

Happy authenticating! 🔐
