import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer
} from 'recharts';

interface Job {
  job_id: string;
  status: string;
  file_name: string;
  business_type: string;
  summary?: {
    total_rows: number;
    avg_confidence: number;
    risk_percent: number;
  };
  error_message?: string;
}

interface PredictionRow {
  account_name: string;
  predicted_tax_object: string;
  confidence_percent: number;
  explanation?: string;
}

const COLORS = [
  '#667eea', '#764ba2', '#f093fb', '#4facfe',
  '#43e97b', '#fa709a', '#fee140', '#30cfd0'
];

const TAX_OBJECT_INFO: Record<string, { emoji: string; category: string }> = {
  'PPh21': { emoji: '👥', category: 'Employee Tax' },
  'PPh22': { emoji: '🚢', category: 'Import Tax' },
  'PPh23_Jasa': { emoji: '🔧', category: 'Service Tax' },
  'PPh23_Sewa': { emoji: '🏢', category: 'Rent Tax' },
  'PPh23_Bunga': { emoji: '💰', category: 'Interest Tax' },
  'PPh23_Dividen': { emoji: '📈', category: 'Dividend Tax' },
  'PPh23_Royalti': { emoji: '©️', category: 'Royalty Tax' },
  'PPh26': { emoji: '🌍', category: 'Foreign Tax' },
  'PPN': { emoji: '🧾', category: 'VAT' },
  'PPh4_2_Final': { emoji: '🏗️', category: 'Final Tax' },
  'Fiscal_Correction_Positive': { emoji: '⚠️', category: 'Correction +' },
  'Fiscal_Correction_Negative': { emoji: 'ℹ️', category: 'Correction -' },
  'Non_Object': { emoji: '❌', category: 'Non-Taxable' },
};

