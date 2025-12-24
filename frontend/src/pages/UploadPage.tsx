import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

export default function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [businessType, setBusinessType] = useState('');
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState<string[]>([]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  }, []);

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile);

    // Read first few lines for preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target?.result as string;
      const lines = text.split('\n').slice(0, 5);
      setPreview(lines);
    };
    reader.readAsText(selectedFile.slice(0, 2000));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !businessType) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('business_type', businessType);

    try {
      const response = await axios.post('/api/jobs', formData, {
        headers: {
          'X-Aurora-Key': 'aurora-dev-key-change-in-production',
        },
      });

      navigate(`/app/results/${response.data.job_id}`);
    } catch (error) {
      alert('Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Header with Gradient */}
      <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white py-8 shadow-lg">
        <div className="container mx-auto px-4">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl font-bold text-center mb-2"
            style={{
              background: 'linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text'
            }}
          >
            🔍 Aurora
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-center text-indigo-100 text-lg"
          >
            Audit Object Recognition Analytics - Advanced AI Tax Classifier
          </motion.p>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">

          {/* Tab-like Header */}
          <div className="flex gap-4 mb-8">
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="flex-1 bg-white rounded-lg shadow-lg p-6 border-l-4 border-indigo-600"
            >
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center text-2xl">
                  📁
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-800">Batch File Upload</h2>
                  <p className="text-sm text-gray-500">Process entire GL files instantly</p>
                </div>
              </div>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.02 }}
              onClick={() => navigate('/app/direct-analysis')}
              className="flex-1 bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-400 cursor-pointer hover:shadow-xl transition-shadow"
            >
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center text-2xl">
                  ✍️
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-800">Direct Text Analysis</h2>
                  <p className="text-sm text-gray-500">Analyze transactions instantly</p>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Upload Form */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-2xl shadow-2xl overflow-hidden"
          >
            <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6">
              <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                📤 Upload General Ledger Data
              </h2>
              <p className="text-indigo-100 mt-1">Upload CSV or Excel files for comprehensive tax object analysis</p>
            </div>

            <form onSubmit={handleSubmit} className="p-8">

              {/* Drag and Drop Zone */}
              <div className="mb-8">
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  Upload File (CSV or Excel)
                </label>
                <div
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                  className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all ${
                    dragActive
                      ? 'border-indigo-500 bg-indigo-50 scale-105'
                      : 'border-gray-300 bg-gray-50 hover:border-indigo-400 hover:bg-indigo-25'
                  }`}
                >
                  <input
                    type="file"
                    accept=".csv,.xlsx,.xls"
                    onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />

                  <div className="pointer-events-none">
                    {!file ? (
                      <>
                        <div className="text-6xl mb-4">📂</div>
                        <p className="text-lg font-semibold text-gray-700 mb-2">
                          Drag & drop your file here
                        </p>
                        <p className="text-sm text-gray-500 mb-4">or click to browse</p>
                        <div className="inline-block px-6 py-2 bg-indigo-100 text-indigo-700 rounded-lg font-medium">
                          Choose File
                        </div>
                      </>
                    ) : (
                      <div className="flex items-center justify-center gap-3">
                        <div className="text-5xl">✅</div>
                        <div className="text-left">
                          <p className="font-bold text-gray-800 text-lg">{file.name}</p>
                          <p className="text-sm text-gray-500">
                            {(file.size / 1024).toFixed(2)} KB
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* File Preview */}
              <AnimatePresence>
                {preview.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="mb-6 bg-gray-50 rounded-lg p-4 border border-gray-200"
                  >
                    <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                      👁️ File Preview (First 5 lines)
                    </h3>
                    <pre className="text-xs text-gray-600 overflow-x-auto">
                      {preview.join('\n')}
                    </pre>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Business Type Selection */}
              <div className="mb-8">
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  Business Type / Industry Classification
                </label>
                <div className="grid grid-cols-3 gap-4">
                  {[
                    { value: 'Manufaktur', icon: '🏭', label: 'Manufacturing', desc: 'Production & Assembly' },
                    { value: 'Perdagangan', icon: '🏪', label: 'Trading', desc: 'Buy & Sell Goods' },
                    { value: 'Jasa', icon: '💼', label: 'Services', desc: 'Professional Services' }
                  ].map((type) => (
                    <motion.div
                      key={type.value}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => setBusinessType(type.value)}
                      className={`cursor-pointer rounded-xl p-6 border-2 transition-all ${
                        businessType === type.value
                          ? 'border-indigo-600 bg-indigo-50 shadow-lg'
                          : 'border-gray-200 bg-white hover:border-indigo-300 hover:shadow-md'
                      }`}
                    >
                      <div className="text-4xl mb-3 text-center">{type.icon}</div>
                      <h3 className="font-bold text-gray-800 text-center mb-1">{type.label}</h3>
                      <p className="text-xs text-gray-500 text-center">{type.desc}</p>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Submit Button */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                type="submit"
                disabled={loading || !file || !businessType}
                className={`w-full py-4 rounded-xl font-bold text-lg shadow-lg transition-all ${
                  loading || !file || !businessType
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:shadow-2xl'
                }`}
              >
                {loading ? (
                  <div className="flex items-center justify-center gap-3">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                    <span>Processing your file...</span>
                  </div>
                ) : (
                  <span className="flex items-center justify-center gap-2">
                    🚀 Submit for Analysis
                  </span>
                )}
              </motion.button>
            </form>
          </motion.div>

          {/* Feature Highlights */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-8 grid grid-cols-3 gap-6"
          >
            {[
              { icon: '⚡', title: 'Fast Processing', desc: '1000+ rows/second' },
              { icon: '🎯', title: '14 Tax Objects', desc: 'PPh21-26, PPN, Corrections' },
              { icon: '📊', title: 'Deep Insights', desc: 'Charts, trends & analytics' }
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 + i * 0.1 }}
                className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow"
              >
                <div className="text-3xl mb-2">{feature.icon}</div>
                <h3 className="font-bold text-gray-800 mb-1">{feature.title}</h3>
                <p className="text-sm text-gray-500">{feature.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
