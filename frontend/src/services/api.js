import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '/api' : 'http://localhost:8000/api');
const api = axios.create({ baseURL: BASE_URL, timeout: 30000 });

// Attach Authorization Bearer token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('learnsphere_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
  updateProfile: (data) => api.put('/auth/profile', data),
};

export const subjectsAPI = {
  list: (category) => api.get(`/subjects${category ? `?category=${encodeURIComponent(category)}` : ''}`),
  getCategories: () => api.get('/subjects/categories'),
  getDetail: (id) => api.get(`/subjects/${id}`),
};

export const conceptsAPI = {
  list: (subjectId) => api.get(`/concepts${subjectId ? `?subject_id=${subjectId}` : ''}`),
};

export const studentsAPI = {
  list: () => api.get('/students'),
  get: (id) => api.get(`/students/${id}`),
  getDashboard: (id, subjectId) =>
    api.get(`/students/${id}/dashboard${subjectId ? `?subject_id=${subjectId}` : ''}`),
  getMastery: (id) => api.get(`/students/${id}/mastery`),
};

export const assessmentAPI = {
  getQuestions: (studentId, subjectId) => {
    const params = new URLSearchParams();
    if (studentId) params.append('student_id', studentId);
    if (subjectId) params.append('subject_id', subjectId);
    const query = params.toString() ? `?${params.toString()}` : '';
    return api.get(`/assessment/questions${query}`);
  },
  submit: (data) => api.post('/assessment/submit', data),
};

export const learningAPI = {
  getSubjects: (studentId) => {
    const query = studentId ? `?student_id=${studentId}` : '';
    return api.get(`/learning/subjects${query}`);
  },
  getNextQuestion: (studentId, subjectId, conceptId) => {
    const params = new URLSearchParams({ student_id: studentId });
    if (subjectId) params.append('subject_id', subjectId);
    if (conceptId) params.append('concept_id', conceptId);
    return api.get(`/learning/next-question?${params.toString()}`);
  },
  submitAnswer: (data) => api.post('/learning/answer', data),
  getHistory: (studentId, subjectId) => {
    const params = new URLSearchParams({ student_id: studentId });
    if (subjectId) params.append('subject_id', subjectId);
    return api.get(`/learning/history?${params.toString()}`);
  },
};

export const revisionsAPI = {
  get: (studentId, subjectId) =>
    api.get(`/revisions/${studentId}${subjectId ? `?subject_id=${subjectId}` : ''}`),
  complete: (data) => api.post('/revisions/complete', data),
};

export const teacherAPI = {
  getAnalytics: () => api.get('/teacher/analytics'),
};

export default api;