export default function ResultsPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState<Job | null>(null);
  const [rows, setRows] = useState<PredictionRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const jobRes = await axios.get(`/api/jobs/${jobId}`, {
          headers: { 'X-Aurora-Key': 'aurora-dev-key-change-in-production' }
        });
        setJob(jobRes.data);

        if (jobRes.data.status === 'completed') {
          const rowsRes = await axios.get(`/api/jobs/${jobId}/rows`, {
            headers: { 'X-Aurora-Key': 'aurora-dev-key-change-in-production' }
          });
          setRows(rowsRes.data.rows);
          setLoading(false);
        }
      } catch (error) {
        console.error('Failed to fetch results');
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, [jobId]);

  // Calculate distribution
  const taxDistribution = rows.reduce((acc, row) => {
    const label = row.predicted_tax_object;
    acc[label] = (acc[label] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const pieData = Object.entries(taxDistribution).map(([name, value]) => ({
    name,
    value,
    percentage: ((value / rows.length) * 100).toFixed(1)
  }));

  const barData = Object.entries(taxDistribution)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([name, count]) => ({ name: name.replace('PPh23_', ''), count }));

  // Confidence distribution
  const confidenceBuckets = [
    { range: '0-20%', count: 0 },
    { range: '20-40%', count: 0 },
    { range: '40-60%', count: 0 },
    { range: '60-80%', count: 0 },
    { range: '80-100%', count: 0 }
  ];

  rows.forEach(row => {
    const conf = row.confidence_percent;
    if (conf < 20) confidenceBuckets[0].count++;
    else if (conf < 40) confidenceBuckets[1].count++;
    else if (conf < 60) confidenceBuckets[2].count++;
    else if (conf < 80) confidenceBuckets[3].count++;
    else confidenceBuckets[4].count++;
  });

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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-lg font-semibold text-gray-700">Loading results...</p>
        </div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">❌</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Job Not Found</h2>
          <button
            onClick={() => navigate('/app/upload')}
            className="mt-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            ← Back to Upload
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white py-8 shadow-lg">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="text-4xl font-bold mb-2">📊 Analysis Results</h1>
            <p className="text-indigo-100">Comprehensive Tax Object Detection Report</p>
          </motion.div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Job Info Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl shadow-xl p-6 mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-2xl font-bold text-gray-800">
                📄 {job.file_name}
              </h2>
              <p className="text-gray-500">Job ID: {job.job_id}</p>
              <p className="text-gray-500">Business Type: <span className="font-semibold">{job.business_type}</span></p>
            </div>
            <div className={`px-6 py-3 rounded-full font-bold text-lg ${
              job.status === 'completed' ? 'bg-green-100 text-green-700' :
              job.status === 'processing' ? 'bg-yellow-100 text-yellow-700' :
              job.status === 'failed' ? 'bg-red-100 text-red-700' :
              'bg-gray-100 text-gray-700'
            }`}>
              {job.status === 'completed' && '✅ '}
              {job.status === 'processing' && '⏳ '}
              {job.status === 'failed' && '❌ '}
              {job.status.toUpperCase()}
            </div>
          </div>

          {job.error_message && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
              <p className="text-red-700 font-semibold">Error: {job.error_message}</p>
            </div>
          )}
        </motion.div>

        {job.status === 'processing' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded-lg mb-8"
          >
            <div className="flex items-center gap-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-600"></div>
              <div>
                <p className="font-bold text-yellow-800">Processing your file...</p>
                <p className="text-yellow-700 text-sm">This may take a few moments. Page will auto-refresh.</p>
              </div>
            </div>
          </motion.div>
        )}

        {job.status === 'completed' && job.summary && rows.length > 0 && (
          <>
            {/* Key Metrics */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
            >
              {[
                { title: 'Total Transactions', value: job.summary.total_rows.toLocaleString(), icon: '📝', color: 'from-blue-500 to-cyan-500' },
                { title: 'Average Confidence', value: `${job.summary.avg_confidence.toFixed(1)}%`, icon: '🎯', color: 'from-green-500 to-teal-500' },
                { title: 'Risk Score', value: `${job.summary.risk_percent.toFixed(1)}%`, icon: '⚠️', color: 'from-orange-500 to-red-500' },
                { title: 'Tax Objects Found', value: Object.keys(taxDistribution).length, icon: '🏷️', color: 'from-purple-500 to-pink-500' }
              ].map((metric, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 + i * 0.1 }}
                  className="bg-white rounded-xl shadow-lg overflow-hidden"
                >
                  <div className={`bg-gradient-to-r ${metric.color} p-4 text-white`}>
                    <div className="text-3xl mb-1">{metric.icon}</div>
                    <p className="text-sm font-medium opacity-90">{metric.title}</p>
                  </div>
                  <div className="p-4">
                    <p className="text-3xl font-bold text-gray-800">{metric.value}</p>
                  </div>
                </motion.div>
              ))}
            </motion.div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              {/* Pie Chart */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  🥧 Tax Object Distribution
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({name, percentage}) => `${name}: ${percentage}%`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {pieData.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </motion.div>

              {/* Bar Chart */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  📊 Top 10 Tax Objects by Count
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={barData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#667eea" />
                  </BarChart>
                </ResponsiveContainer>
              </motion.div>

              {/* Confidence Distribution */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  🎯 Prediction Confidence Distribution
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={confidenceBuckets}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="range" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#4facfe" />
                  </BarChart>
                </ResponsiveContainer>
              </motion.div>

              {/* Summary Table */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  📋 Tax Object Summary
                </h3>
                <div className="space-y-2 max-h-[300px] overflow-y-auto">
                  {Object.entries(taxDistribution)
                    .sort((a, b) => b[1] - a[1])
                    .map(([label, count]) => {
                      const info = TAX_OBJECT_INFO[label] || { emoji: '📌', category: label };
                      const percentage = ((count / rows.length) * 100).toFixed(1);
                      return (
                        <div key={label} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                          <div className="flex items-center gap-2">
                            <span className="text-2xl">{info.emoji}</span>
                            <div>
                              <p className="font-semibold text-gray-800 text-sm">{label}</p>
                              <p className="text-xs text-gray-500">{info.category}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="font-bold text-indigo-600">{count}</p>
                            <p className="text-xs text-gray-500">{percentage}%</p>
                          </div>
                        </div>
                      );
                    })}
                </div>
              </motion.div>
            </div>

            {/* Detailed Results Table */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
              className="bg-white rounded-xl shadow-lg overflow-hidden mb-8"
            >
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 text-white">
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  📑 Detailed Predictions ({rows.length} rows)
                </h2>
                <p className="text-indigo-100 mt-1">Complete transaction-level analysis</p>
              </div>

              <div className="overflow-x-auto max-h-[600px]">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50 sticky top-0">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">#</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Account Name</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tax Object</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Confidence</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Explanation</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {rows.map((row, i) => {
                      const info = TAX_OBJECT_INFO[row.predicted_tax_object] || { emoji: '📌', category: row.predicted_tax_object };
                      return (
                        <tr key={i} className="hover:bg-indigo-50 transition">
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{i + 1}</td>
                          <td className="px-6 py-4 text-sm text-gray-900 font-medium">{row.account_name}</td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center gap-2">
                              <span className="text-xl">{info.emoji}</span>
                              <div>
                                <p className="text-sm font-semibold text-gray-800">{row.predicted_tax_object}</p>
                                <p className="text-xs text-gray-500">{info.category}</p>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center gap-2">
                              <span>{getConfidenceEmoji(row.confidence_percent)}</span>
                              <span className={`font-bold ${getConfidenceColor(row.confidence_percent)}`}>
                                {row.confidence_percent.toFixed(1)}%
                              </span>
                            </div>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">
                            {row.explanation || 'N/A'}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </motion.div>

            {/* Action Buttons */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
              className="flex gap-4 justify-center"
            >
              <button
                onClick={() => navigate('/app/upload')}
                className="px-8 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition"
              >
                📁 Upload Another File
              </button>
              <button
                onClick={() => {
                  const csv = [
                    ['Account Name', 'Tax Object', 'Confidence %', 'Explanation'],
                    ...rows.map(r => [r.account_name, r.predicted_tax_object, r.confidence_percent, r.explanation || ''])
                  ].map(row => row.join(',')).join('\n');

                  const blob = new Blob([csv], { type: 'text/csv' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = `aurora_results_${jobId}.csv`;
                  a.click();
                }}
                className="px-8 py-3 bg-gradient-to-r from-green-600 to-teal-600 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition"
              >
                💾 Download Results CSV
              </button>
            </motion.div>
          </>
        )}
      </div>
    </div>
  );
}
