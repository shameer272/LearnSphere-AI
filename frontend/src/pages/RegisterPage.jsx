import { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiCpu, FiUser, FiMail, FiLock, FiArrowRight, FiAlertCircle, FiCheck, FiLayers } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import { subjectsAPI } from '../services/api';
import Navbar from '../components/Navbar';
import { CATEGORY_SUBJECT_CODES, getSubjectIdsForCategory } from '../utils/categoryCurriculum';

export default function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [learningLevel, setLearningLevel] = useState('Intermediate');
  const [availableSubjects, setAvailableSubjects] = useState([]);
  const [selectedSubjectIds, setSelectedSubjectIds] = useState([]);
  const [selectedCategoryName, setSelectedCategoryName] = useState('');
  const [loadingSubjects, setLoadingSubjects] = useState(true);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    async function fetchSubjects() {
      try {
        const res = await subjectsAPI.list();
        const subjects = res.data || [];
        setAvailableSubjects(subjects);

        // Read selected category and subject IDs/codes from navigation state or URL parameters
        const passedCategory = location.state?.category || searchParams.get('category');
        const passedCodes = location.state?.subjectCodes || (passedCategory ? CATEGORY_SUBJECT_CODES[passedCategory] : null);
        const passedIds = location.state?.subjectIds;

        if (passedCategory) {
          setSelectedCategoryName(passedCategory);
        }

        if (Array.isArray(passedIds) && passedIds.length > 0) {
          // Preselect specific IDs passed directly
          const validIds = subjects.filter((s) => passedIds.includes(s.id)).map((s) => s.id);
          setSelectedSubjectIds(validIds);
        } else if (Array.isArray(passedCodes) && passedCodes.length > 0) {
          // Automatically preselect ONLY the subjects belonging to the category clicked
          const matchingIds = subjects.filter((s) => passedCodes.includes(s.code)).map((s) => s.id);
          setSelectedSubjectIds(matchingIds);
        } else if (passedCategory) {
          // Fallback via helper
          const matchingIds = getSubjectIdsForCategory(passedCategory, subjects);
          setSelectedSubjectIds(matchingIds);
        } else {
          // If registration is opened directly without a category selection, start with ZERO subjects selected
          setSelectedSubjectIds([]);
        }
      } catch (err) {
        console.error('Failed to load subjects:', err);
      } finally {
        setLoadingSubjects(false);
      }
    }
    fetchSubjects();
  }, [location.state, searchParams]);

  const toggleSubject = (id) => {
    setSelectedSubjectIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Please enter your full name.');
      return;
    }
    if (!email.trim() || !/\S+@\S+\.\S+/.test(email.trim())) {
      setError('Please enter a valid email address.');
      return;
    }
    if (!password) {
      setError('Please enter a password.');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match. Please re-enter.');
      return;
    }
    if (selectedSubjectIds.length === 0) {
      setError('Please select at least one B.Tech CSE subject to get started.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await register({
        name: name.trim(),
        email: email.trim().toLowerCase(),
        password,
        learning_level: learningLevel,
        degree: 'B.Tech Computer Science and Engineering',
        selected_subject_ids: selectedSubjectIds,
      });
      navigate('/dashboard');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Registration failed. Please try again.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-navy-900 flex flex-col selection:bg-purple-500 selection:text-white">
      <Navbar />

      <div className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="w-full max-w-2xl"
        >
          <div className="glass rounded-3xl p-8 sm:p-10 border border-white/10 shadow-2xl backdrop-blur-2xl">
            <div className="text-center mb-8">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center mx-auto mb-4 shadow-xl shadow-purple-500/25">
                <FiCpu className="w-7 h-7 text-white" />
              </div>
              <h1 className="text-3xl font-black text-white tracking-tight">Create Student Account</h1>
              <p className="text-slate-400 text-sm mt-1.5">
                Join the B.Tech Computer Science adaptive learning platform
              </p>
            </div>

            {error && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-start gap-2.5 text-rose-300 text-sm"
              >
                <FiAlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5 text-rose-400" />
                <span>{error}</span>
              </motion.div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Full Name
                  </label>
                  <div className="relative">
                    <FiUser className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 w-4 h-4 pointer-events-none" />
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="Devansh Singhania"
                      required
                      style={{ color: '#111827' }}
                      className="w-full pl-10 pr-4 py-3 rounded-xl bg-white text-gray-900 border border-gray-300 placeholder-gray-400 text-sm focus:outline-none focus:border-purple-600 focus:ring-2 focus:ring-purple-500 font-medium transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Email Address
                  </label>
                  <div className="relative">
                    <FiMail className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 w-4 h-4 pointer-events-none" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="student@btech.edu"
                      required
                      style={{ color: '#111827' }}
                      className="w-full pl-10 pr-4 py-3 rounded-xl bg-white text-gray-900 border border-gray-300 placeholder-gray-400 text-sm focus:outline-none focus:border-purple-600 focus:ring-2 focus:ring-purple-500 font-medium transition-all"
                    />
                  </div>
                </div>
              </div>

              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Password (Min. 6 chars)
                  </label>
                  <div className="relative">
                    <FiLock className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 w-4 h-4 pointer-events-none" />
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      required
                      style={{ color: '#111827' }}
                      className="w-full pl-10 pr-4 py-3 rounded-xl bg-white text-gray-900 border border-gray-300 placeholder-gray-400 text-sm focus:outline-none focus:border-purple-600 focus:ring-2 focus:ring-purple-500 font-medium transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Confirm Password
                  </label>
                  <div className="relative">
                    <FiLock className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 w-4 h-4 pointer-events-none" />
                    <input
                      type="password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="••••••••"
                      required
                      style={{ color: '#111827' }}
                      className="w-full pl-10 pr-4 py-3 rounded-xl bg-white text-gray-900 border border-gray-300 placeholder-gray-400 text-sm focus:outline-none focus:border-purple-600 focus:ring-2 focus:ring-purple-500 font-medium transition-all"
                    />
                  </div>
                </div>
              </div>

              {/* Learning Level Selection */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Initial Experience Level
                </label>
                <div className="grid grid-cols-3 gap-2.5">
                  {['Beginner', 'Intermediate', 'Advanced'].map((lvl) => (
                    <button
                      key={lvl}
                      type="button"
                      onClick={() => setLearningLevel(lvl)}
                      className={`py-2.5 px-3 rounded-xl text-xs sm:text-sm font-semibold transition-all border ${
                        learningLevel === lvl
                          ? 'bg-purple-500/20 text-purple-300 border-purple-500/50 shadow-md'
                          : 'glass text-slate-400 hover:text-white border-white/5'
                      }`}
                    >
                      {lvl}
                    </button>
                  ))}
                </div>
              </div>

              {/* Subject Selection Multi-Select */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Select Focus Subjects ({selectedSubjectIds.length} selected)
                  </label>
                  <span className="text-xs text-purple-400">Click to toggle</span>
                </div>

                {selectedCategoryName && (
                  <div className="mb-2.5 px-3 py-2 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-between text-xs text-purple-200">
                    <span className="flex items-center gap-1.5">
                      <FiLayers className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Curriculum Track: <strong>{selectedCategoryName}</strong></span>
                    </span>
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedCategoryName('');
                        setSelectedSubjectIds([]);
                      }}
                      className="text-[11px] text-slate-400 hover:text-white underline cursor-pointer"
                    >
                      Clear track
                    </button>
                  </div>
                )}

                {loadingSubjects ? (
                  <p className="text-xs text-slate-400 py-3">Loading B.Tech CSE subjects...</p>
                ) : (
                  <div className="max-h-48 overflow-y-auto pr-1 space-y-1.5 border border-white/10 p-2.5 rounded-xl bg-navy-950/50 scrollbar-thin">
                    {availableSubjects.map((s) => {
                      const selected = selectedSubjectIds.includes(s.id);
                      return (
                        <div
                          key={s.id}
                          onClick={() => toggleSubject(s.id)}
                          className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs cursor-pointer transition-all border ${
                            selected
                              ? 'bg-purple-500/20 text-white border-purple-500/40'
                              : 'bg-white/5 text-slate-300 border-transparent hover:bg-white/10'
                          }`}
                        >
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-[10px] text-purple-300 px-1.5 py-0.5 rounded bg-purple-500/20">
                              {s.code}
                            </span>
                            <span className="font-medium">{s.name}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-[10px] text-slate-400">{s.category}</span>
                            {selected ? (
                              <div className="w-4 h-4 rounded-full bg-cyan-400 flex items-center justify-center text-navy-950">
                                <FiCheck className="w-3 h-3 stroke-[3]" />
                              </div>
                            ) : (
                              <div className="w-4 h-4 rounded-full border border-slate-500" />
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full mt-4 py-3.5 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-500 via-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-500/25 hover:opacity-95 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? (
                  <span>Creating Account...</span>
                ) : (
                  <>
                    <span>Complete Registration & Launch Dashboard</span>
                    <FiArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>

            <div className="mt-6 text-center text-sm text-slate-400">
              Already have an account?{' '}
              <Link to="/login" className="font-semibold text-purple-400 hover:text-purple-300 transition-colors">
                Sign In
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
