import { motion } from 'framer-motion';
import { getMasteryBg } from '../utils/helpers';

export default function MasteryBar({ mastery, score, label, showLabel = true, animate = true }) {
  const value = score ?? mastery ?? 0;
  const bg = getMasteryBg(value);

  return (
    <div className="w-full">
      {showLabel && label && (
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs text-slate-300 font-medium">{label}</span>
          <span className="text-xs font-semibold text-white">{Math.round(value)}%</span>
        </div>
      )}
      <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${bg}`}
          initial={animate ? { width: 0 } : { width: `${value}%` }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      </div>
      {!showLabel && (
        <div className="text-right mt-1">
          <span className="text-[10px] text-slate-400 font-mono">{Math.round(value)}%</span>
        </div>
      )}
    </div>
  );
}
