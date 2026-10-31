import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  FiCpu,
  FiZap,
  FiTarget,
  FiRepeat,
  FiArrowRight,
  FiCheckCircle,
  FiCode,
  FiLayers,
  FiDatabase,
  FiServer,
  FiAward,
  FiCompass,
} from 'react-icons/fi';
import Navbar from '../components/Navbar';
import { CATEGORY_SUBJECT_CODES } from '../utils/categoryCurriculum';

const features = [
  {
    icon: FiCpu,
    title: 'AI Misconception Detection',
    desc: 'Deep reasoning analysis identifies precisely why algorithmic and conceptual errors occur, not just syntax mistakes.',
    color: 'from-purple-500/20 to-purple-600/10 border-purple-500/30',
    iconColor: 'text-purple-400',
  },
  {
    icon: FiZap,
    title: 'Adaptive Question Engine',
    desc: 'Dynamic difficulty scaling serves target questions at your edge of competence — from foundational to FAANG-grade.',
    color: 'from-cyan-500/20 to-cyan-600/10 border-cyan-500/30',
    iconColor: 'text-cyan-400',
  },
  {
    icon: FiRepeat,
    title: 'Smart Spaced Repetition',
    desc: 'Automated retention intervals model memory decay curves to schedule high-yield reviews before you forget.',
    color: 'from-blue-500/20 to-blue-600/10 border-blue-500/30',
    iconColor: 'text-blue-400',
  },
  {
    icon: FiTarget,
    title: 'Concept Mastery Tracking',
    desc: 'Granular topic graphs reflect deterministic mastery scoring across data structures, system design, and AI models.',
    color: 'from-emerald-500/20 to-emerald-600/10 border-emerald-500/30',
    iconColor: 'text-emerald-400',
  },
  {
    icon: FiCode,
    title: 'Code Debugging & Execution',
    desc: 'Scenario-based questions, memory dereference visualizations, and output prediction for compiled and interpreted languages.',
    color: 'from-amber-500/20 to-amber-600/10 border-amber-500/30',
    iconColor: 'text-amber-400',
  },
  {
    icon: FiCompass,
    title: 'Adaptive Learning Analytics',
    desc: 'Comprehensive diagnostic reports map your knowledge gaps directly to targeted engineering curriculum modules.',
    color: 'from-rose-500/20 to-rose-600/10 border-rose-500/30',
    iconColor: 'text-rose-400',
  },
];

const cseCategories = [
  {
    name: 'Programming Languages',
    icon: FiCode,
    color: 'text-purple-400',
    subjects: ['Python', 'C Programming', 'C++', 'Java', 'JavaScript'],
  },
  {
    name: 'Frontend Engineering',
    icon: FiLayers,
    color: 'text-cyan-400',
    subjects: ['React.js', 'HTML5 & CSS3', 'Tailwind CSS', 'Modern JS'],
  },
  {
    name: 'Backend Architecture',
    icon: FiServer,
    color: 'text-blue-400',
    subjects: ['Node.js', 'FastAPI', 'REST APIs', 'Auth & Security'],
  },
  {
    name: 'Database Management',
    icon: FiDatabase,
    color: 'text-emerald-400',
    subjects: ['SQL', 'MySQL', 'MongoDB', 'Database Normalization'],
  },
  {
    name: 'CS Core Fundamentals',
    icon: FiTarget,
    color: 'text-amber-400',
    subjects: ['Data Structures & Algorithms', 'Operating Systems', 'Networks', 'OOP'],
  },
  {
    name: 'Artificial Intelligence',
    icon: FiCpu,
    color: 'text-rose-400',
    subjects: ['Machine Learning', 'Deep Learning', 'Generative AI', 'Agentic AI'],
  },
];

