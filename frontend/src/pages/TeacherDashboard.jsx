import { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import {
  FiUsers,
  FiAward,
  FiAlertTriangle,
  FiTrendingDown,
  FiLayers,
  FiActivity,
  FiZap,
  FiInfo,
  FiClock,
} from 'react-icons/fi';
import Navbar from '../components/Navbar';
import LoadingSpinner from '../components/LoadingSpinner';
import { teacherAPI } from '../services/api';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const d = payload[0].payload;
    return (
      <div className="glass rounded-xl p-3 border border-white/10 text-xs shadow-xl space-y-1">
        <p className="font-bold text-white">{d.fullName || d.name}</p>
        <p className="text-cyan-300">Class Average: {d.average}%</p>
        <div className="flex gap-2 text-[10px] pt-1 text-slate-300">
          <span className="text-rose-400">Weak: {d.weak}</span>
          <span className="text-amber-400">Dev: {d.developing}</span>
          <span className="text-emerald-400">Mastered: {d.mastered}</span>
        </div>
      </div>
    );
  }
  return null;
};

export default function TeacherDashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchAnalytics() {
      setLoading(true);
      setError('');
      try {
        const res = await teacherAPI.getAnalytics();
        setAnalytics(res.data);
      } catch (err) {
        console.error('Failed to load teacher analytics:', err);
        if (err.response?.status === 401 || err.response?.status === 403) {
          setError('Authorization required: Please log in with an authorized account to access faculty analytics.');
        } else {
          setError('Failed to fetch class intelligence data from the database.');
        }
      } finally {
        setLoading(false);
      }
    }
    fetchAnalytics();
  }, []);

  // Filter subject charts strictly to subjects with actual recorded student data
  const subjectChartData = (analytics?.subject_analytics || [])
    .filter((s) => s.has_data && s.average_mastery !== null)
    .slice(0, 8)
    .map((s) => ({
      name: s.subject_code,
      fullName: s.subject_name,
      average: Math.round(s.average_mastery),
      weak: s.weak_count,
      developing: s.developing_count,
      mastered: s.mastered_count,
    }));

  const getBarColor = (val) => {
    if (val < 40) return '#f43f5e';
    if (val < 70) return '#f59e0b';
    return '#10b981';
  };

  // Deduplicate and ensure only genuine unique students are rendered
  const uniqueStudents = (analytics?.students || []).filter(
    (st, idx, arr) =>
      st.id &&
      arr.findIndex(
        (o) =>
          o.id === st.id ||
          (o.email && st.email && o.email.trim().toLowerCase() === st.email.trim().toLowerCase())
      ) === idx
  );

  return (
    <div className="min-h-screen bg-navy-900 text-slate-100 flex flex-col selection:bg-purple-500 selection:text-white">
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10 space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass rounded-3xl p-6 sm:p-8 border border-white/10">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-purple-500/20 text-purple-300 border border-purple-500/30 mb-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
              Faculty Cohort Intelligence Hub
            </div>
            <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
              B.Tech CSE Class Analytics
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Live curriculum analytics strictly derived from verified student accounts and real assessment data.
            </p>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center gap-2">
            <FiAlertTriangle className="shrink-0 w-5 h-5 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center">
            <LoadingSpinner />
            <p className="text-slate-400 mt-4 text-sm animate-pulse">Aggregating live cohort telemetry from database...</p>
          </div>
        ) : !analytics?.has_registered_students ? (
          /* EMPTY STATE 1: No registered students yet */
          <div className="glass rounded-3xl p-14 text-center border border-white/10 space-y-4 my-8">
            <div className="w-16 h-16 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center mx-auto text-purple-400">
              <FiUsers className="w-8 h-8" />
            </div>
            <h2 className="text-2xl font-black text-white">No registered students yet.</h2>
            <p className="text-slate-400 text-sm max-w-md mx-auto leading-relaxed">
              Genuine student profiles, subject distribution, and learning performance will dynamically populate here once students register.
            </p>
          </div>
        ) : (
          <>
            {/* Top KPI Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
              <div className="glass rounded-2xl p-5 border border-white/10">
                <div className="flex items-center justify-between text-slate-400 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider">Registered Engineers</span>
                  <FiUsers className="w-5 h-5 text-purple-400" />
                </div>
                <div className="text-3xl font-black text-white">{uniqueStudents.length}</div>
                <p className="text-xs text-slate-400 mt-1">Genuine student accounts</p>
              </div>

              <div className="glass rounded-2xl p-5 border border-white/10">
                <div className="flex items-center justify-between text-slate-400 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider">Class Average Mastery</span>
                  <FiAward className="w-5 h-5 text-cyan-400" />
                </div>
                <div className="text-3xl font-black gradient-text">
                  {analytics.average_class_mastery !== null ? `${analytics.average_class_mastery}%` : 'N/A'}
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  {analytics.assessed_students_count > 0
                    ? `Calculated from ${analytics.assessed_students_count} assessed students`
                    : 'Pending initial assessments'}
                </p>
              </div>

              <div className="glass rounded-2xl p-5 border border-white/10">
                <div className="flex items-center justify-between text-slate-400 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider">Intervention Watchlist</span>
                  <FiAlertTriangle className="w-5 h-5 text-rose-400" />
                </div>
                <div className="text-3xl font-black text-rose-400">
                  {analytics.struggling_students?.length ?? 0}
                </div>
                <p className="text-xs text-slate-400 mt-1">Assessed students with &lt;40% mastery</p>
              </div>

              <div className="glass rounded-2xl p-5 border border-white/10">
                <div className="flex items-center justify-between text-slate-400 mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider">B.Tech Subjects Monitored</span>
                  <FiLayers className="w-5 h-5 text-emerald-400" />
                </div>
                <div className="text-3xl font-black text-emerald-400">
                  {analytics.subject_analytics?.length ?? 0}
                </div>
                <p className="text-xs text-slate-400 mt-1">Curriculum topics active</p>
              </div>
            </div>

            {/* EMPTY STATE 2: Registered students exist, but no assessment data */}
            {!analytics.has_assessment_data ? (
              <div className="glass rounded-3xl p-10 text-center border border-cyan-500/30 bg-cyan-500/5 space-y-4 my-6">
                <div className="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mx-auto text-cyan-400">
                  <FiClock className="w-7 h-7" />
                </div>
                <h3 className="text-xl font-bold text-white">
                  No assessment data available yet. Student analytics will appear after assessments are completed.
                </h3>
                <p className="text-slate-400 text-xs sm:text-sm max-w-xl mx-auto leading-relaxed">
                  Students have successfully registered and enrolled in B.Tech CSE subjects. Concept mastery curves, difficulty comparisons, and diagnostic scores will dynamically display as soon as students submit tests.
                </p>
              </div>
            ) : (
              <>
                {/* Subject Mastery Bar Chart (Displayed only when genuine assessment data exists) */}
                {subjectChartData.length > 0 && (
                  <div className="glass rounded-2xl p-6 sm:p-7 border border-white/10 space-y-4">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div>
                        <h2 className="text-lg font-bold text-white flex items-center gap-2">
                          <FiActivity className="text-purple-400" /> Core Subject Mastery Comparison
                        </h2>
                        <p className="text-xs text-slate-400">Actual average class performance derived from student assessments</p>
                      </div>
                      <div className="flex items-center gap-4 text-xs font-medium">
                        <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-rose-500" /> &lt;40%</span>
                        <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-500" /> 40-70%</span>
                        <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> &gt;70%</span>
                      </div>
                    </div>

                    <div className="h-64 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={subjectChartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                          <XAxis dataKey="name" stroke="#94a3b8" fontSize={11} tickLine={false} />
                          <YAxis stroke="#94a3b8" domain={[0, 100]} fontSize={11} tickFormatter={(v) => `${v}%`} />
                          <Tooltip content={<CustomTooltip />} />
                          <Bar dataKey="average" radius={[6, 6, 0, 0]}>
                            {subjectChartData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={getBarColor(entry.average)} />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}

                {/* Critical Intervention Watchlist & Difficult Concepts */}
                <div className="grid lg:grid-cols-2 gap-6">
                  {/* Struggling Students */}
                  <div className="glass rounded-2xl p-6 border border-white/10 space-y-4">
                    <div className="flex items-center justify-between">
                      <h2 className="text-lg font-bold text-white flex items-center gap-2">
                        <FiAlertTriangle className="text-rose-400" /> Critical Intervention Watchlist
                      </h2>
                      <span className="text-xs text-rose-400 font-semibold">Assessed &lt; 40%</span>
                    </div>

                    {!analytics.struggling_students || analytics.struggling_students.length === 0 ? (
                      <p className="text-xs text-slate-400 py-4">No assessed students currently requiring urgent intervention.</p>
                    ) : (
                      <div className="space-y-2.5">
                        {analytics.struggling_students.map((s) => (
                          <div key={s.id} className="p-3.5 rounded-xl bg-navy-950/60 border border-white/5 flex items-center justify-between text-xs">
                            <div>
                              <p className="font-bold text-white">{s.name}</p>
                              <p className="text-slate-400 text-[11px]">{s.email}</p>
                            </div>
                            <div className="text-right">
                              <span className="text-sm font-bold text-rose-400">{Math.round(s.overall_mastery)}%</span>
                              <span className="block text-[10px] text-slate-400">{s.level} Track</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Most Difficult Concepts */}
                  <div className="glass rounded-2xl p-6 border border-white/10 space-y-4">
                    <div className="flex items-center justify-between">
                      <h2 className="text-lg font-bold text-white flex items-center gap-2">
                        <FiTrendingDown className="text-amber-400" /> Lowest Concept Masteries
                      </h2>
                      <span className="text-xs text-slate-400">Class-wide gaps</span>
                    </div>

                    {!analytics.most_difficult_concepts || analytics.most_difficult_concepts.length === 0 ? (
                      <p className="text-xs text-slate-400 py-4">No concept difficulty telemetry recorded yet.</p>
                    ) : (
                      <div className="space-y-2.5">
                        {analytics.most_difficult_concepts.slice(0, 5).map((c) => (
                          <div key={c.concept_id} className="p-3.5 rounded-xl bg-navy-950/60 border border-white/5 flex items-center justify-between text-xs">
                            <div>
                              <p className="font-bold text-white">{c.concept_name}</p>
                              <p className="text-[11px] text-purple-300 font-mono">{c.subject_name}</p>
                            </div>
                            <div className="text-right">
                              <span className="text-sm font-bold text-amber-400">{c.average_mastery}%</span>
                              <span className="block text-[10px] text-slate-400">{c.students_weak} students weak</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </>
            )}

            {/* Genuine Registered Student Roster */}
            <div className="glass rounded-2xl p-6 border border-white/10 space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <FiUsers className="text-purple-400" /> Registered Student Roster
                </h2>
                <span className="text-xs text-slate-400">{uniqueStudents.length} Total Enrolled</span>
              </div>

              {uniqueStudents.length === 0 ? (
                <div className="py-8 text-center text-slate-400 text-xs sm:text-sm">
                  <FiUsers className="w-8 h-8 mx-auto mb-2 opacity-40 text-purple-400" />
                  <p className="font-semibold text-slate-300">No registered students yet.</p>
                  <p className="text-[11px] text-slate-500 mt-1">Genuine student profiles will dynamically populate here once students register.</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-300">
                    <thead className="text-[11px] uppercase tracking-wider text-slate-400 border-b border-white/10">
                      <tr>
                        <th className="py-2.5 px-3">Student Name</th>
                        <th className="py-2.5 px-3">Email</th>
                        <th className="py-2.5 px-3">Level</th>
                        <th className="py-2.5 px-3">Enrolled Subjects</th>
                        <th className="py-2.5 px-3 text-right">Mastery Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                      {uniqueStudents.map((st) => (
                        <tr key={st.id} className="hover:bg-white/[0.02]">
                          <td className="py-3 px-3 font-semibold text-white">{st.name}</td>
                          <td className="py-3 px-3 font-mono text-slate-400">{st.email}</td>
                          <td className="py-3 px-3">
                            <span className="px-2 py-0.5 rounded-full bg-white/5 text-[10px] font-medium text-purple-300 border border-purple-500/20">
                              {st.level}
                            </span>
                          </td>
                          <td className="py-3 px-3 text-slate-300">
                            {(st.enrolled_subjects || []).slice(0, 3).join(', ')}
                            {(st.enrolled_subjects || []).length > 3 && ` +${st.enrolled_subjects.length - 3} more`}
                          </td>
                          <td className="py-3 px-3 text-right">
                            {st.has_assessed && st.overall_mastery !== null ? (
                              <span className={`font-bold ${st.overall_mastery >= 70 ? 'text-emerald-400' : st.overall_mastery >= 40 ? 'text-amber-400' : 'text-rose-400'}`}>
                                {st.overall_mastery}%
                              </span>
                            ) : (
                              <span className="text-slate-500 italic">Pending Assessment</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* EMPTY STATE 3: Misconceptions Feed or 'No learning activity recorded yet.' */}
            <div className="glass rounded-2xl p-6 border border-white/10 space-y-4">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <FiZap className="text-purple-400" /> Diagnosed Programming Misconceptions Feed
              </h2>

              {!analytics.has_learning_activity || !analytics.recent_misconceptions || analytics.recent_misconceptions.length === 0 ? (
                <div className="p-8 text-center text-slate-400 text-xs sm:text-sm">
                  <FiInfo className="w-6 h-6 mx-auto mb-2 opacity-50" />
                  <p className="font-semibold text-slate-300">No learning activity recorded yet.</p>
                  <p className="text-[11px] text-slate-500 mt-1">Diagnosed coding misconceptions will appear here in real time as students complete questions.</p>
                </div>
              ) : (
                <div className="grid sm:grid-cols-2 gap-3">
                  {analytics.recent_misconceptions.map((m) => (
                    <div key={m.id} className="p-3.5 rounded-xl bg-navy-950/60 border border-purple-500/20 text-xs space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-purple-300 font-mono">{m.concept_name}</span>
                        <span className="text-[10px] text-slate-500">
                          {new Date(m.detected_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                      <p className="text-slate-200 text-xs font-medium">{m.description}</p>
                      <p className="text-[10px] text-slate-400">
                        Identified in: <span className="text-purple-300 font-semibold">{m.student_name}</span> ({m.student_email})
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </main>
    </div>
  );
}
