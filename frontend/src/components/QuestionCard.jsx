import { motion } from 'framer-motion';
import { getDifficultyColor } from '../utils/helpers';
import { FiCode, FiTerminal } from 'react-icons/fi';

const DEFAULT_KEYS = ['A', 'B', 'C', 'D'];

export default function QuestionCard({
  question,
  selectedAnswer,
  onSelectAnswer,
  showResult = false,
  correctAnswer,
  disabled = false,
}) {
  if (!question) return null;

  // Standardize options into array of { key: 'A', text: '...' }
  let formattedOptions = [];
  if (Array.isArray(question.options)) {
    formattedOptions = question.options.map((opt, idx) => {
      if (typeof opt === 'string') {
        const key = DEFAULT_KEYS[idx] || String.fromCharCode(65 + idx);
        return { key, text: opt };
      }
      if (opt && typeof opt === 'object') {
        return {
          key: opt.key || opt.label || DEFAULT_KEYS[idx],
          text: opt.text || opt.value || JSON.stringify(opt),
        };
      }
      return { key: DEFAULT_KEYS[idx], text: String(opt) };
    });
  } else if (question.options && typeof question.options === 'object') {
    formattedOptions = Object.entries(question.options).map(([key, text]) => ({
      key: key.toUpperCase(),
      text: String(text),
    }));
  }

  const subjectName = question.subject_name || '';
  const conceptName = question.concept_name || question.concept || '';
  const difficulty = question.difficulty || 'medium';
  const difficultyClass = getDifficultyColor(difficulty);
  const isAi = question.is_ai_generated ?? question.ai_generated;
  const questionType = question.question_type || 'mcq';

  return (
    <div className="glass rounded-2xl p-6 sm:p-7 space-y-5 border border-white/10 shadow-xl">
      {/* Badges */}
      <div className="flex flex-wrap items-center gap-2">
        {subjectName && (
          <span className="text-xs px-2.5 py-1 rounded-full font-semibold bg-purple-500/20 text-purple-300 border border-purple-500/30 flex items-center gap-1.5">
            <FiCode className="w-3.5 h-3.5" />
            {subjectName}
          </span>
        )}
        {conceptName && (
          <span className="text-xs px-2.5 py-1 rounded-full font-medium bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">
            {conceptName}
          </span>
        )}
        {difficulty && (
          <span className={`text-xs px-2.5 py-1 rounded-full font-medium capitalize ${difficultyClass}`}>
            {difficulty}
          </span>
        )}
        {questionType && questionType !== 'mcq' && (
          <span className="text-[11px] px-2.5 py-1 rounded-full font-mono bg-white/5 text-slate-300 border border-white/10">
            {questionType.replace('_', ' ').toUpperCase()}
          </span>
        )}
        {isAi && (
          <span className="text-xs px-2.5 py-1 rounded-full font-medium bg-gradient-to-r from-purple-500/20 to-cyan-500/20 text-purple-300 border border-purple-500/30">
            ✨ AI-Calibrated
          </span>
        )}
      </div>

      {/* Question text */}
      <p className="text-base sm:text-lg text-white leading-relaxed font-semibold">
        {question.question_text || question.question}
      </p>

      {/* Code Snippet Box if present */}
      {question.code_snippet && (
        <div className="rounded-xl overflow-hidden border border-white/10 bg-navy-950/80">
          <div className="px-4 py-2 border-b border-white/10 bg-black/40 flex items-center justify-between text-xs text-slate-400 font-mono">
            <span className="flex items-center gap-1.5">
              <FiTerminal className="w-3.5 h-3.5 text-purple-400" />
              <span>Code Snippet</span>
            </span>
            <span className="text-[10px] text-slate-500">B.Tech Engineering Syntax</span>
          </div>
          <pre className="p-4 text-xs sm:text-sm font-mono text-cyan-200 overflow-x-auto leading-relaxed">
            {question.code_snippet}
          </pre>
        </div>
      )}

      {/* Options */}
      <div className="space-y-3 pt-1">
        {formattedOptions.map(({ key, text }) => {
          const isSelected = (selectedAnswer || '').toUpperCase() === key;
          const isCorrect = showResult && (correctAnswer || '').toUpperCase() === key;
          const isWrong = showResult && isSelected && !isCorrect;

          let borderClass = 'border border-white/10 hover:border-purple-500/50 hover:bg-white/5';
          if (isSelected && !showResult) {
            borderClass = 'border-2 border-purple-400 bg-purple-500/20 shadow-md shadow-purple-500/20';
          }
          if (isCorrect) {
            borderClass = 'border-2 border-green-500 bg-green-500/20 text-green-300';
          }
          if (isWrong) {
            borderClass = 'border-2 border-red-500 bg-red-500/20 text-red-300';
          }

          return (
            <motion.button
              key={key}
              type="button"
              className={`w-full flex items-center gap-3.5 px-4 py-3.5 rounded-xl text-left transition-all ${borderClass} ${
                disabled ? 'cursor-default' : 'cursor-pointer'
              }`}
              onClick={() => {
                if (!disabled && onSelectAnswer) {
                  onSelectAnswer(key);
                }
              }}
              whileHover={!disabled ? { scale: 1.005 } : {}}
              whileTap={!disabled ? { scale: 0.995 } : {}}
            >
              <span
                className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold shrink-0 transition-colors ${
                  isSelected && !showResult
                    ? 'bg-purple-500 text-white shadow-sm'
                    : isCorrect
                    ? 'bg-green-500 text-white'
                    : isWrong
                    ? 'bg-red-500 text-white'
                    : 'bg-white/10 text-slate-300'
                }`}
              >
                {key}
              </span>
              <span className={`text-sm font-medium ${isCorrect ? 'text-green-200' : isWrong ? 'text-red-200' : 'text-slate-200'}`}>
                {text}
              </span>
              {isCorrect && <span className="ml-auto text-green-400 font-bold text-xs">✓ Correct</span>}
              {isWrong && <span className="ml-auto text-red-400 font-bold text-xs">✗ Selected</span>}
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}
