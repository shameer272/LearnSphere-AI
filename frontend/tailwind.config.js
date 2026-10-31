export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        navy: { 900: '#0a0e1a', 800: '#0d1329', 700: '#111827', 600: '#1a2236' },
        purple: { 400: '#a855f7', 500: '#9333ea', 600: '#7c3aed' },
        cyan: { 400: '#22d3ee', 500: '#06b6d4' },
        blue: { 400: '#60a5fa', 500: '#3b82f6' }
      },
      fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] }
    }
  },
  plugins: []
}
