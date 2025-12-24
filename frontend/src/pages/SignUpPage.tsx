import { SignUp } from '@clerk/clerk-react'

export default function SignUpPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="w-full max-w-md p-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 mb-2">
            AURORA
          </h1>
          <p className="text-gray-300 text-sm">
            Audit Object Recognition & Analytics
          </p>
        </div>

        <SignUp
          appearance={{
            elements: {
              rootBox: "w-full",
              card: "bg-slate-800 shadow-2xl",
              headerTitle: "text-white",
              headerSubtitle: "text-gray-400",
              socialButtonsBlockButton: "bg-slate-700 hover:bg-slate-600 text-white border-slate-600",
              formButtonPrimary: "bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700",
              formFieldInput: "bg-slate-700 border-slate-600 text-white",
              formFieldLabel: "text-gray-300",
              footerActionLink: "text-blue-400 hover:text-blue-300",
              identityPreviewText: "text-white",
              identityPreviewEditButton: "text-blue-400",
            }
          }}
          redirectUrl="/upload"
          signInUrl="/sign-in"
        />
      </div>
    </div>
  )
}
