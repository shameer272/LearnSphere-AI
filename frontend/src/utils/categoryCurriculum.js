/**
 * Category-specific curriculum mapping for LearnSphere AI.
 * Maps curriculum category names to exact database subject codes.
 */
export const CATEGORY_SUBJECT_CODES = {
  'Programming Languages': ['CS-PY', 'CS-C', 'CS-CPP', 'CS-JAVA', 'CS-JS'],
  'Frontend Engineering': ['CS-REACT', 'CS-HTML', 'CS-CSS', 'CS-TAILWIND', 'CS-JS'],
  'Backend Architecture': ['CS-NODE', 'CS-FASTAPI', 'CS-REST', 'CS-AUTH'],
  'Database Management': ['CS-SQL', 'CS-MYSQL', 'CS-MONGO', 'CS-DBDESIGN', 'CS-DBMS'],
  'CS Core Fundamentals': ['CS-DSA', 'CS-OS', 'CS-CN', 'CS-OOP'],
  'Artificial Intelligence': ['CS-ML', 'CS-DL', 'CS-GENAI', 'CS-AGENTS'],
};

/**
 * Returns subject IDs matching the category from a list of subjects fetched from the database.
 * @param {string} category
 * @param {Array<{id: number, code: string, category: string}>} availableSubjects
 * @returns {number[]}
 */
export function getSubjectIdsForCategory(category, availableSubjects = []) {
  if (!category || !Array.isArray(availableSubjects)) return [];
  const targetCodes = CATEGORY_SUBJECT_CODES[category];
  if (targetCodes && targetCodes.length > 0) {
    return availableSubjects
      .filter((s) => targetCodes.includes(s.code))
      .map((s) => s.id);
  }
  // Fallback: match by DB category string if exact code mapping not found
  return availableSubjects
    .filter((s) => s.category?.toLowerCase() === category.toLowerCase())
    .map((s) => s.id);
}
