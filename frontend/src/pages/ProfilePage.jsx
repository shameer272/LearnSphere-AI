import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiUser, FiAward, FiCheck, FiLayers, FiAlertCircle, FiSave, FiLogOut } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import { subjectsAPI } from '../services/api';
import Navbar from '../components/Navbar';
import LoadingSpinner from '../components/LoadingSpinner';

export default function ProfilePage() {
  const { user, updateProfile, logout } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [learningLevel, setLearningLevel] = useState(user?.learning_level || 'Intermediate');
  const [availableSubjects, setAvailableSubjects] = useState([]);
  const [selectedSubjectIds, setSelectedSubjectIds] = useState([]);
  const [loadingSubjects, setLoadingSubjects] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadData() {
      try {
        const res = await subjectsAPI.list();
        setAvailableSubjects(res.data || []);
        if (user?.enrolled_subjects) {
          setSelectedSubjectIds(user.enrolled_subjects.map((s) => s.id));
        }
      } catch {
        console.error('Failed to load subjects:', err);
      } finally {
        setLoadingSubjects(false);
      }
    }
    loadData();
  }, [user]);

  const toggleSubject = (id) => {
    setSelectedSubjectIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleSave = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Name cannot be empty.');
      return;
    }
    if (selectedSubjectIds.length === 0) {
      setError('Please select at least one enrolled subject.');
      return;
    }

    setSaving(true);
    setError('');
    setMessage('');

    try {
      await updateProfile({
        name: name.trim(),
        learning_level: learningLevel,
        selected_subject_ids: selectedSubjectIds,
      });
      setMessage('Profile and subject enrollments updated successfully!');
    } catch {
      setError('Failed to update profile. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-navy-900 text-slate-100 flex flex-col selection:bg-purple-500 selection:text-white">
      <Navbar />

      <main className="flex-1 max-w-5xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-black text-white tracking-tight">Student Profile</h1>
            <p className="text-slate-400 text-sm mt-1">Manage your B.Tech CSE learning settings and focus tracks</p>
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium text-rose-300 hover:text-white bg-rose-500/10 hover:bg-rose-500/20 transition-all border border-rose-500/20"
          >
            <FiLogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </button>
        </div>

        {message && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-sm flex items-center gap-2"
          >
            <FiCheck className="w-5 h-5 flex-shrink-0" />
            <span>{message}</span>
          </motion.div>
        )}

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center gap-2"
          >
            <FiAlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </motion.div>
        )}

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left: Summary Card */}
          <div className="glass rounded-2xl p-6 border border-white/10 h-fit space-y-6">
            <div className="text-center pb-6 border-b border-white/10">
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center mx-auto mb-4 shadow-xl shadow-purple-500/25">
                <FiUser className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-xl font-bold text-white">{user?.name}</h2>
              <p className="text-xs text-purple-300 font-mono mt-1">{user?.email}</p>
              <div className="mt-3 inline-block px-3 py-1 rounded-full text-xs font-semibold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                {user?.learning_level} Tier
              </div>
            </div>

            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between text-slate-400">
                <span>Degree:</span>
                <span className="text-white font-medium">{user?.degree}</span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>Active Streak:</span>
                <span className="text-amber-400 font-bold">{user?.streak_days || 1} Days 🔥</span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>Enrolled Subjects:</span>
                <span className="text-purple-300 font-semibold">{selectedSubjectIds.length} Subjects</span>
              </div>
            </div>
          </div>

          {/* Right: Editable Settings */}
          <div className="lg:col-span-2 glass rounded-2xl p-6 sm:p-8 border border-white/10">
            <form onSubmit={handleSave} className="space-y-6">
              <div>
                <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                  <FiAward className="text-purple-400" /> Academic Information
                </h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                      Student Name
                    </label>
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full px-4 py-3 rounded-xl bg-navy-950/60 border border-white/10 text-white text-sm focus:outline-none focus:border-purple-500 transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                      Target Learning Pace / Difficulty
                    </label>
                    <div className="grid grid-cols-3 gap-3">
                      {['Beginner', 'Intermediate', 'Advanced'].map((lvl) => (
                        <button
                          key={lvl}
                          type="button"
                          onClick={() => setLearningLevel(lvl)}
                          className={`py-2.5 rounded-xl text-xs font-semibold transition-all border ${
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
                </div>
              </div>

              <div className="pt-6 border-t border-white/10">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <FiLayers className="text-cyan-400" /> Enrolled Subjects
                  </h3>
                  <span className="text-xs text-purple-400">{selectedSubjectIds.length} Selected</span>
                </div>

                {loadingSubjects ? (
                  <LoadingSpinner />
                ) : (
                  <div className="max-h-64 overflow-y-auto pr-1 space-y-2 border border-white/10 p-3 rounded-xl bg-navy-950/50 scrollbar-thin">
                    {availableSubjects.map((s) => {
                      const selected = selectedSubjectIds.includes(s.id);
                      return (
                        <div
                          key={s.id}
                          onClick={() => toggleSubject(s.id)}
                          className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs cursor-pointer transition-all border ${
                            selected
                              ? 'bg-purple-500/20 text-white border-purple-500/40 shadow-sm'
                              : 'bg-white/5 text-slate-300 border-transparent hover:bg-white/10'
                          }`}
                        >
                          <div>
                            <span className="font-mono text-[10px] text-purple-300 mr-2 px-1.5 py-0.5 rounded bg-purple-500/20">
                              {s.code}
                            </span>
                            <span className="font-semibold">{s.name}</span>
                            <span className="text-slate-400 text-[10px] ml-2">({s.category})</span>
                          </div>
                          {selected ? (
                            <div className="w-4 h-4 rounded-full bg-cyan-400 flex items-center justify-center text-navy-950">
                              <FiCheck className="w-3 h-3 stroke-[3]" />
                            </div>
                          ) : (
                            <div className="w-4 h-4 rounded-full border border-slate-500" />
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-white/10 flex justify-end">
                <button
                  type="submit"
                  disabled={saving}
                  className="px-6 py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-500 via-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-500/25 hover:opacity-95 transition-all flex items-center gap-2 disabled:opacity-50"
                >
                  <FiSave className="w-4 h-4" />
                  <span>{saving ? 'Saving Changes...' : 'Save Settings'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