const steps = [
  {
    num: '01',
    title: 'Assess Your Knowledge',
    desc: 'Take an adaptive diagnostic test that dynamically maps your foundational understanding across B.Tech CSE topics.',
  },
  {
    num: '02',
    title: 'Discover Learning Gaps',
    desc: 'Gemini AI evaluates your written reasoning to pinpoint exact misconceptions before they become persistent bad habits.',
  },
  {
    num: '03',
    title: 'Learn with AI Tutoring',
    desc: 'Receive tailored code challenges, algorithmic hints, and step-by-step diagnostic feedback targeted to your weak concepts.',
  },
  {
    num: '04',
    title: 'Track Your Improvement',
    desc: 'Watch your concept mastery grow across our interactive dependency graph with automated spaced repetition reminders.',
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-navy-900 text-white selection:bg-purple-500 selection:text-white">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-28 pb-20 px-4 sm:px-6 lg:px-8">
        {/* Ambient Gradient Glows */}
        <div className="absolute top-10 left-1/3 w-[500px] h-[500px] bg-purple-600/15 rounded-full blur-[140px] pointer-events-none" />
        <div className="absolute top-32 right-1/4 w-[450px] h-[450px] bg-cyan-500/15 rounded-full blur-[140px] pointer-events-none" />

        <div className="max-w-7xl mx-auto text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: -15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-2 glass rounded-full text-xs sm:text-sm text-purple-300 font-medium mb-8 border border-purple-500/30 shadow-lg shadow-purple-500/10"
          >
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            Adaptive AI Learning Platform for B.Tech Computer Science
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-tight max-w-4xl mx-auto mb-6"
          >
            Master Every Skill. <br />
            <span className="gradient-text">Learn at Your Own Pace.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto mb-10 leading-relaxed font-normal"
          >
            An intelligent AI-powered learning platform that understands your knowledge, identifies your weaknesses, and creates a personalized learning journey.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto"
          >
            <Link
              to="/register"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl font-semibold bg-gradient-to-r from-purple-500 via-indigo-500 to-cyan-500 text-white hover:opacity-95 transition-all shadow-xl shadow-purple-500/25 active:scale-95"
            >
              Start Learning Free <FiArrowRight className="w-5 h-5" />
            </Link>
            <a
              href="#features"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl font-semibold glass text-slate-200 hover:text-white hover:bg-white/10 transition-all border border-white/10"
            >
              Explore Features
            </a>
          </motion.div>

          {/* Social Proof / Stats Pill */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto pt-10 border-t border-white/10 text-center"
          >
            <div>
              <p className="text-3xl font-extrabold gradient-text">31</p>
              <p className="text-xs text-slate-400 mt-1 uppercase tracking-wider">B.Tech CSE Subjects</p>
            </div>
            <div>
              <p className="text-3xl font-extrabold gradient-text">6</p>
              <p className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Curriculum Categories</p>
            </div>
            <div>
              <p className="text-3xl font-extrabold gradient-text">Gemini AI</p>
              <p className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Reasoning Engine</p>
            </div>
            <div>
              <p className="text-3xl font-extrabold gradient-text">100%</p>
              <p className="text-xs text-slate-400 mt-1 uppercase tracking-wider">Adaptive Mastery</p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-4 sm:px-6 lg:px-8 border-t border-white/5 relative bg-navy-950/40">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs uppercase tracking-widest font-bold text-purple-400 mb-3">Intelligent Pedagogy</h2>
            <h3 className="text-3xl sm:text-5xl font-black text-white tracking-tight">
              Engineered for Deep Conceptual Mastery
            </h3>
            <p className="text-slate-400 text-base sm:text-lg mt-4">
              LearnSphere AI is not a generic quiz bank. It diagnoses algorithmic reasoning and dynamically adapts to your personal learning curve.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.1 }}
                className={`glass rounded-2xl p-6 border bg-gradient-to-br ${f.color} hover:border-white/20 transition-all`}
              >
                <div className={`w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center mb-5 ${f.iconColor}`}>
                  <f.icon className="w-6 h-6" />
                </div>
                <h4 className="text-xl font-bold text-white mb-2">{f.title}</h4>
                <p className="text-slate-400 text-sm leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Subjects Section */}
      <section id="subjects" className="py-24 px-4 sm:px-6 lg:px-8 border-t border-white/5">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs uppercase tracking-widest font-bold text-cyan-400 mb-3">Comprehensive Curriculum</h2>
            <h3 className="text-3xl sm:text-5xl font-black text-white tracking-tight">
              Built for Computer Science & Engineering
            </h3>
            <p className="text-slate-400 text-base sm:text-lg mt-4">
              Explore 31 industry-relevant subjects curated specifically for university coursework, competitive exams, and technical interviews.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {cseCategories.map((cat) => (
              <div
                key={cat.name}
                className="glass rounded-2xl p-6 border border-white/10 hover:border-cyan-500/30 transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center">
                      <cat.icon className={`w-5 h-5 ${cat.color}`} />
                    </div>
                    <h4 className="font-bold text-lg text-white">{cat.name}</h4>
                  </div>
                  <ul className="space-y-2 mb-6">
                    {cat.subjects.map((sub) => (
                      <li key={sub} className="flex items-center gap-2 text-sm text-slate-300">
                        <FiCheckCircle className="w-4 h-4 text-cyan-400/80 shrink-0" />
                        <span>{sub}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <Link
                  to={`/register?category=${encodeURIComponent(cat.name)}`}
                  state={{
                    category: cat.name,
                    subjectCodes: CATEGORY_SUBJECT_CODES[cat.name] || [],
                  }}
                  className="inline-flex items-center gap-1.5 text-xs font-semibold text-purple-300 hover:text-purple-200 transition-colors pt-4 border-t border-white/5 cursor-pointer"
                >
                  Enroll in curriculum <FiArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-24 px-4 sm:px-6 lg:px-8 border-t border-white/5 bg-navy-950/40">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs uppercase tracking-widest font-bold text-purple-400 mb-3">Learning Methodology</h2>
            <h3 className="text-3xl sm:text-5xl font-black text-white tracking-tight">
              How LearnSphere AI Works
            </h3>
            <p className="text-slate-400 text-base sm:text-lg mt-4">
              Four deliberate steps designed to move you from baseline recall to intuitive problem-solving mastery.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {steps.map((st) => (
              <div key={st.num} className="glass rounded-2xl p-6 border border-white/10 relative">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500/30 to-cyan-500/30 border border-purple-500/40 flex items-center justify-center text-lg font-black text-white mb-4">
                  {st.num}
                </div>
                <h4 className="text-lg font-bold text-white mb-2">{st.title}</h4>
                <p className="text-slate-400 text-xs sm:text-sm leading-relaxed">{st.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-24 px-4 sm:px-6 lg:px-8 border-t border-white/5">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-xs uppercase tracking-widest font-bold text-cyan-400 mb-3">About LearnSphere AI</h2>
          <h3 className="text-3xl sm:text-4xl font-black text-white mb-6">
            Empowering Next-Generation Software Engineers
          </h3>
          <p className="text-slate-300 leading-relaxed text-base sm:text-lg mb-8">
            LearnSphere AI was designed by computer science educators and software architects to eliminate the frustration of one-size-fits-all tutorials. By evaluating the root cause of algorithmic misconceptions in code snippets and reasoning, we provide every student with an individualized tutor that scales with them from introductory syntax to advanced distributed architectures.
          </p>
          <div className="inline-flex items-center gap-6 text-sm text-slate-400">
            <span className="flex items-center gap-2"><FiAward className="text-yellow-400" /> B.Tech CSE Accredited</span>
            <span className="flex items-center gap-2"><FiCpu className="text-purple-400" /> Gemini Powered</span>
            <span className="flex items-center gap-2"><FiTarget className="text-cyan-400" /> Mastery Guaranteed</span>
          </div>
        </div>
      </section>

      {/* Final Call to Action */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 border-t border-white/5 bg-gradient-to-b from-navy-900 to-purple-950/40">
        <div className="max-w-4xl mx-auto text-center glass rounded-3xl p-10 sm:p-14 border border-purple-500/30 shadow-2xl shadow-purple-500/20">
          <h2 className="text-3xl sm:text-5xl font-black text-white tracking-tight mb-4">
            Accelerate Your Engineering Career Today
          </h2>
          <p className="text-slate-300 text-base sm:text-lg max-w-xl mx-auto mb-8">
            Create your account in seconds, take your baseline diagnostic assessment, and let AI build your personalized roadmap to mastery.
          </p>
          <Link
            to="/register"
            className="inline-flex items-center gap-2 px-9 py-4 rounded-xl font-bold text-base bg-gradient-to-r from-purple-500 to-cyan-500 text-white hover:opacity-95 transition-all shadow-xl shadow-purple-500/30 active:scale-95"
          >
            Start Learning Free <FiArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12 px-4 sm:px-6 lg:px-8 text-center text-slate-400 text-xs sm:text-sm">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-purple-500 to-cyan-400 flex items-center justify-center text-white font-bold text-sm">
              L
            </div>
            <span className="font-bold text-white text-base">LearnSphere AI</span>
          </div>
          <p>© 2026 LearnSphere AI — B.Tech Computer Science and Engineering. All rights reserved.</p>
          <div className="flex items-center gap-4">
            <Link to="/login" className="hover:text-white transition-colors">Login</Link>
            <Link to="/register" className="hover:text-white transition-colors">Register</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
