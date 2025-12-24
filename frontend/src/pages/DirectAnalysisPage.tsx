import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../lib/axios';
import { motion, AnimatePresence } from 'framer-motion';

interface AnalysisResult {
  account_name: string;
  predicted_label: string;
  confidence: number;
  explanation: string;
}

const TAX_OBJECT_INFO: Record<string, { emoji: string; category: string; description: string; rate: string }> = {
  'PPh21': {
    emoji: '👥',
    category: 'Employee Income Tax',
    description: 'Withholding tax on employment income, wages, salaries, honorariums, and allowances',
    rate: 'Progressive rate (5%-35%) or flat rates based on income level'
  },
  'PPh22': {
    emoji: '🚢',
    category: 'Import & Specific Transaction Tax',
    description: 'Tax collection on imports, government purchases, and specific industries',
    rate: 'Various rates: 2.5%-7.5% depending on transaction type'
  },
  'PPh23_Jasa': {
    emoji: '🔧',
    category: 'Service Tax',
    description: 'Withholding tax on various services including consulting, maintenance, legal services',
    rate: '2% of gross amount'
  },
  'PPh23_Sewa': {
    emoji: '🏢',
    category: 'Rent Tax',
    description: 'Withholding tax on rental income for land, buildings, or equipment',
    rate: '2% of gross rental amount'
  },
  'PPh23_Bunga': {
    emoji: '💰',
    category: 'Interest Tax',
    description: 'Withholding tax on interest income from deposits, bonds, or loans',
    rate: '15% of gross interest'
  },
  'PPh23_Dividen': {
    emoji: '📈',
    category: 'Dividend Tax',
    description: 'Withholding tax on dividend distributions to shareholders',
    rate: '15% of gross dividend (or exempt under certain conditions)'
  },
  'PPh23_Royalti': {
    emoji: '©️',
    category: 'Royalty Tax',
    description: 'Withholding tax on royalty payments for intellectual property',
    rate: '15% of gross royalty'
  },
  'PPh26': {
    emoji: '🌍',
    category: 'Foreign Recipient Tax',
    description: 'Withholding tax on payments to foreign entities or individuals',
    rate: '20% (or tax treaty rate if applicable)'
  },
  'PPN': {
    emoji: '🧾',
    category: 'Value Added Tax',
    description: 'Tax on consumption of goods and services',
    rate: '11% (as of 2022, adjustable by regulation)'
  },
  'PPh4_2_Final': {
    emoji: '🏗️',
    category: 'Final Income Tax',
    description: 'Final withholding tax on specific income types (construction, rent, interest, etc.)',
    rate: 'Various rates: 0.5%-10% depending on income type'
  },
  'Fiscal_Correction_Positive': {
    emoji: '⚠️',
    category: 'Positive Fiscal Correction',
    description: 'Increases taxable income (non-deductible expense)',
    rate: 'Adjustment to taxable income'
  },
  'Fiscal_Correction_Negative': {
    emoji: 'ℹ️',
    category: 'Negative Fiscal Correction',
    description: 'Decreases taxable income (non-taxable income)',
    rate: 'Adjustment to taxable income'
  },
  'Non_Object': {
    emoji: '❌',
    category: 'Non-Taxable',
    description: 'Transaction that is not subject to income tax withholding',
    rate: 'N/A'
  }
};

