import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import UploadPage from './pages/UploadPage';
import ResultsPage from './pages/ResultsPage';
import DirectAnalysisPage from './pages/DirectAnalysisPage';
import SignInPage from './pages/SignInPage';
import SignUpPage from './pages/SignUpPage';
import UserProfilePage from './pages/UserProfilePage';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/sign-in" element={<SignInPage />} />
        <Route path="/sign-up" element={<SignUpPage />} />

        {/* Protected routes - require authentication */}
        <Route
          path="/upload"
          element={
            <ProtectedRoute>
              <UploadPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/results/:jobId"
          element={
            <ProtectedRoute>
              <ResultsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/direct-analysis"
          element={
            <ProtectedRoute>
              <DirectAnalysisPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <UserProfilePage />
            </ProtectedRoute>
          }
        />

        {/* Legacy routes - redirect to new paths */}
        <Route path="/app/upload" element={<ProtectedRoute><UploadPage /></ProtectedRoute>} />
        <Route path="/app/results/:jobId" element={<ProtectedRoute><ResultsPage /></ProtectedRoute>} />
        <Route path="/app/direct-analysis" element={<ProtectedRoute><DirectAnalysisPage /></ProtectedRoute>} />
      </Routes>
    </Router>
  );
}

export default App;
