import { motion, AnimatePresence } from 'framer-motion';
import { Check, Loader2, Brain, Database, FileText, PlayCircle, AlertCircle } from 'lucide-react';
import { PipelineStep } from '../types';

interface PipelineStatusProps {
  steps: PipelineStep[];
  isVisible: boolean;
}

const iconMap = {
  brain: Brain,
  database: Database,
  'file-text': FileText,
  'play-circle': PlayCircle
};

export function PipelineStatus({ steps, isVisible }: PipelineStatusProps) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        >
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-8 max-w-2xl w-full shadow-2xl"
          >
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-white mb-2">Deterministic Pipeline</h2>
              <p className="text-slate-400">Processing your request through verified templates</p>
            </div>

            <div className="space-y-4">
              {steps.map((step, index) => {
                const IconComponent = iconMap[step.icon as keyof typeof iconMap] || Brain;

                return (
                  <motion.div
                    key={step.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.2 }}
                    className={`flex items-center gap-4 p-4 rounded-xl border transition-all ${
                      step.status === 'completed'
                        ? 'bg-green-500/10 border-green-500/50'
                        : step.status === 'in_progress'
                        ? 'bg-blue-500/10 border-blue-500/50'
                        : step.status === 'error'
                        ? 'bg-red-500/10 border-red-500/50'
                        : 'bg-slate-800/30 border-slate-700'
                    }`}
                  >
                    <div className="flex-shrink-0">
                      {step.status === 'completed' && (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center"
                        >
                          <Check className="w-6 h-6 text-white" />
                        </motion.div>
                      )}
                      {step.status === 'in_progress' && (
                        <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center">
                          <Loader2 className="w-6 h-6 text-white animate-spin" />
                        </div>
                      )}
                      {step.status === 'error' && (
                        <div className="w-10 h-10 rounded-full bg-red-500 flex items-center justify-center">
                          <AlertCircle className="w-6 h-6 text-white" />
                        </div>
                      )}
                      {step.status === 'pending' && (
                        <div className="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center">
                          <IconComponent className="w-5 h-5 text-slate-400" />
                        </div>
                      )}
                    </div>

                    <div className="flex-1">
                      <p className={`font-medium ${
                        step.status === 'completed'
                          ? 'text-green-300'
                          : step.status === 'in_progress'
                          ? 'text-blue-300'
                          : step.status === 'error'
                          ? 'text-red-300'
                          : 'text-slate-400'
                      }`}>
                        {step.label}
                      </p>
                    </div>

                    {step.status === 'completed' && (
                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="text-green-400 text-sm font-mono"
                      >
                        ✓
                      </motion.div>
                    )}
                    {step.status === 'in_progress' && (
                      <div className="text-blue-400 text-sm font-mono animate-pulse">
                        ⏳
                      </div>
                    )}
                  </motion.div>
                );
              })}
            </div>

            <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
              <p className="text-sm text-blue-200">
                Using verified Manim templates from knowledge base
              </p>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