export default function DirectAnalysisPage() {
  const navigate = useNavigate();
  const [inputMode, setInputMode] = useState<'single' | 'bulk'>('single');
  const [singleText, setSingleText] = useState('');
  const [bulkText, setBulkText] = useState('');
  const [loading, setLoading] = useState(false);
  const [singleResult, setSingleResult] = useState<AnalysisResult | null>(null);
  const [bulkResults, setBulkResults] = useState<AnalysisResult[]>([]);

  const analyzeSingle = async () => {
    if (!singleText.trim()) return;

    setLoading(true);
    try {
      const response = await api.post('/api/predict/direct', {
        texts: [singleText],
      });

      setSingleResult(response.data.predictions[0]);
    } catch (error) {
      alert('Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const analyzeBulk = async () => {
    if (!bulkText.trim()) return;

    const lines = bulkText.split('\n').filter(line => line.trim()).slice(0, 100);

    setLoading(true);
    try {
      const response = await api.post('/api/predict/direct', {
        texts: lines,
      });

      setBulkResults(response.data.predictions);
    } catch (error) {
      alert('Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (conf: number) => {
    if (conf >= 80) return 'text-green-600';
    if (conf >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceEmoji = (conf: number) => {
    if (conf >= 80) return '🟢';
    if (conf >= 60) return '🟡';
    return '🔴';
  };

  const renderSingleResult = (result: AnalysisResult) => {
    const info = TAX_OBJECT_INFO[result.predicted_label] || {
      emoji: '📌',
      category: result.predicted_label,
      description: 'Information not available',
      rate: 'N/A'
    };

    const confidenceEmoji = getConfidenceEmoji(result.confidence);
    const confidenceColor = getConfidenceColor(result.confidence);

    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-6"
      >
        {/* Tax Object Card */}
        <div className="bg-gradient-to-br from-indigo-50 to-purple-50 border-l-4 border-indigo-600 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <div className="text-5xl">{info.emoji}</div>
            <div className="flex-1">
              <h3 className="text-2xl font-bold text-gray-800 mb-1">{confidenceEmoji} Tax Object Detected</h3>
              <p className={`text-3xl font-bold ${confidenceColor} mb-3`}>
                {result.predicted_label}
              </p>
              <div className="space-y-2 text-sm">
                <p><span className="font-semibold text-gray-700">Category:</span> {info.category}</p>
                <p><span className="font-semibold text-gray-700">Description:</span> {info.description}</p>
                <p><span className="font-semibold text-gray-700">Tax Rate:</span> {info.rate}</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm font-medium text-gray-500 mb-1">Confidence</div>
              <div className={`text-4xl font-bold ${confidenceColor}`}>
                {result.confidence.toFixed(1)}%
              </div>
            </div>
          </div>
        </div>

        {/* Explanation Card */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h4 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
            💡 AI Explanation
          </h4>
          <p className="text-gray-700">{result.explanation}</p>
        </div>

        {/* Confidence Bar */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h4 className="text-sm font-semibold text-gray-700 mb-3">Confidence Level</h4>
          <div className="relative h-8 bg-gray-200 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${result.confidence}%` }}
              transition={{ duration: 1, ease: 'easeOut' }}
              className={`h-full ${
                result.confidence >= 80 ? 'bg-gradient-to-r from-green-500 to-teal-500' :
                result.confidence >= 60 ? 'bg-gradient-to-r from-yellow-500 to-orange-500' :
                'bg-gradient-to-r from-red-500 to-pink-500'
              }`}
            />
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="font-bold text-white drop-shadow-lg">
                {result.confidence.toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      </motion.div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white py-8 shadow-lg">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="text-4xl font-bold mb-2">✍️ Direct Text Analysis</h1>
            <p className="text-indigo-100">Instant tax object detection from transaction descriptions</p>
          </motion.div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">

          {/* Mode Tabs */}
          <div className="flex gap-4 mb-8">
            <motion.div
              whileHover={{ scale: 1.02 }}
              onClick={() => navigate('/app/upload')}
              className="flex-1 bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-400 cursor-pointer hover:shadow-xl transition-shadow"
            >
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center text-2xl">
                  📁
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-800">Batch File Upload</h2>
                  <p className="text-sm text-gray-500">Process entire GL files</p>
                </div>
              </div>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.02 }}
              className="flex-1 bg-white rounded-lg shadow-lg p-6 border-l-4 border-indigo-600"
            >
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center text-2xl">
                  ✍️
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-800">Direct Text Analysis</h2>
                  <p className="text-sm text-gray-500">Analyze transactions instantly</p>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Input Mode Selector */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl shadow-lg p-6 mb-8"
          >
            <div className="flex gap-4 mb-6">
              <button
                onClick={() => {
                  setInputMode('single');
                  setSingleResult(null);
                  setBulkResults([]);
                }}
                className={`flex-1 py-4 rounded-lg font-bold transition-all ${
                  inputMode === 'single'
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                🔍 Single Transaction
              </button>
              <button
                onClick={() => {
                  setInputMode('bulk');
                  setSingleResult(null);
                  setBulkResults([]);
                }}
                className={`flex-1 py-4 rounded-lg font-bold transition-all ${
                  inputMode === 'bulk'
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                📝 Multiple Transactions (Bulk)
              </button>
            </div>

            <AnimatePresence mode="wait">
              {inputMode === 'single' ? (
                <motion.div
                  key="single"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="space-y-4"
                >
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Enter transaction description:
                    </label>
                    <textarea
                      value={singleText}
                      onChange={(e) => setSingleText(e.target.value)}
                      placeholder="Example: Pembayaran gaji karyawan bulan Januari 2024"
                      className="w-full border-2 border-gray-300 rounded-lg p-4 focus:border-indigo-500 focus:outline-none transition"
                      rows={3}
                    />
                  </div>
                  <button
                    onClick={analyzeSingle}
                    disabled={loading || !singleText.trim()}
                    className={`w-full py-3 rounded-lg font-bold transition-all ${
                      loading || !singleText.trim()
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:shadow-lg'
                    }`}
                  >
                    {loading ? (
                      <span className="flex items-center justify-center gap-2">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        Analyzing...
                      </span>
                    ) : (
                      '🔍 Analyze Transaction'
                    )}
                  </button>
                </motion.div>
              ) : (
                <motion.div
                  key="bulk"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-4"
                >
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Enter multiple transactions (one per line, max 100):
                    </label>
                    <textarea
                      value={bulkText}
                      onChange={(e) => setBulkText(e.target.value)}
                      placeholder="Example:&#10;Pembayaran gaji karyawan bulan Januari&#10;Sewa gedung kantor&#10;Pembelian ATK&#10;Bunga deposito bank"
                      className="w-full border-2 border-gray-300 rounded-lg p-4 focus:border-indigo-500 focus:outline-none transition font-mono text-sm"
                      rows={8}
                    />
                  </div>
                  <button
                    onClick={analyzeBulk}
                    disabled={loading || !bulkText.trim()}
                    className={`w-full py-3 rounded-lg font-bold transition-all ${
                      loading || !bulkText.trim()
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:shadow-lg'
                    }`}
                  >
                    {loading ? (
                      <span className="flex items-center justify-center gap-2">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        Analyzing {bulkText.split('\n').filter(l => l.trim()).length} transactions...
                      </span>
                    ) : (
                      '🔍 Analyze All Transactions'
                    )}
                  </button>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>

          {/* Results */}
          {inputMode === 'single' && singleResult && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-xl shadow-lg p-8"
            >
              <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                📊 Analysis Result
              </h2>
              {renderSingleResult(singleResult)}
            </motion.div>
          )}

          {inputMode === 'bulk' && bulkResults.length > 0 && (
            <div className="space-y-6">
              {/* Summary */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="grid grid-cols-1 md:grid-cols-3 gap-6"
              >
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <div className="text-3xl mb-2">📝</div>
                  <div className="text-sm text-gray-500 mb-1">Total Analyzed</div>
                  <div className="text-3xl font-bold text-indigo-600">{bulkResults.length}</div>
                </div>
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <div className="text-3xl mb-2">🎯</div>
                  <div className="text-sm text-gray-500 mb-1">Avg Confidence</div>
                  <div className="text-3xl font-bold text-green-600">
                    {(bulkResults.reduce((sum, r) => sum + r.confidence, 0) / bulkResults.length).toFixed(1)}%
                  </div>
                </div>
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <div className="text-3xl mb-2">⚠️</div>
                  <div className="text-sm text-gray-500 mb-1">Low Confidence</div>
                  <div className="text-3xl font-bold text-red-600">
                    {bulkResults.filter(r => r.confidence < 60).length}
                  </div>
                </div>
              </motion.div>

              {/* Results Table */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="bg-white rounded-xl shadow-lg overflow-hidden"
              >
                <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 text-white">
                  <h2 className="text-2xl font-bold">📊 Bulk Analysis Results</h2>
                </div>
                <div className="overflow-x-auto max-h-[600px]">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50 sticky top-0">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">#</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Transaction</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tax Object</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Confidence</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {bulkResults.map((result, i) => {
                        const info = TAX_OBJECT_INFO[result.predicted_label] || { emoji: '📌', category: result.predicted_label };
                        return (
                          <tr key={i} className="hover:bg-indigo-50 transition">
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{i + 1}</td>
                            <td className="px-6 py-4 text-sm text-gray-900 font-medium max-w-xs truncate">
                              {result.account_name}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center gap-2">
                                <span className="text-xl">{info.emoji}</span>
                                <span className="font-semibold text-gray-800">{result.predicted_label}</span>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center gap-2">
                                <span>{getConfidenceEmoji(result.confidence)}</span>
                                <span className={`font-bold ${getConfidenceColor(result.confidence)}`}>
                                  {result.confidence.toFixed(1)}%
                                </span>
                              </div>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </motion.div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
