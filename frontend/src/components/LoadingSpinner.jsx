import { motion } from 'framer-motion';

export default function LoadingSpinner({ fullPage = false, text = 'Loading...' }) {
  const spinner = (
    <div className="flex flex-col items-center justify-center gap-3">
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 rounded-full border-2 border-white/10" />
        <motion.div
          className="absolute inset-0 rounded-full border-2 border-transparent border-t-purple-500 border-r-cyan-500"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        />
      </div>
      {text && <p className="text-sm text-slate-400">{text}</p>}
    </div>
  );

  if (fullPage) {
    return (
      <div className="min-h-screen bg-navy-900 flex items-center justify-center">
        {spinner}
      </div>
    );
  }

  return spinner;
}
