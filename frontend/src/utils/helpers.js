export function getTimeOfDay() {
  const hour = new Date().getHours();
  if (hour < 12) return 'morning';
  if (hour < 17) return 'afternoon';
  return 'evening';
}

export function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = date - now;
  const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Tomorrow';
  if (diffDays > 1 && diffDays <= 7) return `In ${diffDays} days`;
  if (diffDays < 0 && diffDays >= -1) return 'Yesterday';
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

export function getMasteryColor(mastery) {
  if (mastery < 40) return 'text-red-400';
  if (mastery < 70) return 'text-yellow-400';
  return 'text-green-400';
}

export function getMasteryBg(mastery) {
  if (mastery < 40) return 'bg-red-500';
  if (mastery < 70) return 'bg-yellow-500';
  return 'bg-green-500';
}

export function getMasteryLabel(mastery) {
  if (mastery < 40) return 'Weak';
  if (mastery < 70) return 'Developing';
  return 'Mastered';
}

export function getMasteryBadgeClass(mastery) {
  if (mastery < 40) return 'bg-red-500/20 text-red-400 border border-red-500/30';
  if (mastery < 70) return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30';
  return 'bg-green-500/20 text-green-400 border border-green-500/30';
}

export function getDifficultyColor(difficulty) {
  if (!difficulty) return 'bg-gray-500/20 text-gray-400';
  const d = difficulty.toLowerCase();
  if (d === 'easy') return 'bg-green-500/20 text-green-400';
  if (d === 'medium') return 'bg-yellow-500/20 text-yellow-400';
  return 'bg-red-500/20 text-red-400';
}

export function getPriorityBadge(priority) {
  if (!priority) return 'bg-gray-500/20 text-gray-400';
  const p = priority.toLowerCase();
  if (p === 'high') return 'bg-red-500/20 text-red-400 border border-red-500/30';
  if (p === 'medium') return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30';
  return 'bg-green-500/20 text-green-400 border border-green-500/30';
}
