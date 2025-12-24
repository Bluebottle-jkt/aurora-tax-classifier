import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import UploadPage from './pages/UploadPage';
import ResultsPage from './pages/ResultsPage';
import DirectAnalysisPage from './pages/DirectAnalysisPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/app/upload" element={<UploadPage />} />
        <Route path="/app/results/:jobId" element={<ResultsPage />} />
        <Route path="/app/direct-analysis" element={<DirectAnalysisPage />} />
      </Routes>
    </Router>
  );
}

export default App;
