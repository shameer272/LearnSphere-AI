import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import DiagnosticAssessment from './pages/DiagnosticAssessment';
import LearningWorkspace from './pages/LearningWorkspace';
import ConceptMastery from './pages/ConceptMastery';
import RevisionCalendar from './pages/RevisionCalendar';
import TeacherDashboard from './pages/TeacherDashboard';
import ProfilePage from './pages/ProfilePage';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/setup" element={<Navigate to="/register" replace />} />

          {/* Protected Routes */}
          <Route
            path="/teacher"
            element={
              <ProtectedRoute requireTeacher>
                <TeacherDashboard />
              </ProtectedRoute>
            }
          />

          {/* Protected Student Routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/assessment"
            element={
              <ProtectedRoute>
                <DiagnosticAssessment />
              </ProtectedRoute>
            }
          />
          <Route
            path="/learn"
            element={
              <ProtectedRoute>
                <LearningWorkspace />
              </ProtectedRoute>
            }
          />
          <Route
            path="/mastery"
            element={
              <ProtectedRoute>
                <ConceptMastery />
              </ProtectedRoute>
            }
          />
          <Route
            path="/revisions"
            element={
              <ProtectedRoute>
                <RevisionCalendar />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
