import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiCpu, FiMail, FiLock, FiArrowRight, FiAlertCircle, FiEye, FiEyeOff } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim() || !password) {
      setError('Please enter both your email address and password.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await login(email.trim(), password);
      navigate(from, { replace: true });
    } catch (err) {
      const msg = err.response?.data?.detail || 'Invalid email or password. Please try again.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleFillDemo = (demoEmail, demoPass) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setError('');
  };

  return (
    <div className="min-h-screen bg-navy-900 flex flex-col selection:bg-purple-500 selection:text-white">
      <Navbar />

      <div className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="w-full max-w-md"
        >
          {/* Card */}
          <div className="glass rounded-3xl p-8 border border-white/10 shadow-2xl relative overflow-hidden backdrop-blur-2xl">
            <div className="text-center mb-8">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center mx-auto mb-4 shadow-xl shadow-purple-500/25">
                <FiCpu className="w-7 h-7 text-white" />
              </div>
              <h1 className="text-2xl font-black text-white tracking-tight">Student Login</h1>
              <p className="text-slate-400 text-sm mt-1.5">
                Sign in to your B.Tech Computer Science learning workspace
              </p>
            </div>

            {error && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="mb-6 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-start gap-2.5 text-rose-300 text-sm"
              >
                <FiAlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5 text-rose-400" />
                <span>{error}</span>
              </motion.div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  University Email Address
                </label>
                <div className="relative">
                  <FiMail className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 w-4 h-4 pointer-events-none" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="student@btech.edu"
                    required
                    style={{ backgroundColor: '#FFFFFF', color: '#111827' }}
                    className="w-full pl-10 pr-4 py-3 rounded-xl bg-white text-[#111827] border border-gray-300 placeholder-[#64748B] text-sm focus:outline-none focus:border-purple-600 focus:ring-2 focus:ring-purple-500 font-medium transition-all"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Password
                  </label>
                </div>
                <div className="relative">
                  <FiLock className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 w-4 h-4 pointer-events-none" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                    style={{ backgroundColor: '#FFFFFF', color: '#111827' }}
                    className="w-full pl-10 pr-11 py-3 rounded-xl bg-white text-[#111827] border border-gray-300 placeholder-[#64748B] text-sm focus:outline-none focus:border-purple-600 focus:ring-2 focus:ring-purple-500 font-medium transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((prev) => !prev)}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 p-1 focus:outline-none cursor-pointer transition-colors"
                  >
                    {showPassword ? (
                      <FiEyeOff className="w-4 h-4 text-gray-600" />
                    ) : (
                      <FiEye className="w-4 h-4 text-gray-500" />
                    )}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full mt-2 py-3.5 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-500 via-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-500/25 hover:opacity-95 transition-all flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer"
              >
                {loading ? (
                  <span>Authenticating...</span>
                ) : (
                  <>
                    <span>Sign In to Dashboard</span>
                    <FiArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>

            {/* Quick Demo Credentials (Visible only during development or when explicitly enabled) */}
            {(import.meta.env.DEV || import.meta.env.VITE_ENABLE_DEMO_LOGIN === 'true') && (
              <div className="mt-8 pt-6 border-t border-white/10">
                <p className="text-xs text-slate-400 font-medium mb-3 text-center uppercase tracking-wider">
                  Quick Demo Accounts
                </p>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <button
                    type="button"
                    onClick={() => handleFillDemo('student.demo@btech.edu', 'StudentPass123!')}
                    className="p-2.5 rounded-xl glass hover:bg-white/10 text-left border border-white/10 text-slate-300 cursor-pointer transition-all"
                  >
                    <p className="font-semibold text-white">Rahul Sharma</p>
                    <p className="text-[10px] text-purple-300">Verified Student</p>
                  </button>
                  <button
                    type="button"
                    onClick={() => handleFillDemo('faculty.demo@btech.edu', 'TeacherPass123!')}
                    className="p-2.5 rounded-xl glass hover:bg-white/10 text-left border border-white/10 text-slate-300 cursor-pointer transition-all"
                  >
                    <p className="font-semibold text-white">Prof. Ananya Sen</p>
                    <p className="text-[10px] text-cyan-300">Faculty Demo</p>
                  </button>
                </div>
              </div>
            )}

            <div className="mt-6 text-center text-sm text-slate-400">
              Don't have an account yet?{' '}
              <Link to="/register" className="font-semibold text-purple-400 hover:text-purple-300 transition-colors">
                Register Free
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
