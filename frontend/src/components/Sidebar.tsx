import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Database, Code, Brain, ChevronRight, ChevronDown } from 'lucide-react';
import { TopicCategory, TopicItem } from '../types';
import { topics } from '../data/topics';

interface SidebarProps {
  onTopicSelect: (topic: TopicItem) => void;
  selectedTopic: TopicItem | null;
}

const categoryConfig = {
  'data-structures': {
    label: 'Data Structures',
    icon: Database,
    color: 'from-cyan-500 to-blue-500'
  },
  'algorithms': {
    label: 'Algorithms',
    icon: Code,
    color: 'from-blue-500 to-slate-500'
  },
  'ml-fundamentals': {
    label: 'ML Fundamentals',
    icon: Brain,
    color: 'from-slate-500 to-cyan-500'
  }
};

export function Sidebar({ onTopicSelect, selectedTopic }: SidebarProps) {
  const [expandedCategory, setExpandedCategory] = useState<TopicCategory | null>(null);
  const categories: TopicCategory[] = ['data-structures', 'algorithms', 'ml-fundamentals'];

  const toggleCategory = (category: TopicCategory) => {
    setExpandedCategory(expandedCategory === category ? null : category);
  };

  return (
    <motion.aside
      initial={{ x: -300, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="w-80 h-screen bg-gradient-to-b from-slate-950 to-slate-900 border-r border-slate-800 overflow-y-auto"
    >
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white mb-2">AlgoViz AI</h1>
          <p className="text-sm text-slate-400">Deterministic Algorithm Visualization</p>
        </div>

        <div className="space-y-3">
          {categories.map((category) => {
            const config = categoryConfig[category];
            const Icon = config.icon;
            const categoryTopics = topics.filter(t => t.category === category);
            const isExpanded = expandedCategory === category;

            return (
              <div key={category} className="space-y-0">
                <motion.button
                  onClick={() => toggleCategory(category)}
                  className="w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-slate-800/40 hover:bg-slate-800/60 transition-all group"
                  whileHover={{ backgroundColor: 'rgba(30, 41, 59, 0.8)' }}
                >
                  <Icon className="w-5 h-5 text-blue-400 flex-shrink-0" />
                  <span className="flex-1 text-sm font-semibold text-slate-200 text-left">
                    {config.label}
                  </span>
                  <motion.div
                    animate={{ rotate: isExpanded ? 90 : 0 }}
                    transition={{ duration: 0.2 }}
                    className="flex-shrink-0"
                  >
                    <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-slate-400 transition-colors" />
                  </motion.div>
                </motion.button>

                <AnimatePresence>
                  {isExpanded && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                      className="overflow-hidden"
                    >
                      <div className="space-y-1 pl-4 pr-3 py-2 border-l-2 border-slate-700 ml-6">
                        {categoryTopics.map((topic, index) => {
                          const isSelected = selectedTopic?.id === topic.id;

                          return (
                            <motion.button
                              key={topic.id}
                              initial={{ x: -10, opacity: 0 }}
                              animate={{ x: 0, opacity: 1 }}
                              transition={{ duration: 0.15, delay: index * 0.03 }}
                              onClick={() => onTopicSelect(topic)}
                              className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-left transition-all text-sm ${
                                isSelected
                                  ? 'bg-blue-500/25 text-blue-300 border-l-2 border-blue-400 shadow-lg shadow-blue-500/10'
                                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/40'
                              }`}
                              whileHover={{ x: 4 }}
                            >
                              <span className="flex-1">{topic.name}</span>
                              {isSelected && (
                                <motion.div
                                  initial={{ scale: 0 }}
                                  animate={{ scale: 1 }}
                                  className="w-2 h-2 rounded-full bg-blue-400 flex-shrink-0"
                                />
                              )}
                            </motion.button>
                          );
                        })}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            );
          })}
        </div>

        <div className="mt-8 p-4 rounded-lg bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/30">
          <p className="text-xs text-slate-300 leading-relaxed">
            Powered by verified Manim templates and ground-truth knowledge base.
          </p>
        </div>
      </div>
    </motion.aside>
  );
}
