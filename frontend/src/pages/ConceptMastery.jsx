import { useState, useEffect } from 'react';
import { FiArrowRight, FiFilter, FiCpu } from 'react-icons/fi';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import ConceptCard from '../components/ConceptCard';
import KnowledgeGraph from '../components/KnowledgeGraph';
import LoadingSpinner from '../components/LoadingSpinner';
import { studentsAPI, conceptsAPI, subjectsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function ConceptMastery() {
  const { studentId } = useAuth();
  const [concepts, setConcepts] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState('all');
  const [filterTier, setFilterTier] = useState('all'); // all, weak, developing, mastered
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchData() {
      if (!studentId) return;
      setLoading(true);
      setError('');
      try {
        const [dashRes, conceptsRes, subjectsRes] = await Promise.all([
          studentsAPI.getDashboard(studentId),
          conceptsAPI.list(),
          subjectsAPI.list(),
        ]);

        setSubjects(subjectsRes.data || []);

        const masteryByConcept = dashRes.data?.mastery_by_concept || [];
        const conceptMap = {};
        masteryByConcept.forEach((m) => {
          conceptMap[m.concept_id] = m;
        });

        const merged = (conceptsRes.data || []).map((c) => {
          const m = conceptMap[c.id] || {};
          return {
            ...c,
            mastery_score: m.mastery_score ?? 0,
            attempts: m.attempts ?? 0,
            correct: m.correct_count ?? 0,
            current_difficulty: m.current_difficulty ?? 'easy',
          };
        });

        setConcepts(merged);
      } catch (err) {
        console.error('Failed to load concept mastery:', err);
        setError('Failed to load concept mastery data. Please try again.');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [studentId]);

  // Filtering
  const filteredConcepts = concepts.filter((c) => {
    if (selectedSubjectId !== 'all' && c.subject_id !== parseInt(selectedSubjectId, 10)) {
      return false;
    }
    const score = c.mastery_score || 0;
    if (filterTier === 'weak') return score < 40;
    if (filterTier === 'developing') return score >= 40 && score <= 70;
    if (filterTier === 'mastered') return score > 70;
    return true;
  });

  return (
    <div className="min-h-screen bg-navy-900 text-slate-100 flex flex-col selection:bg-purple-500 selection:text-white">
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10 space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-2.5">
              <FiCpu className="text-purple-400" /> B.Tech CSE Concept Mastery Matrix
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Independent concept-level proficiency tracking across Computer Science subjects
            </p>
          </div>
          <Link
            to="/learn"
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold text-xs bg-gradient-to-r from-purple-500 via-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-500/25 self-start sm:self-auto"
          >
            <span>Adaptive Workspace</span>
            <FiArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm">
            {error}
          </div>
        )}

        {loading ? (
          <div className="py-24 flex flex-col items-center justify-center">
            <LoadingSpinner />
            <p className="text-slate-400 mt-4 text-sm animate-pulse">Computing curriculum prerequisite graph...</p>
          </div>
        ) : (
          <>
            {/* Knowledge Graph Component */}
            <KnowledgeGraph concepts={concepts} />

            {/* Filter Toolbar */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass rounded-2xl p-4 border border-white/10">
              <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0 scrollbar-none">
                <span className="text-xs text-slate-400 mr-1 flex items-center gap-1 font-semibold">
                  <FiFilter className="w-3.5 h-3.5" /> Filter:
                </span>
                {[
                  { key: 'all', label: 'All Concepts' },
                  { key: 'weak', label: 'Weak (<40%)' },
                  { key: 'developing', label: 'Developing (40-70%)' },
                  { key: 'mastered', label: 'Mastered (>70%)' },
                ].map((tier) => (
                  <button
                    key={tier.key}
                    onClick={() => setFilterTier(tier.key)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                      filterTier === tier.key
                        ? 'bg-purple-500 text-white shadow-sm'
                        : 'glass text-slate-400 hover:text-white'
                    }`}
                  >
                    {tier.label}
                  </button>
                ))}
              </div>

              {/* Subject Selector */}
              <div className="flex items-center gap-2">
                <label className="text-xs text-slate-400">Subject:</label>
                <select
                  value={selectedSubjectId}
                  onChange={(e) => setSelectedSubjectId(e.target.value)}
                  className="bg-navy-950 border border-white/10 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-purple-500 max-w-[220px]"
                >
                  <option value="all">All Subjects ({subjects.length})</option>
                  {subjects.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.code} - {s.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Concepts Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredConcepts.map((concept) => (
                <ConceptCard key={concept.id} concept={concept} showPractice={true} />
              ))}
            </div>

            {filteredConcepts.length === 0 && (
              <div className="glass rounded-2xl p-12 text-center text-slate-400 text-sm">
                No concepts found matching the selected filters.
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
