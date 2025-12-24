import { UserProfile } from '@clerk/clerk-react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'

export default function UserProfilePage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/upload')}
            className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Dashboard
          </button>

          <div className="text-center">
            <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 mb-2">
              AURORA
            </h1>
            <p className="text-gray-300 text-sm">
              Manage Your Profile
            </p>
          </div>
        </div>

        {/* User Profile Component */}
        <div className="flex justify-center">
          <UserProfile
            appearance={{
              elements: {
                rootBox: "w-full max-w-4xl",
                card: "bg-slate-800 shadow-2xl",
                navbar: "bg-slate-900",
                navbarButton: "text-gray-300 hover:bg-slate-800",
                navbarButtonActive: "text-white bg-slate-800",
                headerTitle: "text-white",
                headerSubtitle: "text-gray-400",
                formButtonPrimary: "bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700",
                formFieldInput: "bg-slate-700 border-slate-600 text-white",
                formFieldLabel: "text-gray-300",
                profileSectionTitle: "text-white",
                profileSectionContent: "text-gray-300",
                accordionTriggerButton: "hover:bg-slate-700",
                badge: "bg-blue-500",
              }
            }}
          />
        </div>
      </div>
    </div>
  )
}
