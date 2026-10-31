import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiCalendar, FiCheckCircle, FiClock, FiArrowRight, FiCheck } from 'react-icons/fi';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import LoadingSpinner from '../components/LoadingSpinner';
import { revisionsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { getPriorityBadge } from '../utils/helpers';

export default function RevisionCalendar() {
  const { studentId, user } = useAuth();
  const [pendingRevisions, setPendingRevisions] = useState([]);
  const [completedRevisions, setCompletedRevisions] = useState([]);
  const [activeTab, setActiveTab] = useState('upcoming'); // 'upcoming' | 'completed'
  const [loading, setLoading] = useState(true);
  const [completingId, setCompletingId] = useState(null);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const loadData = async () => {
    if (!studentId) return;
    setLoading(true);
    setError('');
    try {
      const res = await revisionsAPI.get(studentId);
      const data = res.data || {};
      setPendingRevisions(data.pending || []);
      setCompletedRevisions(data.completed || []);
    } catch (err) {
      console.error('Failed to load revisions:', err);
      setError('Failed to load revision schedule.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [studentId]);

  const handleMarkComplete = async (revision) => {
    setCompletingId(revision.id);
    try {
      await revisionsAPI.complete({
        revision_id: revision.id,
        student_id: studentId,
      });
      setMessage(`Completed revision for "${revision.concept_name}". Retention reinforced!`);
      setTimeout(() => setMessage(''), 4000);
      await loadData();
    } catch (err) {
      console.error('Failed to complete revision:', err);
      setError('Could not mark revision as complete.');
    } finally {
      setCompletingId(null);
    }
  };

  const currentList = activeTab === 'upcoming' ? pendingRevisions : completedRevisions;

  return (
    <div className="min-h-screen bg-navy-900 text-slate-100 flex flex-col selection:bg-purple-500 selection:text-white">
      <Navbar />

      <main className="flex-1 max-w-5xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10 space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-2.5">
              <FiCalendar className="text-amber-400" /> Spaced Repetition Calendar
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Ebbinghaus memory curve scheduling to reinforce B.Tech CSE concepts
            </p>
          </div>
          <Link
            to="/learn"
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold text-xs bg-gradient-to-r from-purple-500 via-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-500/25 self-start sm:self-auto"
          >
            <span>Practice Weak Topics</span>
            <FiArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {message && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-sm flex items-center gap-2"
          >
            <FiCheckCircle className="w-5 h-5 flex-shrink-0" />
            <span>{message}</span>
          </motion.div>
        )}

        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm">
            {error}
          </div>
        )}

        {/* Tab Switcher */}
        <div className="flex items-center gap-3 border-b border-white/10 pb-3">
          <button
            onClick={() => setActiveTab('upcoming')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'upcoming'
                ? 'bg-purple-500 text-white shadow-md'
                : 'glass text-slate-400 hover:text-white'
            }`}
          >
            Due Retention Sessions ({pendingRevisions.length})
          </button>
          <button
            onClick={() => setActiveTab('completed')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'completed'
                ? 'bg-purple-500 text-white shadow-md'
                : 'glass text-slate-400 hover:text-white'
            }`}
          >
            Completed Sessions ({completedRevisions.length})
          </button>
        </div>

        {loading ? (
          <div className="py-20 flex flex-col items-center justify-center">
            <LoadingSpinner />
            <p className="text-slate-400 mt-4 text-sm animate-pulse">Calculating spaced decay intervals...</p>
          </div>
        ) : currentList.length === 0 ? (
          <div className="glass rounded-2xl p-12 text-center text-slate-400 text-sm space-y-3">
            <FiCheckCircle className="w-10 h-10 text-emerald-400 mx-auto" />
            <p className="text-white font-bold">
              {activeTab === 'upcoming'
                ? 'No pending revision sessions!'
                : 'No completed revisions yet.'}
            </p>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              As you practice in the Adaptive Workspace, the engine continuously calculates forgetting risk and schedules retention prompts.
            </p>
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 gap-4">
            {currentList.map((rev) => (
              <motion.div
                key={rev.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-2xl p-5 border border-white/10 space-y-3 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between gap-2 mb-1.5">
                    <div>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 mr-2">
                        {rev.subject_code || 'CS'}
                      </span>
                      <span className="text-xs text-slate-400">{rev.subject_name}</span>
                    </div>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
                        rev.priority === 'high'
                          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                          : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                      }`}
                    >
                      {rev.priority} Priority
                    </span>
                  </div>
                  <h3 className="font-bold text-white text-base">{rev.concept_name}</h3>
                  <p className="text-xs text-slate-400 mt-1 italic leading-relaxed">"{rev.reason}"</p>
                </div>

                <div className="pt-3 border-t border-white/5 space-y-3">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span className="flex items-center gap-1.5">
                      <FiClock className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Scheduled: {new Date(rev.scheduled_date).toLocaleDateString()}</span>
                    </span>
                    <Link
                      to={`/learn?concept_id=${rev.concept_id}`}
                      className="text-purple-400 hover:text-purple-300 font-medium"
                    >
                      Practice →
                    </Link>
                  </div>

                  {activeTab === 'upcoming' && (
                    <button
                      onClick={() => handleMarkComplete(rev)}
                      disabled={completingId === rev.id}
                      className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30 transition-all disabled:opacity-50"
                    >
                      <FiCheck className="w-4 h-4" />
                      <span>{completingId === rev.id ? 'Marking...' : 'Mark Revision Complete'}</span>
                    </button>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
