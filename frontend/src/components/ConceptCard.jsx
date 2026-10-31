import { motion } from 'framer-motion';
import { getMasteryBadgeClass, getMasteryLabel, getMasteryColor } from '../utils/helpers';
import MasteryBar from './MasteryBar';
import { Link } from 'react-router-dom';
import { FiArrowRight } from 'react-icons/fi';

function getConceptGradient(name) {
  const n = (name || '').toLowerCase();
  if (n.includes('python') || n.includes('object') || n.includes('mutable') || n.includes('dunder')) {
    return 'from-purple-500/20 to-purple-600/10 border-purple-500/30';
  }
  if (n.includes('react') || n.includes('state') || n.includes('hook') || n.includes('dom')) {
    return 'from-cyan-500/20 to-cyan-600/10 border-cyan-500/30';
  }
  if (n.includes('sql') || n.includes('dbms') || n.includes('join') || n.includes('acid') || n.includes('database')) {
    return 'from-emerald-500/20 to-emerald-600/10 border-emerald-500/30';
  }
  if (n.includes('dsa') || n.includes('algorithm') || n.includes('tree') || n.includes('complexity') || n.includes('pointer')) {
    return 'from-amber-500/20 to-amber-600/10 border-amber-500/30';
  }
  if (n.includes('ai') || n.includes('learning') || n.includes('rag') || n.includes('neural') || n.includes('agent')) {
    return 'from-pink-500/20 to-pink-600/10 border-pink-500/30';
  }
  return 'from-blue-500/20 to-blue-600/10 border-blue-500/30';
}

export default function ConceptCard({ concept, showPractice = true }) {
  const mastery = concept.mastery_score ?? concept.mastery ?? 0;
  const colorClass = getConceptGradient(concept.name);

  return (
    <motion.div
      className={`glass rounded-2xl p-5 sm:p-6 border bg-gradient-to-br ${colorClass} hover:border-purple-500/40 transition-all flex flex-col justify-between`}
      whileHover={{ y: -3 }}
    >
      <div>
        <div className="flex items-start justify-between mb-2.5 gap-2">
          <div>
            {concept.subject_name && (
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-slate-300 block w-fit mb-1">
                {concept.subject_name}
              </span>
            )}
            <h3 className="font-bold text-white text-base leading-snug">{concept.name}</h3>
          </div>
          <span className={`text-xs px-2.5 py-0.5 rounded-full font-semibold shrink-0 ${getMasteryBadgeClass(mastery)}`}>
            {getMasteryLabel(mastery)}
          </span>
        </div>

        {concept.description && (
          <p className="text-xs text-slate-300 mb-4 line-clamp-2 leading-relaxed">{concept.description}</p>
        )}
      </div>

      <div>
        <div className="mb-4">
          <div className="flex justify-between text-xs mb-1.5">
            <span className="text-slate-400">Mastery Level</span>
            <span className={`font-bold ${getMasteryColor(mastery)}`}>
              {Math.round(mastery)}%
            </span>
          </div>
          <MasteryBar score={mastery} showLabel={false} />
        </div>

        {(concept.attempts !== undefined || concept.correct !== undefined) && (
          <div className="flex items-center justify-between text-[11px] text-slate-400 mb-4 pt-2 border-t border-white/5">
            <span>Attempts: <strong className="text-white">{concept.attempts || 0}</strong></span>
            <span>Correct: <strong className="text-emerald-400">{concept.correct || concept.correct_count || 0}</strong></span>
            <span className="capitalize">Tier: <strong className="text-cyan-300">{concept.current_difficulty || 'easy'}</strong></span>
          </div>
        )}

        {showPractice && (
          <Link
            to={`/learn?concept_id=${concept.id}`}
            className="flex items-center justify-center gap-1.5 w-full text-center px-4 py-2.5 rounded-xl text-xs font-bold glass text-purple-300 hover:text-white hover:bg-white/10 border border-purple-500/30 transition-all shadow-sm"
          >
            <span>Practice Concept</span>
            <FiArrowRight className="w-3.5 h-3.5" />
          </Link>
        )}
      </div>
    </motion.div>
  );
}
