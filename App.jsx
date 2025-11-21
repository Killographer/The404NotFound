import React, { useState, useRef } from 'react';
import { FileText, Upload, X } from 'lucide-react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import GlassCard from './components/GlassCard';
import GlassButton from './components/GlassButton';

const API_BASE_URL = 'http://localhost:5000';

function App() {
  const [activeTab, setActiveTab] = useState('scan');
  const [inputText, setInputText] = useState('');
  const [wordCount, setWordCount] = useState(0);
  const [selectedFile, setSelectedFile] = useState(null);
  const [packageName, setPackageName] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const fileInputRef = useRef(null);

  const handleTextChange = (e) => {
    const text = e.target.value;
    setInputText(text);
    setWordCount(text.trim().split(/\s+/).filter(word => word.length > 0).length);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith('.apk')) {
      setSelectedFile(file);
    }
  };

  const handleScan = async () => {
    setLoading(true);
    setResults(null);

    try {
      let response;
      
      if (activeTab === 'upload' && selectedFile) {
        const formData = new FormData();
        formData.append('file', selectedFile);
        response = await fetch(`${API_BASE_URL}/analyze_apk`, {
          method: 'POST',
          body: formData,
        });
      } else if (activeTab === 'package' && packageName) {
        response = await fetch(`${API_BASE_URL}/analyze_package`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ package_name: packageName }),
        });
      } else {
        alert('Please provide input first');
        setLoading(false);
        return;
      }

      const data = await response.json();
      if (response.ok) {
        setResults(data);
      } else {
        alert('Error: ' + (data.error || 'Failed to analyze'));
      }
    } catch (error) {
      alert('Error connecting to server. Make sure the backend is running on port 5000.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setResults(null);
    setInputText('');
    setWordCount(0);
    setSelectedFile(null);
    setPackageName('');
  };

  return (
    <div className="min-h-screen relative z-10 px-4 md:px-6 py-6 md:py-8">
      <div className="max-w-7xl mx-auto">
        <Header 
          title="🔍 BroIsThisFake" 
          subtitle="Detect suspicious and fraudulent Android banking apps with AI-powered analysis"
        />

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <GlassCard className="mb-6" padding="large">
              {/* Tab Buttons */}
              <div className="flex gap-3 mb-6">
                <button
                  onClick={() => setActiveTab('upload')}
                  className={`
                    flex-1 px-6 py-3 rounded-xl font-semibold
                    transition-all duration-300
                    ${activeTab === 'upload' 
                      ? 'glass-strong bg-white/25 border-white/40 shadow-lg' 
                      : 'glass-soft bg-white/10 border-white/20 hover:bg-white/15'
                    }
                    ${activeTab === 'upload' ? 'text-white scale-105' : 'text-white/80 hover:scale-105'}
                  `}
                >
                  <div className="flex items-center justify-center gap-2">
                    <Upload className="w-4 h-4" />
                    <span>Upload File</span>
                  </div>
                </button>
                <button
                  onClick={() => setActiveTab('package')}
                  className={`
                    flex-1 px-6 py-3 rounded-xl font-semibold
                    transition-all duration-300
                    ${activeTab === 'package' 
                      ? 'glass-strong bg-white/25 border-white/40 shadow-lg' 
                      : 'glass-soft bg-white/10 border-white/20 hover:bg-white/15'
                    }
                    ${activeTab === 'package' ? 'text-white scale-105' : 'text-white/80 hover:scale-105'}
                  `}
                >
                  <div className="flex items-center justify-center gap-2">
                    <FileText className="w-4 h-4" />
                    <span>Package Name</span>
                  </div>
                </button>
              </div>

              {/* Upload Tab */}
              {activeTab === 'upload' && (
                <div className="space-y-6">
                  <div
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                    className="glass-soft border-2 border-dashed border-white/40 rounded-2xl p-12 md:p-16 text-center cursor-pointer transition-all duration-400 hover:bg-white/15 hover:border-white/60 hover:-translate-y-1 hover:shadow-2xl relative overflow-hidden group"
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept=".apk"
                      onChange={handleFileSelect}
                      className="hidden"
                    />
                    <div className="relative z-10">
                      <Upload className="w-16 h-16 mx-auto mb-4 text-white/90 drop-shadow-lg" />
                      <p className="text-xl font-semibold text-white mb-2">
                        {selectedFile ? selectedFile.name : 'Click to upload APK file'}
                      </p>
                      <p className="text-sm text-white/70">
                        or drag and drop here
                      </p>
                    </div>
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
                  </div>
                </div>
              )}

              {/* Package Name Tab */}
              {activeTab === 'package' && (
                <div className="space-y-4">
                  <div>
                    <label className="block mb-2 font-semibold text-white">
                      Package Name
                    </label>
                    <input
                      type="text"
                      value={packageName}
                      onChange={(e) => setPackageName(e.target.value)}
                      placeholder="e.g., com.example.bankapp"
                      className="w-full px-5 py-4 rounded-xl glass-soft border-white/30 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30 focus:bg-white/20 transition-all"
                    />
                    <small className="block mt-2 text-white/70 text-sm">
                      Enter the Android app package name to analyze
                    </small>
                  </div>
                </div>
              )}

              {/* Word Count (for text input - if needed) */}
              {activeTab === 'scan' && inputText && (
                <div className="mt-4 text-right">
                  <span className="text-white/70 text-sm">
                    {wordCount} words
                  </span>
                </div>
              )}

              {/* Scan Button */}
              <div className="mt-6">
                <GlassButton
                  onClick={handleScan}
                  disabled={loading || (activeTab === 'upload' && !selectedFile) || (activeTab === 'package' && !packageName)}
                  className="w-full text-lg py-5 uppercase tracking-wide"
                  variant="primary"
                >
                  {loading ? 'Scanning...' : '🔍 Scan for Fake Banking Apps'}
                </GlassButton>
              </div>
            </GlassCard>

            {/* Results Section */}
            {results && (
              <div className="space-y-6 animate-fade-in-up">
                <GlassCard padding="large">
                  <h2 className="text-3xl font-bold text-white mb-6">Analysis Results</h2>
                  
                  {/* Risk Badge */}
                  <div className={`
                    glass rounded-2xl p-8 mb-6 text-center
                    ${results.risk_level === 'HIGH' ? 'bg-red-500/20 border-red-500/40' : ''}
                    ${results.risk_level === 'MEDIUM' ? 'bg-orange-500/20 border-orange-500/40' : ''}
                    ${results.risk_level === 'LOW' ? 'bg-green-500/20 border-green-500/40' : ''}
                  `}>
                    <div className="text-4xl font-extrabold mb-4 text-white drop-shadow-lg">
                      {results.risk_level || 'UNKNOWN'}
                    </div>
                    <div className="flex justify-between items-center mb-4">
                      <span className="text-xl font-bold text-white">
                        Risk Score: {results.risk_score || 0}/100
                      </span>
                      <span className="text-2xl font-extrabold text-white">
                        {results.risk_score || 0}%
                      </span>
                    </div>
                    <div className="w-full h-9 bg-white/10 rounded-full overflow-hidden mb-4">
                      <div 
                        className="h-full bg-gradient-to-r from-white/40 to-white/60 rounded-full transition-all duration-800 flex items-center justify-center text-white font-bold text-sm"
                        style={{ width: `${results.risk_score || 0}%` }}
                      />
                    </div>
                  </div>

                  {/* Package Info */}
                  <div className="mb-6">
                    <h3 className="text-xl font-bold text-white mb-4">Package Information</h3>
                    <div className="space-y-2 text-white/95">
                      <p><strong>Package:</strong> {results.package_name || '-'}</p>
                      <p>
                        <strong>Status:</strong>{' '}
                        <span className={results.is_fake ? 'text-red-400' : 'text-green-400'}>
                          {results.is_fake ? '⚠️ FAKE APP DETECTED' : '✅ App looks legitimate'}
                        </span>
                      </p>
                      <p><strong>App Type:</strong> {results.app_type || 'Not classified'}</p>
                    </div>
                  </div>

                  {/* Evidence Kit */}
                  {results.takedown_email && (
                    <div className="mb-6">
                      <h3 className="text-xl font-bold text-white mb-4">Evidence Kit</h3>
                      <p className="text-white/80 mb-4 text-sm">
                        This section summarises why the app was flagged and prepares a ready-to-use takedown email.
                      </p>
                      <div className="space-y-4">
                        <div>
                          <label className="block mb-2 font-semibold text-white text-sm">
                            Subject
                          </label>
                          <input
                            type="text"
                            value={results.takedown_email.subject || ''}
                            readOnly
                            className="w-full px-4 py-3 rounded-xl glass-soft border-white/20 text-white text-sm"
                          />
                        </div>
                        <div>
                          <label className="block mb-2 font-semibold text-white text-sm">
                            Body
                          </label>
                          <textarea
                            value={results.takedown_email.body || ''}
                            readOnly
                            rows={6}
                            className="w-full px-4 py-3 rounded-xl glass-soft border-white/20 text-white text-sm resize-y"
                          />
                        </div>
                        <div className="flex gap-3">
                          <GlassButton
                            variant="secondary"
                            onClick={() => {
                              navigator.clipboard.writeText(results.takedown_email.body || '');
                              alert('Takedown email copied to clipboard.');
                            }}
                            className="text-sm"
                          >
                            Copy Email
                          </GlassButton>
                          <GlassButton
                            variant="secondary"
                            onClick={() => {
                              const subject = encodeURIComponent(results.takedown_email.subject || '');
                              const body = encodeURIComponent(results.takedown_email.body || '');
                              window.open(`https://mail.google.com/mail/?view=cm&fs=1&to=play-developer-support@google.com&su=${subject}&body=${body}`, '_blank');
                            }}
                            className="text-sm"
                          >
                            Open in Gmail
                          </GlassButton>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Checks */}
                  <div className="space-y-4 mb-6">
                    {results.checks?.permissions && (
                      <GlassCard padding="default">
                        <h4 className="text-lg font-bold text-white mb-2">🔐 Permissions Check</h4>
                        <p className="text-white/90 mb-2">{results.checks.permissions.message || '-'}</p>
                        <ul className="list-disc list-inside text-white/85 space-y-1 text-sm">
                          {results.checks.permissions.suspicious_permissions?.length > 0
                            ? results.checks.permissions.suspicious_permissions.map((perm, idx) => (
                                <li key={idx}>{perm}</li>
                              ))
                            : <li>No suspicious permissions found</li>
                          }
                        </ul>
                      </GlassCard>
                    )}

                    {results.checks?.package_similarity && (
                      <GlassCard padding="default">
                        <h4 className="text-lg font-bold text-white mb-2">🔗 Package Similarity</h4>
                        <p className="text-white/90 mb-2">{results.checks.package_similarity.message || '-'}</p>
                        <ul className="list-disc list-inside text-white/85 space-y-1 text-sm">
                          {results.checks.package_similarity.similar_apps?.length > 0
                            ? results.checks.package_similarity.similar_apps.map((app, idx) => (
                                <li key={idx}>{app.package} ({app.similarity}% similar)</li>
                              ))
                            : <li>No similar apps found</li>
                          }
                        </ul>
                      </GlassCard>
                    )}

                    {results.checks?.playstore && (
                      <GlassCard padding="default">
                        <h4 className="text-lg font-bold text-white mb-2">🏪 Play Store Check</h4>
                        <p className="text-white/90 mb-2">{results.checks.playstore.message || '-'}</p>
                        {results.checks.playstore.exists_on_playstore ? (
                          <div className="text-white/85 text-sm space-y-1">
                            <p><strong>Rating:</strong> {results.checks.playstore.rating ? `${results.checks.playstore.rating}/5.0` : 'N/A'}</p>
                            <p><strong>Reviews:</strong> {results.checks.playstore.review_count || 0}</p>
                            <p><strong>Developer:</strong> {results.checks.playstore.developer || 'Unknown'}</p>
                          </div>
                        ) : (
                          <p className="text-red-400 text-sm">App not found on Play Store</p>
                        )}
                      </GlassCard>
                    )}
                  </div>

                  <GlassButton
                    onClick={resetAnalysis}
                    variant="secondary"
                    className="w-full"
                  >
                    Analyze Another App
                  </GlassButton>
                </GlassCard>
              </div>
            )}

            {/* Loading Spinner */}
            {loading && (
              <GlassCard padding="large" className="text-center">
                <div className="w-16 h-16 border-4 border-white/20 border-t-white rounded-full animate-spin mx-auto mb-4" />
                <p className="text-white font-semibold text-lg">Analyzing app...</p>
              </GlassCard>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="glass-soft rounded-2xl p-6 text-center mt-8">
          <p className="text-white/80 text-sm">
            Built for Pixel Pitch 2025 | BroIsThisFake
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;

