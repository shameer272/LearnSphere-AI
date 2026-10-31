import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiCpu, FiMenu, FiX, FiLogOut, FiUser, FiBookOpen, FiActivity, FiLayers, FiCalendar } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isTeacher = user?.role === 'teacher' || user?.role === 'admin';

  const navLinks = isAuthenticated
    ? [
        { to: '/dashboard', label: 'Dashboard', icon: FiActivity },
        { to: '/learn', label: 'Adaptive Learn', icon: FiBookOpen },
        { to: '/assessment', label: 'Diagnostic', icon: FiLayers },
        { to: '/mastery', label: 'Mastery', icon: FiCpu },
        { to: '/revisions', label: 'Revisions', icon: FiCalendar },
        ...(isTeacher ? [{ to: '/teacher', label: 'Teacher Dashboard' }] : []),
      ]
    : [
        { to: '/', label: 'Home' },
        { to: '/#features', label: 'Features' },
        { to: '/#subjects', label: 'Subjects' },
        { to: '/#about', label: 'About' },
      ];

  const handleNavClick = (to) => {
    setMobileOpen(false);
    if (to.startsWith('/#')) {
      const targetId = to.replace('/#', '');
      const el = document.getElementById(targetId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <nav className="glass sticky top-0 z-50 border-b border-white/10 backdrop-blur-xl bg-navy-900/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to={isAuthenticated ? '/dashboard' : '/'} className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-purple-500/20 group-hover:scale-105 transition-transform">
              <FiCpu className="w-5 h-5 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-base font-black tracking-tight gradient-text">LearnSphere AI</span>
              <span className="text-[10px] text-slate-400 font-medium tracking-wider uppercase">B.Tech CSE Adaptive Platform</span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => {
              const isActive = location.pathname === link.to;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  onClick={() => handleNavClick(link.to)}
                  className={`px-3.5 py-2 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30 shadow-sm'
                      : 'text-slate-300 hover:text-white hover:bg-white/10'
                  }`}
                >
                  {link.label}
                </Link>
              );
            })}
          </div>

          {/* Right Action Buttons */}
          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <Link
                  to="/profile"
                  className="flex items-center gap-2 px-3 py-1.5 glass rounded-xl hover:bg-white/10 transition-colors border border-white/10"
                >
                  <div className="w-6 h-6 rounded-full bg-purple-500/30 flex items-center justify-center text-purple-300">
                    <FiUser className="w-3.5 h-3.5" />
                  </div>
                  <span className="text-sm font-medium text-slate-200">{user?.name?.split(' ')[0] || 'Student'}</span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                    {user?.learning_level || 'B.Tech'}
                  </span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-all"
                  title="Logout"
                >
                  <FiLogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2.5">
                <Link
                  to="/login"
                  className="px-4 py-2 rounded-xl text-sm font-medium text-slate-300 hover:text-white hover:bg-white/10 transition-all"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-5 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-purple-500 to-cyan-500 text-white hover:opacity-95 shadow-md shadow-purple-500/25 transition-all hover:scale-[1.02]"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>

          {/* Mobile hamburger button */}
          <button
            className="md:hidden p-2 rounded-xl text-slate-300 hover:text-white hover:bg-white/10 transition-all"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle navigation menu"
          >
            {mobileOpen ? <FiX className="w-6 h-6" /> : <FiMenu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t border-white/10 bg-navy-900/95 backdrop-blur-xl overflow-hidden"
          >
            <div className="px-4 py-3 space-y-1">
              {navLinks.map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  onClick={() => handleNavClick(link.to)}
                  className="block px-3 py-2 rounded-xl text-sm text-slate-300 hover:text-white hover:bg-white/10 transition-all font-medium"
                >
                  {link.label}
                </Link>
              ))}

              <div className="pt-3 border-t border-white/10 flex flex-col gap-2">
                {isAuthenticated ? (
                  <>
                    <div className="flex items-center justify-between px-3 py-2 text-sm text-slate-300">
                      <span>{user?.name}</span>
                      <span className="text-xs text-purple-400">{user?.degree}</span>
                    </div>
                    <Link
                      to="/profile"
                      onClick={() => setMobileOpen(false)}
                      className="w-full text-center py-2.5 rounded-xl text-sm font-medium glass text-white"
                    >
                      My Profile
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="w-full text-center py-2.5 rounded-xl text-sm font-medium text-red-400 bg-red-500/10 hover:bg-red-500/20"
                    >
                      Logout
                    </button>
                  </>
                ) : (
                  <>
                    <Link
                      to="/login"
                      onClick={() => setMobileOpen(false)}
                      className="w-full text-center py-2.5 rounded-xl text-sm font-medium text-white glass hover:bg-white/10"
                    >
                      Login
                    </Link>
                    <Link
                      to="/register"
                      onClick={() => setMobileOpen(false)}
                      className="w-full text-center py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-purple-500 to-cyan-500 text-white"
                    >
                      Get Started Free
                    </Link>
                  </>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
