import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from './LoadingSpinner';

export default function ProtectedRoute({ children, requireTeacher = false }) {
  const { user, isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen bg-navy-900 flex flex-col items-center justify-center">
        <LoadingSpinner />
        <p className="text-slate-400 mt-4 text-sm animate-pulse">Verifying credentials...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requireTeacher) {
    const isTeacher = user?.role === 'teacher' || user?.role === 'admin';
    if (!isTeacher) {
      return (
        <Navigate
          to="/dashboard"
          state={{ error: 'Access Denied: Teacher or Faculty role authorization required to view Teacher Hub.' }}
          replace
        />
      );
    }
  }

  return children;
}
