import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiArrowRight, FiAlertTriangle, FiAward, FiLayers } from 'react-icons/fi';
import Navbar from '../components/Navbar';
import QuestionCard from '../components/QuestionCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { assessmentAPI, subjectsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

function CountUp({ end, duration = 1200 }) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    let start = 0;
    const step = end / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= end) {
        setValue(end);
        clearInterval(timer);
      } else {
        setValue(Math.floor(start));
      }
    }, 16);
    return () => clearInterval(timer);
  }, [end, duration]);
  return <span>{value}</span>;
}

export default function DiagnosticAssessment() {
  const { studentId } = useAuth();
  const navigate = useNavigate();

  const [subjects, setSubjects] = useState([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState(null);
  const [subjectName, setSubjectName] = useState('B.Tech CSE Core');
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState({});
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [results, setResults] = useState(null);

  // Load available enrolled subjects
  useEffect(() => {
    async function loadSubjects() {
      try {
        const res = await subjectsAPI.list();
        const subs = res.data || [];
        setSubjects(subs);
        if (subs.length > 0) {
          // Default to first enrolled subject or first subject
          const firstSub = subs[0];
          setSelectedSubjectId(firstSub.id);
          setSubjectName(firstSub.name);
        }
      } catch (err) {
        console.error('Failed to load subjects', err);
      }
    }
    loadSubjects();
  }, []);

  // Load questions when subject changes
  useEffect(() => {
    async function loadQuestions() {
      if (!selectedSubjectId && !studentId) return;
      setLoading(true);
      setError('');
      try {
        const res = await assessmentAPI.getQuestions(studentId, selectedSubjectId);
        const data = res.data || {};
        const qs = data.questions || [];
        setQuestions(qs);
        if (data.subject_name) setSubjectName(data.subject_name);
        setCurrentIdx(0);
        setAnswers({});
        setSelectedAnswer(null);
        setResults(null);
      } catch (err) {
        const msg = err.response?.data?.detail || err.message || 'Failed to load diagnostic questions.';
        setError(msg);
      } finally {
        setLoading(false);
      }
    }
    loadQuestions();
  }, [studentId, selectedSubjectId]);

  const currentQ = questions[currentIdx];
  const isLast = currentIdx === questions.length - 1;
  const progress = questions.length > 0 ? ((currentIdx + 1) / questions.length) * 100 : 0;

  function handleSelectAnswer(option) {
    setSelectedAnswer(option);
  }

  function handleNext() {
    if (!selectedAnswer) return;
    const qKey = currentQ.id || currentIdx;
    const newAnswers = { ...answers, [qKey]: selectedAnswer };
    setAnswers(newAnswers);
    setSelectedAnswer(null);

    if (isLast) {
      submitAssessment(newAnswers);
    } else {
      setCurrentIdx((i) => i + 1);
    }
  }

  async function submitAssessment(finalAnswers) {
    setSubmitting(true);
    setError('');
    try {
      const payloadAnswers = Object.entries(finalAnswers).map(([qid, ans]) => ({
        question_id: parseInt(qid, 10),
        selected_answer: ans,
      }));

      const res = await assessmentAPI.submit({
        student_id: studentId,
        subject_id: selectedSubjectId,
        answers: payloadAnswers,
      });

      setResults(res.data);
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to submit assessment.';
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-navy-900 text-slate-100 flex flex-col selection:bg-purple-500 selection:text-white">
      <Navbar />

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10">
        {results ? (
          /* Results View */
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass rounded-3xl p-8 sm:p-10 border border-white/10 shadow-2xl space-y-8 text-center"
          >
            <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center mx-auto shadow-xl shadow-purple-500/25">
              <FiAward className="w-10 h-10 text-white" />
            </div>

            <div>
              <span className="text-xs px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 font-semibold border border-cyan-500/30">
                Diagnostic Complete: {subjectName}
              </span>
              <h1 className="text-3xl sm:text-4xl font-black text-white mt-3">Assessment Results</h1>
              <div className="text-6xl font-black gradient-text my-4">
                <CountUp end={Math.round(results.score_percentage)} />%
              </div>
              <p className="text-slate-300 text-sm">
                You answered {results.correct_answers} of {results.total_questions} questions correctly.
              </p>
            </div>

            {/* Initialized Concept Mastery Matrix */}
            <div className="text-left space-y-3 pt-4 border-t border-white/10">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                Concept Mastery Initialized:
              </h3>
              <div className="grid sm:grid-cols-2 gap-3">
                {Object.entries(results.mastery_initialized || {}).map(([conceptName, score]) => (
                  <div key={conceptName} className="p-3 rounded-xl bg-navy-950/60 border border-white/5 flex items-center justify-between text-xs">
                    <span className="text-slate-200 font-medium">{conceptName}</span>
                    <span className={`font-bold ${score >= 70 ? 'text-emerald-400' : score >= 40 ? 'text-amber-400' : 'text-rose-400'}`}>
                      {score}%
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendations */}
            {results.recommendations && results.recommendations.length > 0 && (
              <div className="text-left p-4 rounded-xl bg-purple-500/10 border border-purple-500/20 space-y-1.5 text-xs text-purple-200">
                <p className="font-bold uppercase tracking-wider text-purple-300">🎯 Next Learning Path:</p>
                {results.recommendations.map((rec, i) => (
                  <p key={i} className="flex items-center gap-1.5">
                    <span>•</span> {rec}
                  </p>
                ))}
              </div>
            )}

            <div className="flex flex-wrap justify-center gap-4 pt-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="px-6 py-3 rounded-xl font-bold text-sm bg-white/10 hover:bg-white/20 text-white transition-all"
              >
                Go to Dashboard
              </button>
              <button
                onClick={() => navigate('/learn')}
                className="px-7 py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-500 via-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-500/25 hover:opacity-95 transition-all flex items-center gap-2"
              >
                <span>Start Adaptive Practice</span>
                <FiArrowRight className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        ) : (
          /* Question View */
          <div className="space-y-6">
            {/* Subject Selector Bar */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass rounded-2xl p-4 sm:p-5 border border-white/10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-300 flex items-center justify-center font-bold">
                  <FiLayers className="w-5 h-5" />
                </div>
                <div>
                  <h1 className="text-lg font-bold text-white">Diagnostic Assessment</h1>
                  <p className="text-xs text-slate-400">Targeting Subject: {subjectName}</p>
                </div>
              </div>

              {/* Subject Switcher dropdown */}
              <div className="flex items-center gap-2">
                <label className="text-xs text-slate-400">Subject:</label>
                <select
                  value={selectedSubjectId || ''}
                  onChange={(e) => setSelectedSubjectId(parseInt(e.target.value, 10))}
                  className="bg-navy-950 border border-white/10 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-purple-500"
                >
                  {subjects.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.code} - {s.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {error && (
              <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center gap-2">
                <FiAlertTriangle className="w-5 h-5 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {loading ? (
              <div className="py-20 flex flex-col items-center justify-center">
                <LoadingSpinner />
                <p className="text-slate-400 mt-4 text-sm animate-pulse">Loading B.Tech CSE diagnostic questions...</p>
              </div>
            ) : questions.length === 0 ? (
              <div className="glass rounded-2xl p-8 text-center space-y-4">
                <p className="text-slate-300 text-sm">No diagnostic questions found for this subject.</p>
                <button
                  onClick={() => setSelectedSubjectId(subjects[0]?.id)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold bg-purple-500 text-white"
                >
                  Switch Subject
                </button>
              </div>
            ) : (
              <>
                {/* Progress bar */}
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Question {currentIdx + 1} of {questions.length}</span>
                    <span className="font-mono">{Math.round(progress)}% Completed</span>
                  </div>
                  <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-purple-500 to-cyan-500"
                      initial={{ width: 0 }}
                      animate={{ width: `${progress}%` }}
                      transition={{ duration: 0.3 }}
                    />
                  </div>
                </div>

                {/* Question Card with code snippet support */}
                <QuestionCard
                  question={currentQ}
                  selectedAnswer={selectedAnswer}
                  onSelectAnswer={handleSelectAnswer}
                  disabled={submitting}
                />

                {/* Action Bar */}
                <div className="flex items-center justify-between pt-4">
                  <span className="text-xs text-slate-400">
                    {selectedAnswer ? 'Option selected. Click Next to confirm.' : 'Select an option to proceed.'}
                  </span>
                  <button
                    onClick={handleNext}
                    disabled={!selectedAnswer || submitting}
                    className="px-7 py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-500 via-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-500/25 hover:opacity-95 transition-all flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    <span>{isLast ? (submitting ? 'Submitting...' : 'Submit Assessment') : 'Next Question'}</span>
                    <FiArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
