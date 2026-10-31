import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import {
  FiTarget,
  FiAward,
  FiZap,
  FiCheckCircle,
  FiAlertTriangle,
  FiArrowRight,
  FiCalendar,
  FiLayers,
  FiCode,
  FiActivity,
} from 'react-icons/fi';
import Navbar from '../components/Navbar';
import MasteryBar from '../components/MasteryBar';
import LoadingSpinner from '../components/LoadingSpinner';
import { studentsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { getTimeOfDay } from '../utils/helpers';

export default function Dashboard() {
  const { user, studentId } = useAuth();
  const location = useLocation();
  const accessDenied = location.state?.error;
  const [data, setData] = useState(null);
  const [selectedSubjectId, setSelectedSubjectId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadDashboard() {
      if (!studentId) return;
      setLoading(true);
      setError('');
      try {
        const res = await studentsAPI.getDashboard(studentId, selectedSubjectId);
        setData(res.data);
      } catch (err) {
        const msg = err.response?.data?.detail || err.message || 'Failed to load dashboard.';
        setError(msg);
      } finally {
        setLoading(false);
      }
    }
    loadDashboard();
  }, [studentId, selectedSubjectId]);

  const timeOfDay = getTimeOfDay();
  const student = data?.student || user || {};
  const overallMastery = data?.overall_mastery ?? 0;
  const subjectMasteries = data?.subject_masteries || [];
  const weakConcepts = data?.concepts_needing_attention || [];
  const upcomingRevisions = data?.upcoming_revisions || [];
  const recentAssessments = data?.recent_assessments || [];
  const weeklyProgress = data?.weekly_progress || [];
  const recommendation = data?.recommended_next_activity;

  return (
    <div className="min-h-screen bg-navy-900 text-slate-100 flex flex-col selection:bg-purple-500 selection:text-white">
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Welcome Banner */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass rounded-3xl p-6 sm:p-8 border border-white/10 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-bl from-purple-500/10 via-cyan-500/10 to-transparent rounded-full blur-3xl pointer-events-none" />
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs px-2.5 py-1 rounded-full bg-purple-500/20 text-purple-300 font-semibold border border-purple-500/30">
                {student?.degree || 'B.Tech Computer Science & Engineering'}
              </span>
              <span className="text-xs px-2.5 py-1 rounded-full bg-cyan-500/20 text-cyan-300 font-semibold border border-cyan-500/30">
                {student?.learning_level || 'Intermediate'} Track
              </span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-black text-white tracking-tight">
              Good {timeOfDay}, {student?.name || 'Engineer'} 👋
            </h1>
            <p className="text-slate-300 text-sm sm:text-base mt-1.5 max-w-2xl">
              Welcome to your adaptive learning intelligence dashboard. Here is your current knowledge breakdown and retention schedule.
            </p>
          </div>

          <div className="flex items-center gap-3 relative z-10">
            <Link
              to="/learn"
              className="flex items-center gap-2 px-6 py-3.5 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-500 via-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-500/25 hover:opacity-95 transition-all"
            >
              <FiZap className="w-4 h-4" />
              <span>Continue Adaptive Learning</span>
            </Link>
          </div>
        </div>

        {accessDenied && (
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-sm flex items-center gap-2">
            <FiAlertTriangle className="w-5 h-5 flex-shrink-0 text-amber-400" />
            <span className="font-medium">{accessDenied}</span>
          </div>
        )}

        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center gap-2">
            <FiAlertTriangle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {loading ? (
          <div className="py-20 flex flex-col items-center justify-center">
            <LoadingSpinner />
            <p className="text-slate-400 mt-4 text-sm animate-pulse">Computing cognitive mastery metrics...</p>
          </div>
        ) : (
          <>
            {/* Top KPI Metrics */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
              <div className="glass rounded-2xl p-5 border border-white/10">
                <div className="flex items-center justify-between text-slate-400 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider">Overall Mastery</span>
                  <FiAward className="w-5 h-5 text-purple-400" />
                </div>
                <div className="text-3xl font-black gradient-text">{overallMastery}%</div>
                <p className="text-xs text-slate-400 mt-1">Across enrolled B.Tech units</p>
              </div>

              <div className="glass rounded-2xl p-5 border border-white/10">
                <div className="flex items-center justify-between text-slate-400 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider">Enrolled Subjects</span>
                  <FiLayers className="w-5 h-5 text-cyan-400" />
                </div>
                <div className="text-3xl font-black text-white">{subjectMasteries.length}</div>
                <p className="text-xs text-slate-400 mt-1">Active focus curricula</p>
              </div>

              <div className="glass rounded-2xl p-5 border border-white/10">
                <div className="flex items-center justify-between text-slate-400 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider">Mastered Concepts</span>
                  <FiCheckCircle className="w-5 h-5 text-emerald-400" />
                </div>
                <div className="text-3xl font-black text-emerald-400">{data?.concepts_mastered ?? 0}</div>
                <p className="text-xs text-slate-400 mt-1">&gt; 70% threshold reached</p>
              </div>

              <div className="glass rounded-2xl p-5 border border-white/10">
                <div className="flex items-center justify-between text-slate-400 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider">Learning Streak</span>
                  <FiZap className="w-5 h-5 text-amber-400" />
                </div>
                <div className="text-3xl font-black text-amber-400">{student?.streak_days || 1} Days</div>
                <p className="text-xs text-slate-400 mt-1">Consistent daily progress 🔥</p>
              </div>
            </div>

            {/* AI Recommendation Banner */}
            {recommendation && (
              <motion.div
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-2xl p-5 border border-purple-500/30 bg-purple-500/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
              >
                <div className="flex items-start sm:items-center gap-3.5">
                  <div className="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-300 flex items-center justify-center flex-shrink-0">
                    <FiTarget className="w-5 h-5 text-purple-400" />
                  </div>
                  <div>
                    <span className="text-xs font-bold text-purple-400 uppercase tracking-wider">🎯 AI Recommendation</span>
                    <h3 className="text-base font-bold text-white mt-0.5" style={{ color: '#FFFFFF' }}>{recommendation.action_text}</h3>
                    <p className="text-xs text-[#CBD5E1] mt-0.5 leading-relaxed" style={{ color: '#CBD5E1' }}>
                      Current mastery is {recommendation.current_mastery}%. Reinforcing this concept will unblock higher-order prerequisites.
                    </p>
                  </div>
                </div>

                <Link
                  to={`/learn?concept_id=${recommendation.concept_id}`}
                  className="px-5 py-2.5 rounded-xl text-xs bg-gradient-to-r from-purple-600 to-cyan-500 text-white font-semibold hover:brightness-110 shadow-md shadow-purple-500/20 transition-all flex items-center gap-1.5 whitespace-nowrap self-start sm:self-auto focus:outline-none focus:ring-2 focus:ring-purple-400"
                  style={{ color: '#FFFFFF' }}
                >
                  <span className="text-white font-semibold" style={{ color: '#FFFFFF' }}>Practice Concept</span>
                  <FiArrowRight className="w-3.5 h-3.5 text-white" />
                </Link>
              </motion.div>
            )}

            {/* Subject Filter Tabs */}
            <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
              <button
                onClick={() => setSelectedSubjectId(null)}
                className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all border ${
                  selectedSubjectId === null
                    ? 'bg-purple-500 text-white border-purple-400 shadow-md shadow-purple-500/25'
                    : 'glass text-slate-300 hover:text-white border-white/10'
                }`}
              >
                All Enrolled Subjects ({subjectMasteries.length})
              </button>
              {subjectMasteries.map((s) => (
                <button
                  key={s.subject_id}
                  onClick={() => setSelectedSubjectId(s.subject_id)}
                  className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all border ${
                    selectedSubjectId === s.subject_id
                      ? 'bg-purple-500 text-white border-purple-400 shadow-md shadow-purple-500/25'
                      : 'glass text-slate-300 hover:text-white border-white/10'
                  }`}
                >
                  <span className="font-mono mr-1 text-[10px] opacity-75">{s.subject_code}</span>
                  {s.subject_name} ({s.average_mastery}%)
                </button>
              ))}
            </div>

            {/* Main Content Grid */}
            <div className="grid lg:grid-cols-3 gap-8">
              {/* Left 2 Columns: Subject Breakdown & Concept Mastery */}
              <div className="lg:col-span-2 space-y-8">
                {/* Subject-Wise Progress Cards */}
                <div className="glass rounded-2xl p-6 border border-white/10">
                  <div className="flex items-center justify-between mb-5">
                    <div>
                      <h2 className="text-lg font-bold text-white flex items-center gap-2">
                        <FiCode className="text-purple-400" /> B.Tech CSE Subject Progress
                      </h2>
                      <p className="text-xs text-slate-400 mt-0.5">Continuous concept-level score distribution</p>
                    </div>
                    <Link to="/mastery" className="text-xs text-purple-400 hover:text-purple-300 flex items-center gap-1">
                      View Full Matrix <FiArrowRight />
                    </Link>
                  </div>

                  <div className="grid sm:grid-cols-2 gap-4">
                    {subjectMasteries.map((sm) => (
                      <div
                        key={sm.subject_id}
                        className="p-4 rounded-xl bg-navy-950/50 border border-white/5 hover:border-purple-500/30 transition-all flex flex-col justify-between"
                      >
                        <div>
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-mono text-[10px] text-purple-300 bg-purple-500/20 px-2 py-0.5 rounded">
                              {sm.subject_code}
                            </span>
                            <span className="text-xs font-bold text-white">{sm.average_mastery}%</span>
                          </div>
                          <h3 className="font-bold text-sm text-white">{sm.subject_name}</h3>
                          <p className="text-xs text-slate-400 mb-3">{sm.category}</p>
                          <MasteryBar score={sm.average_mastery} showLabel={false} />
                        </div>

                        <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400">
                          <span>{sm.concepts_count} Concepts</span>
                          <Link
                            to={`/learn?subject_id=${sm.subject_id}`}
                            className="text-purple-400 hover:text-purple-300 font-medium flex items-center gap-1"
                          >
                            Practice <FiArrowRight className="w-3 h-3" />
                          </Link>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Weekly Learning Activity Chart */}
                <div className="glass rounded-2xl p-6 border border-white/10">
                  <div className="flex items-center justify-between mb-6">
                    <div>
                      <h2 className="text-lg font-bold text-white flex items-center gap-2">
                        <FiActivity className="text-cyan-400" /> Weekly Learning Activity
                      </h2>
                      <p className="text-xs text-slate-400 mt-0.5">Questions answered over the last 7 days</p>
                    </div>
                  </div>

                  <div className="h-56 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={weeklyProgress} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <defs>
                          <linearGradient id="colorQuestions" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4} />
                            <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                        <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} tickLine={false} />
                        <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#0f172a',
                            borderColor: '#334155',
                            borderRadius: '0.75rem',
                            fontSize: '12px',
                          }}
                        />
                        <Area
                          type="monotone"
                          dataKey="questions_answered"
                          stroke="#8b5cf6"
                          strokeWidth={2}
                          fillOpacity={1}
                          fill="url(#colorQuestions)"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              {/* Right Column: Weak Concepts, Revisions & Recent Assessments */}
              <div className="space-y-6">
                {/* Weak Concepts Card */}
                <div className="glass rounded-2xl p-6 border border-white/10">
                  <h2 className="text-lg font-bold text-white flex items-center gap-2 mb-1">
                    <FiAlertTriangle className="text-rose-400" /> Knowledge Gaps (&lt; 40%)
                  </h2>
                  <p className="text-xs text-slate-400 mb-4">Targeted by adaptive difficulty engine</p>

                  {weakConcepts.length === 0 ? (
                    <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
                      <FiCheckCircle className="w-4 h-4 flex-shrink-0" />
                      <span>All evaluated concepts are above 40% mastery! Great job.</span>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {weakConcepts.slice(0, 4).map((c) => (
                        <div key={c.concept_id} className="p-3 rounded-xl bg-navy-950/60 border border-white/5 space-y-2">
                          <div className="flex items-center justify-between text-xs">
                            <span className="font-semibold text-slate-200">{c.concept_name}</span>
                            <span className="text-rose-400 font-bold">{c.mastery_score}%</span>
                          </div>
                          <MasteryBar score={c.mastery_score} showLabel={false} />
                          <div className="flex items-center justify-between pt-1 text-[11px] text-slate-400">
                            <span>{c.subject_name}</span>
                            <Link
                              to={`/learn?concept_id=${c.concept_id}`}
                              className="text-purple-400 hover:text-purple-300 font-medium"
                            >
                              Strengthen →
                            </Link>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Upcoming Revisions */}
                <div className="glass rounded-2xl p-6 border border-white/10">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold text-white flex items-center gap-2">
                      <FiCalendar className="text-amber-400" /> Spaced Revisions
                    </h2>
                    <Link to="/revisions" className="text-xs text-purple-400 hover:text-purple-300">
                      View All
                    </Link>
                  </div>

                  {upcomingRevisions.length === 0 ? (
                    <p className="text-xs text-slate-400 py-3">No pending retention sessions due.</p>
                  ) : (
                    <div className="space-y-2.5">
                      {upcomingRevisions.slice(0, 3).map((r) => (
                        <div key={r.id} className="p-3 rounded-xl bg-navy-950/60 border border-white/5 text-xs">
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-semibold text-white">{r.concept_name}</span>
                            <span
                              className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                                r.priority === 'high'
                                  ? 'bg-rose-500/20 text-rose-300'
                                  : 'bg-amber-500/20 text-amber-300'
                              }`}
                            >
                              {r.priority.toUpperCase()}
                            </span>
                          </div>
                          <p className="text-slate-400 text-[11px] leading-relaxed">{r.reason}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Recent Diagnostic Tests */}
                <div className="glass rounded-2xl p-6 border border-white/10">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold text-white flex items-center gap-2">
                      <FiLayers className="text-cyan-400" /> Assessments
                    </h2>
                    <Link to="/assessment" className="text-xs text-purple-400 hover:text-purple-300">
                      Take Test
                    </Link>
                  </div>

                  {recentAssessments.length === 0 ? (
                    <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20 text-center">
                      <p className="text-xs text-slate-300 mb-2">No diagnostic assessments recorded yet.</p>
                      <Link
                        to="/assessment"
                        className="inline-block px-3 py-1.5 rounded-lg text-xs font-semibold bg-purple-500 text-white"
                      >
                        Start Diagnostic Assessment
                      </Link>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {recentAssessments.slice(0, 3).map((a) => (
                        <div key={a.id} className="p-3 rounded-xl bg-navy-950/60 border border-white/5 flex items-center justify-between text-xs">
                          <div>
                            <p className="font-semibold text-white">{a.subject_name}</p>
                            <p className="text-[10px] text-slate-400">{new Date(a.completed_at).toLocaleDateString()}</p>
                          </div>
                          <span className="font-bold text-cyan-300">{a.score_percentage}% Score</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
