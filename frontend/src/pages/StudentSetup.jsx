import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FiCpu, FiUser, FiMail, FiHash, FiArrowRight, FiAlertCircle } from 'react-icons/fi';
import { studentsAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

export default function StudentSetup({ onLogin }) {
  const navigate = useNavigate();
  const [tab, setTab] = useState('new'); // 'new' | 'existing'
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [studentIdInput, setStudentIdInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [demoStudents, setDemoStudents] = useState([]);
  const [loadingDemo, setLoadingDemo] = useState(false);

  async function fetchDemoStudents() {
    setLoadingDemo(true);
    try {
      const res = await studentsAPI.list();
      setDemoStudents(res.data || []);
    } catch {
      // silently fail — user can still enter ID manually
    } finally {
      setLoadingDemo(false);
    }
  }

  useEffect(() => {
    if (tab === 'existing') {
      fetchDemoStudents();
    }
  }, [tab]);

  async function handleNewStudent(e) {
    e.preventDefault();
    if (!name.trim() || !email.trim()) {
      setError('Please enter your name and email.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await studentsAPI.create({ name: name.trim(), email: email.trim() });
      const id = res.data?.student_id || res.data?.id;
      if (!id) throw new Error('No student ID returned from server.');
      onLogin(id);
      navigate('/assessment');
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to create student. Is the backend running?';
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  async function handleExistingStudent(e) {
    e.preventDefault();
    const id = studentIdInput.trim();
    if (!id) {
      setError('Please enter a student ID.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await studentsAPI.get(id);
      onLogin(id);
      navigate('/dashboard');
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Student not found. Check the ID and try again.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-navy-900 flex items-center justify-center px-4">
      {/* Background glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      <motion.div
        className="w-full max-w-md"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center mx-auto mb-4 shadow-xl shadow-purple-500/30">
            <FiCpu className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-black text-white">Welcome to LearnSphere AI</h1>
          <p className="text-slate-400 mt-2">Your personalized AI learning companion</p>
        </div>

        <div className="glass rounded-2xl p-6">
          {/* Tabs */}
          <div className="flex bg-white/5 rounded-xl p-1 mb-6">
            {[{ key: 'new', label: 'New Student' }, { key: 'existing', label: 'Existing Student' }].map((t) => (
              <button
                key={t.key}
                onClick={() => { setTab(t.key); setError(''); }}
                className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${
                  tab === t.key
                    ? 'bg-gradient-to-r from-purple-500 to-cyan-500 text-white shadow'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          <AnimatePresence mode="wait">
            {tab === 'new' ? (
              <motion.form
                key="new"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                onSubmit={handleNewStudent}
                className="space-y-4"
              >
                <div>
                  <label className="text-sm text-slate-300 mb-1.5 flex items-center gap-1.5">
                    <FiUser className="w-3.5 h-3.5" /> Full Name
                  </label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter your full name"
                    style={{ color: '#111827' }}
                    className="w-full bg-white border border-gray-300 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 font-medium focus:outline-none focus:border-purple-600 focus:ring-2 focus:ring-purple-500 transition-all"
                  />
                </div>
                <div>
                  <label className="text-sm text-slate-300 mb-1.5 flex items-center gap-1.5">
                    <FiMail className="w-3.5 h-3.5" /> Email
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email"
                    style={{ color: '#111827' }}
                    className="w-full bg-white border border-gray-300 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 font-medium focus:outline-none focus:border-purple-600 focus:ring-2 focus:ring-purple-500 transition-all"
                  />
                </div>

                {error && (
                  <div className="flex items-start gap-2 p-3 bg-red-500/10 border border-red-500/30 rounded-xl">
                    <FiAlertCircle className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-red-400">{error}</p>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full flex items-center justify-center gap-2 py-3 rounded-xl font-semibold bg-gradient-to-r from-purple-500 to-cyan-500 text-white hover:opacity-90 transition-all disabled:opacity-50"
                >
                  {loading ? <LoadingSpinner text="" /> : <>Create Account & Start <FiArrowRight /></>}
                </button>
              </motion.form>
            ) : (
              <motion.form
                key="existing"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                onSubmit={handleExistingStudent}
                className="space-y-4"
              >
                {loadingDemo ? (
                  <div className="flex justify-center py-4">
                    <LoadingSpinner text="Loading demo students..." />
                  </div>
                ) : demoStudents.length > 0 && (
                  <div>
                    <label className="text-sm text-slate-300 mb-1.5 block">Select Demo Student</label>
                    <select
                      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-purple-500 transition-colors"
                      onChange={(e) => setStudentIdInput(e.target.value)}
                      defaultValue=""
                    >
                      <option value="" disabled className="bg-navy-800">— Choose a demo student —</option>
                      {demoStudents.map((s) => (
                        <option key={s.student_id || s.id} value={s.student_id || s.id} className="bg-navy-800">
                          {s.name} (ID: {s.student_id || s.id})
                        </option>
                      ))}
                    </select>
                  </div>
                )}

                <div>
                  <label className="text-sm text-slate-300 mb-1.5 flex items-center gap-1.5">
                    <FiHash className="w-3.5 h-3.5" /> Or Enter Student ID
                  </label>
                  <input
                    type="text"
                    value={studentIdInput}
                    onChange={(e) => setStudentIdInput(e.target.value)}
                    placeholder="e.g. student_abc123"
                    style={{ color: '#111827' }}
                    className="w-full bg-white border border-gray-300 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 font-medium focus:outline-none focus:border-purple-600 focus:ring-2 focus:ring-purple-500 transition-all"
                  />
                </div>

                {error && (
                  <div className="flex items-start gap-2 p-3 bg-red-500/10 border border-red-500/30 rounded-xl">
                    <FiAlertCircle className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-red-400">{error}</p>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full flex items-center justify-center gap-2 py-3 rounded-xl font-semibold bg-gradient-to-r from-purple-500 to-cyan-500 text-white hover:opacity-90 transition-all disabled:opacity-50"
                >
                  {loading ? <LoadingSpinner text="" /> : <>Continue to Dashboard <FiArrowRight /></>}
                </button>
              </motion.form>
            )}
          </AnimatePresence>
        </div>

        <p className="text-center text-slate-500 text-sm mt-4">
          By continuing, you agree to use this for educational purposes.
        </p>
      </motion.div>
    </div>
  );
}
