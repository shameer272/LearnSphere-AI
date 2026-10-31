import { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FiAlertTriangle, FiSend, FiZap, FiClock, FiCheckCircle, FiXCircle, FiBookOpen } from 'react-icons/fi';
import Navbar from '../components/Navbar';
import QuestionCard from '../components/QuestionCard';
import FeedbackCard from '../components/FeedbackCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { learningAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function LearningWorkspace() {
  const { studentId } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();

  const paramSubjectId = searchParams.get('subject_id') ? parseInt(searchParams.get('subject_id'), 10) : null;
  const paramConceptId = searchParams.get('concept_id') ? parseInt(searchParams.get('concept_id'), 10) : null;

  const [subjects, setSubjects] = useState([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState(paramSubjectId);
  const [question, setQuestion] = useState(null);
  const [loadingQ, setLoadingQ] = useState(true);
  const [error, setError] = useState('');
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [reasoning, setReasoning] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [isCorrect, setIsCorrect] = useState(null);
  const [conceptMastery, setConceptMastery] = useState(null);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  // Fetch only the authenticated student's enrolled subjects
  useEffect(() => {
    async function loadEnrolledSubjects() {
      try {
        const res = await learningAPI.getSubjects(studentId);
        const enrolled = res.data || [];
        setSubjects(enrolled);
        if (!paramSubjectId && !selectedSubjectId && enrolled.length > 0) {
          setSelectedSubjectId(enrolled[0].id);
        }
      } catch (err) {
        console.error('Failed to load enrolled subjects', err);
      }
    }
    if (studentId) {
      loadEnrolledSubjects();
    }
  }, [studentId, paramSubjectId]);

  // Fetch student's recent question history
  const loadHistory = useCallback(async () => {
    if (!studentId) return;
    try {
      const res = await learningAPI.getHistory(studentId, selectedSubjectId || undefined);
      setHistory(res.data || []);
    } catch (err) {
      console.error('Failed to load question history', err);
    }
  }, [studentId, selectedSubjectId]);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const fetchNextQuestion = useCallback(async () => {
    if (!studentId) return;
    setLoadingQ(true);
    setError('');
    setFeedback(null);
    setSelectedAnswer(null);
    setReasoning('');
    setIsCorrect(null);
    setConceptMastery(null);

    try {
      const res = await learningAPI.getNextQuestion(
        studentId,
        selectedSubjectId || undefined,
        paramConceptId || undefined
      );
      setQuestion(res.data);
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to load adaptive question.';
      setError(msg);
    } finally {
      setLoadingQ(false);
    }
  }, [studentId, selectedSubjectId, paramConceptId]);

  useEffect(() => {
    fetchNextQuestion();
  }, [fetchNextQuestion]);

  async function handleSubmit() {
    if (!selectedAnswer || !question || submitting) return;
    setSubmitting(true);
    setError('');

    try {
      const payload = {
        student_id: Number(studentId),
        question_id: question.id || null,
        concept_id: question.concept_id,
        selected_answer: selectedAnswer,
        written_reasoning: reasoning.trim() || null,
        time_taken_seconds: 25,
      };

      const res = await learningAPI.submitAnswer(payload);
      const data = res.data;
      setFeedback(data);
      setIsCorrect(data.is_correct);
      setConceptMastery(data.new_mastery);
      // Refresh question history
      loadHistory();
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to evaluate answer.';
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  }

  const handleSubjectChange = (subjId) => {
    setSelectedSubjectId(subjId || null);
    if (subjId) {
      setSearchParams({ subject_id: subjId.toString() });
    } else {
      setSearchParams({});
    }
  };

  return (
    <div className="min-h-screen bg-navy-900 text-slate-100 flex flex-col selection:bg-purple-500 selection:text-white">
      <Navbar />

      <main className="flex-1 max-w-5xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* Workspace Header & Subject Controls */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass rounded-2xl p-4 sm:p-5 border border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-300 flex items-center justify-center font-bold">
              <FiZap className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white">Adaptive Learning Workspace</h1>
              <p className="text-xs text-slate-400">
                Subject-specific question engine with dynamic difficulty calibration
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2">
              <label className="text-xs text-slate-400 font-medium">Enrolled Subject:</label>
              <select
                value={selectedSubjectId || ''}
                onChange={(e) => handleSubjectChange(e.target.value ? parseInt(e.target.value, 10) : null)}
                className="bg-white text-gray-900 border border-gray-300 rounded-xl px-3 py-1.5 text-xs font-medium focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 cursor-pointer shadow-sm"
                style={{ backgroundColor: '#FFFFFF', color: '#111827' }}
              >
                <option value="" className="bg-white text-gray-900" style={{ backgroundColor: '#FFFFFF', color: '#111827' }}>
                  All Enrolled Subjects
                </option>
                {subjects.map((s) => (
                  <option
                    key={s.id}
                    value={s.id}
                    className="bg-white text-gray-900"
                    style={{ backgroundColor: '#FFFFFF', color: '#111827' }}
                  >
                    {s.code} - {s.name}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={() => setShowHistory(!showHistory)}
              className="px-3 py-1.5 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-xs text-slate-300 flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <FiClock className="w-3.5 h-3.5 text-purple-400" />
              <span>History ({history.length})</span>
            </button>
          </div>
        </div>

        {/* Collapsible Question History Drawer */}
        <AnimatePresence>
          {showHistory && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="glass rounded-2xl p-4 border border-white/10 space-y-3 overflow-hidden"
            >
              <div className="flex items-center justify-between pb-2 border-b border-white/5">
                <span className="text-xs font-bold uppercase tracking-wider text-purple-300 flex items-center gap-1.5">
                  <FiBookOpen className="w-4 h-4 text-cyan-400" /> Recent Question History (Duplicate Excluded)
                </span>
                <span className="text-[11px] text-slate-400">{history.length} attempts recorded</span>
              </div>
              {history.length === 0 ? (
                <p className="text-xs text-slate-400 py-2">No questions attempted yet for this subject.</p>
              ) : (
                <div className="max-h-48 overflow-y-auto space-y-2 pr-1 scrollbar-thin">
                  {history.map((h) => (
                    <div
                      key={h.id}
                      className="flex items-start justify-between gap-3 p-2.5 rounded-xl bg-navy-950/60 border border-white/5 text-xs"
                    >
                      <div className="space-y-0.5">
                        <div className="flex items-center gap-2">
                          {h.is_correct ? (
                            <span className="text-emerald-400 flex items-center gap-1 font-semibold text-[11px]">
                              <FiCheckCircle className="w-3.5 h-3.5" /> Correct
                            </span>
                          ) : (
                            <span className="text-rose-400 flex items-center gap-1 font-semibold text-[11px]">
                              <FiXCircle className="w-3.5 h-3.5" /> Incorrect
                            </span>
                          )}
                          <span className="text-slate-400 text-[10px] font-mono px-1.5 py-0.5 rounded bg-white/5">
                            {h.subject_name} • {h.concept_name}
                          </span>
                        </div>
                        <p className="text-slate-200 line-clamp-1">{h.question_text}</p>
                      </div>
                      <span className="text-[10px] text-slate-400 whitespace-nowrap">
                        {h.answered_at ? new Date(h.answered_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center gap-2">
            <FiAlertTriangle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {loadingQ ? (
          <div className="py-24 flex flex-col items-center justify-center">
            <LoadingSpinner />
            <p className="text-slate-400 mt-4 text-sm animate-pulse">
              Selecting calibrated problem from knowledge graph...
            </p>
          </div>
        ) : question ? (
          <div className="space-y-6">
            {/* Question Card with clear Subject, Topic, Concept, Difficulty badges */}
            <QuestionCard
              question={question}
              selectedAnswer={selectedAnswer}
              onSelectAnswer={(opt) => !feedback && setSelectedAnswer(opt)}
              showResult={feedback !== null}
              correctAnswer={feedback?.correct_answer}
              disabled={submitting || feedback !== null}
            />

            {/* Written Reasoning Area (active before feedback) */}
            {!feedback && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-2xl p-5 border border-white/10 space-y-3"
              >
                <div className="flex items-center justify-between">
                  <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider">
                    Written Reasoning (Optional for Deep Diagnostic)
                  </label>
                  <span className="text-[11px] text-purple-400">
                    Gemini AI inspects your explanation for misconceptions
                  </span>
                </div>
                <textarea
                  value={reasoning}
                  onChange={(e) => setReasoning(e.target.value)}
                  placeholder="Explain why you picked this option (e.g. In Python, mutable default arguments retain mutations across function calls...)"
                  rows={3}
                  className="w-full px-4 py-3 rounded-xl bg-navy-950/70 border border-white/10 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all font-sans leading-relaxed"
                />
                <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
                  <span className="text-xs text-slate-400">
                    {selectedAnswer ? 'Option selected. Submit to receive diagnostic feedback.' : 'Select an option above to submit.'}
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={fetchNextQuestion}
                      disabled={loadingQ}
                      className="px-4 py-3 rounded-xl font-medium text-xs border border-white/20 bg-white/5 hover:bg-white/10 text-slate-300 transition-all cursor-pointer"
                    >
                      Next Question
                    </button>
                    <button
                      type="button"
                      onClick={handleSubmit}
                      disabled={!selectedAnswer || submitting}
                      className="px-7 py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-500 via-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-500/25 hover:opacity-95 transition-all flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
                    >
                      <span>{submitting ? 'Analyzing Reasoning...' : 'Submit Answer'}</span>
                      <FiSend className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Misconception Diagnostic Feedback Card with Next Question button */}
            {feedback && (
              <FeedbackCard
                feedback={feedback}
                isCorrect={isCorrect}
                conceptMastery={conceptMastery}
                conceptName={question.concept_name}
                onNext={fetchNextQuestion}
              />
            )}
          </div>
        ) : (
          <div className="glass rounded-2xl p-12 text-center space-y-4">
            <p className="text-slate-300">All available questions for this subject have been answered or practiced.</p>
            <button
              onClick={() => handleSubjectChange(null)}
              className="px-5 py-2.5 rounded-xl text-xs font-bold bg-purple-500 text-white cursor-pointer"
            >
              Reset Filters
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
