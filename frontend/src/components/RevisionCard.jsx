import { motion } from 'framer-motion';
import { formatDate, getPriorityBadge } from '../utils/helpers';
import { FiCalendar, FiCheck } from 'react-icons/fi';

export default function RevisionCard({ revision, onComplete, completing = false }) {
  const priority = revision.priority || 'low';
  const badgeClass = getPriorityBadge(priority);
  const dateStr = formatDate(revision.scheduled_date);

  return (
    <motion.div
      className="glass rounded-xl p-5 space-y-3"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-start justify-between gap-3">
        <h3 className="font-semibold text-white">{revision.concept_name || revision.concept}</h3>
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium whitespace-nowrap capitalize ${badgeClass}`}>
          {priority} priority
        </span>
      </div>

      <div className="flex items-center gap-2 text-sm text-slate-400">
        <FiCalendar className="w-4 h-4 text-cyan-400" />
        <span>{dateStr}</span>
      </div>

      {revision.reason && (
        <p className="text-sm text-slate-400 italic">"{revision.reason}"</p>
      )}

      {onComplete && (
        <motion.button
          onClick={() => onComplete(revision)}
          disabled={completing}
          className="w-full flex items-center justify-center gap-2 py-2 rounded-lg text-sm font-medium bg-green-500/20 text-green-400 border border-green-500/30 hover:bg-green-500/30 transition-all disabled:opacity-50"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <FiCheck className="w-4 h-4" />
          {completing ? 'Marking...' : 'Mark Complete'}
        </motion.button>
      )}
    </motion.div>
  );
}
