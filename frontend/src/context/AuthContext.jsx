import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => {
    if (typeof window === 'undefined' || typeof localStorage === 'undefined') return null;
    return localStorage.getItem('learnsphere_token');
  });
  const [user, setUser] = useState(() => {
    if (typeof window === 'undefined' || typeof localStorage === 'undefined') return null;
    const saved = localStorage.getItem('learnsphere_user');
    try {
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState(true);

  // Validate or restore authentication on mount
  useEffect(() => {
    async function verifyAuth() {
      if (typeof window === 'undefined' || typeof localStorage === 'undefined') {
        setLoading(false);
        return;
      }
      const storedToken = localStorage.getItem('learnsphere_token');
      if (!storedToken) {
        setToken(null);
        setUser(null);
        setLoading(false);
        return;
      }

      try {
        const res = await authAPI.getMe();
        setUser(res.data);
        localStorage.setItem('learnsphere_user', JSON.stringify(res.data));
      } catch {
        // Token expired or invalid
        localStorage.removeItem('learnsphere_token');
        localStorage.removeItem('learnsphere_user');
        setToken(null);
        setUser(null);
      } finally {
        setLoading(false);
      }
    }

    verifyAuth();
  }, []);

  const login = async (email, password) => {
    const res = await authAPI.login({ email, password });
    const { access_token, student } = res.data;
    localStorage.setItem('learnsphere_token', access_token);
    localStorage.setItem('learnsphere_user', JSON.stringify(student));
    localStorage.setItem('learnsphere_student_id', student.id.toString());
    setToken(access_token);
    setUser(student);
    return student;
  };

  const register = async (data) => {
    const res = await authAPI.register(data);
    const { access_token, student } = res.data;
    localStorage.setItem('learnsphere_token', access_token);
    localStorage.setItem('learnsphere_user', JSON.stringify(student));
    localStorage.setItem('learnsphere_student_id', student.id.toString());
    setToken(access_token);
    setUser(student);
    return student;
  };

  const logout = () => {
    localStorage.removeItem('learnsphere_token');
    localStorage.removeItem('learnsphere_user');
    localStorage.removeItem('learnsphere_student_id');
    setToken(null);
    setUser(null);
  };

  const updateProfile = async (data) => {
    const res = await authAPI.updateProfile(data);
    setUser(res.data);
    localStorage.setItem('learnsphere_user', JSON.stringify(res.data));
    return res.data;
  };

  const refreshUser = async () => {
    try {
      const res = await authAPI.getMe();
      setUser(res.data);
      localStorage.setItem('learnsphere_user', JSON.stringify(res.data));
      return res.data;
    } catch {
      return user;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        studentId: user?.id || null,
        isAuthenticated: !!token && !!user,
        isTeacher: user?.role === 'teacher' || user?.role === 'admin',
        loading,
        login,
        register,
        logout,
        updateProfile,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return ctx;
}
