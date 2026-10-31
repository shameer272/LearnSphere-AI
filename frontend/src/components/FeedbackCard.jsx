import { motion } from 'framer-motion';
import MasteryBar from './MasteryBar';
import { FiAlertTriangle, FiCheckCircle, FiXCircle, FiArrowRight, FiCalendar } from 'react-icons/fi';

export default function FeedbackCard({ feedback, isCorrect, conceptMastery, conceptName, onNext }) {
  if (!feedback) return null;

  const detectedMis = feedback.detected_misconception || feedback.misconception;
  const misCategory = feedback.misconception_category;
  const recommendedAction = feedback.recommended_learning_action || feedback.recommended_action;
  const newScore = feedback.new_mastery ?? conceptMastery ?? feedback.updated_mastery ?? 0;
  const prevScore = feedback.previous_mastery;

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      {/* Correct/Incorrect Header */}
      <div
        className={`flex items-center gap-3.5 p-4 rounded-2xl border ${
          isCorrect ? 'bg-emerald-500/15 border-emerald-500/30' : 'bg-rose-500/15 border-rose-500/30'
        }`}
      >
        <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 350 }}>
          {isCorrect ? (
            <FiCheckCircle className="w-8 h-8 text-emerald-400" />
          ) : (
            <FiXCircle className="w-8 h-8 text-rose-400" />
          )}
        </motion.div>
        <div>
          <p className={`font-black text-lg ${isCorrect ? 'text-emerald-400' : 'text-rose-400'}`}>
            {isCorrect ? 'Concept Correctly Applied!' : 'Incorrect Derivation'}
          </p>
          <span className="text-xs bg-purple-500/20 text-purple-300 border border-purple-500/30 px-2.5 py-0.5 rounded-full font-mono">
            {feedback.is_ai_generated ? '✨ Gemini Cognitive Diagnostic' : 'Deterministic Misconception Engine'}
          </span>
        </div>
      </div>

      {/* Misconception Alert if detected */}
      {detectedMis && (
        <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-2xl space-y-1.5">
          <div className="flex items-center gap-2 text-amber-400 font-bold text-xs uppercase tracking-wider">
            <FiAlertTriangle className="w-4 h-4 flex-shrink-0" />
            <span>Diagnosed Programming Misconception</span>
            {misCategory && (
              <span className="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono">
                {misCategory}
              </span>
            )}
          </div>
          <p className="text-sm text-amber-200/90 font-medium leading-relaxed">{detectedMis}</p>
        </div>
      )}

      {/* Reasoning Analysis */}
      {feedback.reasoning_analysis && (
        <div className="glass rounded-2xl p-4 sm:p-5 border border-white/10 space-y-1.5">
          <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Student Reasoning Analysis
          </h4>
          <p className="text-sm text-slate-300 leading-relaxed font-normal">{feedback.reasoning_analysis}</p>
        </div>
      )}

      {/* Concept Explanation */}
      {feedback.explanation && (
        <div className="glass rounded-2xl p-4 sm:p-5 border border-white/10 space-y-1.5">
          <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider">
            Technical Principle &amp; Correct Concept
          </h4>
          <p className="text-sm text-slate-300 leading-relaxed">{feedback.explanation}</p>
        </div>
      )}

      {/* Recommended Learning Action */}
      {recommendedAction && (
        <div className="p-4 rounded-2xl bg-cyan-500/10 border border-cyan-500/25 space-y-1">
          <p className="text-xs font-bold text-cyan-400 uppercase tracking-wider">🎯 Recommended Next Action</p>
          <p className="text-sm text-cyan-200/90 leading-relaxed">{recommendedAction}</p>
        </div>
      )}

      {/* Revision Scheduled Notification */}
      {feedback.revision_scheduled && (
        <div className="p-3 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-between text-xs text-purple-200">
          <div className="flex items-center gap-2">
            <FiCalendar className="w-4 h-4 text-purple-400" />
            <span>Spaced Revision Scheduled ({new Date(feedback.revision_scheduled.scheduled_date).toLocaleDateString()})</span>
          </div>
          <span className="font-semibold uppercase text-purple-300 text-[10px] bg-purple-500/20 px-2 py-0.5 rounded">
            {feedback.revision_scheduled.priority} Priority
          </span>
        </div>
      )}

      {/* Mastery Score Progress */}
      <div className="glass rounded-2xl p-4 sm:p-5 border border-white/10 space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-300 font-medium">
            Concept Mastery: <span className="text-white font-bold">{conceptName || 'Target Concept'}</span>
          </span>
          <span className="font-bold text-white text-sm">
            {prevScore !== undefined && `${prevScore}% → `}
            <span className="text-cyan-300">{Math.round(newScore)}%</span>
          </span>
        </div>
        <MasteryBar score={newScore} showLabel={false} />
      </div>

      {/* Next Button */}
      <motion.button
        onClick={onNext}
        className="w-full py-4 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-500 via-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-500/25 hover:opacity-95 transition-all flex items-center justify-center gap-2"
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.99 }}
      >
        <span>Proceed to Next Adaptive Challenge</span>
        <FiArrowRight className="w-4 h-4" />
      </motion.button>
    </motion.div>
  );
}
