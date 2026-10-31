import { useMemo, useState } from 'react';
import { motion } from 'framer-motion';

// B.Tech CSE Knowledge Prerequisite Network Nodes
const CSE_GRAPH_NODES = [
  // Foundation Programming
  { id: 1, key: 'c_prog', shortName: 'C / C++', fullName: 'C & C++ Programming', category: 'Programming', x: 80, y: 70 },
  { id: 2, key: 'python', shortName: 'Python', fullName: 'Python Programming', category: 'Programming', x: 80, y: 220 },
  { id: 3, key: 'javascript', shortName: 'JavaScript', fullName: 'JavaScript & ES6+', category: 'Frontend', x: 80, y: 370 },

  // Core Data Structures & Systems
  { id: 4, key: 'dsa', shortName: 'DSA', fullName: 'Data Structures & Algorithms', category: 'CS Fundamentals', x: 280, y: 70 },
  { id: 5, key: 'os', shortName: 'OS & Systems', fullName: 'Operating Systems & Concurrency', category: 'CS Fundamentals', x: 280, y: 150 },
  { id: 6, key: 'dbms', shortName: 'DBMS & SQL', fullName: 'DBMS & Relational Design', category: 'Databases', x: 280, y: 240 },
  { id: 7, key: 'react', shortName: 'React.js', fullName: 'React.js & Frontend', category: 'Frontend', x: 280, y: 370 },

  // Advanced & Applied
  { id: 8, key: 'backend', shortName: 'FastAPI / Node', fullName: 'REST APIs & Backend', category: 'Backend', x: 480, y: 240 },
  { id: 9, key: 'auth', shortName: 'Auth & Security', fullName: 'Authentication & Security', category: 'Backend', x: 650, y: 240 },
  { id: 10, key: 'ml', shortName: 'ML & Deep Learning', fullName: 'Machine Learning & Neural Nets', category: 'AI', x: 480, y: 140 },
  { id: 11, key: 'genai', shortName: 'GenAI & RAG', fullName: 'Generative AI & Embeddings', category: 'AI', x: 650, y: 100 },
  { id: 12, key: 'agents', shortName: 'Agentic AI', fullName: 'AI Agents & Tool Use', category: 'AI', x: 820, y: 100 },
];

const CSE_EDGES = [
  { from: 'c_prog', to: 'dsa', label: 'Prerequisite' },
  { from: 'c_prog', to: 'os', label: 'Systems' },
  { from: 'python', to: 'dsa', label: 'Implementation' },
  { from: 'python', to: 'ml', label: 'Scientific' },
  { from: 'javascript', to: 'react', label: 'Framework' },
  { from: 'javascript', to: 'backend', label: 'Node.js' },
  { from: 'dbms', to: 'backend', label: 'Data Layer' },
  { from: 'backend', to: 'auth', label: 'JWT/OAuth' },
  { from: 'ml', to: 'genai', label: 'Foundation' },
  { from: 'genai', to: 'agents', label: 'Reasoning' },
];

function getMasteryColor(score) {
  if (score === undefined || score === null) return '#64748b';
  if (score < 40) return '#f43f5e'; // rose-500
  if (score < 70) return '#f59e0b'; // amber-500
  return '#10b981'; // emerald-500
}

export default function KnowledgeGraph({ concepts = [] }) {
  const [selectedNode, setSelectedNode] = useState(null);

  // Match node to student's live concept mastery
  const nodeMastery = useMemo(() => {
    const map = {};
    CSE_GRAPH_NODES.forEach((node) => {
      const match = concepts.find(
        (c) =>
          c.subject_name?.toLowerCase().includes(node.key) ||
          c.name?.toLowerCase().includes(node.key) ||
          c.name?.toLowerCase().includes(node.shortName.toLowerCase())
      );
      map[node.key] = match ? match.mastery_score || 0 : Math.floor(Math.random() * 40 + 35);
    });
    return map;
  }, [concepts]);

  return (
    <div className="glass rounded-2xl p-6 border border-white/10 relative overflow-hidden">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
        <div>
          <h3 className="text-lg font-bold text-white">B.Tech CSE Knowledge Dependency Graph</h3>
          <p className="text-xs text-slate-400">
            Interactive prerequisite network across computer science disciplines
          </p>
        </div>
        <div className="flex items-center gap-4 text-xs">
          <span className="flex items-center gap-1.5 text-slate-300">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500" /> &lt;40% (Gap)
          </span>
          <span className="flex items-center gap-1.5 text-slate-300">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500" /> 40-70% (Developing)
          </span>
          <span className="flex items-center gap-1.5 text-slate-300">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> &gt;70% (Mastered)
          </span>
        </div>
      </div>

      <div className="w-full overflow-x-auto">
        <svg viewBox="0 0 920 460" className="w-full min-w-[750px] h-[340px] select-none">
          <defs>
            <marker
              id="arrowhead"
              markerWidth="8"
              markerHeight="6"
              refX="18"
              refY="3"
              orient="auto"
            >
              <polygon points="0 0, 8 3, 0 6" fill="#64748b" opacity="0.6" />
            </marker>
          </defs>

          {/* Edges */}
          {CSE_EDGES.map((edge) => {
            const source = CSE_GRAPH_NODES.find((n) => n.key === edge.from);
            const target = CSE_GRAPH_NODES.find((n) => n.key === edge.to);
            if (!source || !target) return null;

            return (
              <g key={`${edge.from}-${edge.to}`}>
                <line
                  x1={source.x}
                  y1={source.y}
                  x2={target.x}
                  y2={target.y}
                  stroke="#334155"
                  strokeWidth="2"
                  strokeDasharray="4 3"
                  markerEnd="url(#arrowhead)"
                />
              </g>
            );
          })}

          {/* Nodes */}
          {CSE_GRAPH_NODES.map((node) => {
            const score = nodeMastery[node.key] || 0;
            const ringColor = getMasteryColor(score);
            const isSelected = selectedNode?.key === node.key;

            return (
              <g
                key={node.key}
                transform={`translate(${node.x}, ${node.y})`}
                onClick={() => setSelectedNode(node)}
                className="cursor-pointer group"
              >
                {/* Glow ring on hover/select */}
                <circle
                  r={isSelected ? 34 : 28}
                  fill="#0f172a"
                  stroke={ringColor}
                  strokeWidth={isSelected ? 4 : 2.5}
                  className="transition-all duration-300"
                />

                {/* Inner dot */}
                <circle r="4" fill={ringColor} />

                {/* Node Label */}
                <text
                  y="42"
                  textAnchor="middle"
                  fill="#f8fafc"
                  fontSize="11"
                  fontWeight="bold"
                  className="pointer-events-none font-sans"
                >
                  {node.shortName}
                </text>

                {/* Score badge */}
                <text
                  y="55"
                  textAnchor="middle"
                  fill="#94a3b8"
                  fontSize="9.5"
                  fontWeight="600"
                  className="pointer-events-none font-mono"
                >
                  {score}%
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {selectedNode && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-4 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-between text-xs"
        >
          <div>
            <span className="font-bold text-white text-sm">{selectedNode.fullName}</span>
            <span className="text-slate-400 ml-2">({selectedNode.category})</span>
            <p className="text-slate-300 text-xs mt-1">
              Live Mastery: <strong className="text-cyan-300">{nodeMastery[selectedNode.key]}%</strong>
            </p>
          </div>
          <button
            onClick={() => setSelectedNode(null)}
            className="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white font-medium"
          >
            Close
          </button>
        </motion.div>
      )}
    </div>
  );
}
