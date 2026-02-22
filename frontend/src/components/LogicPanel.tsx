import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, Circle, PlayCircle } from 'lucide-react';
import { TeachingPlan } from '../types';

interface LogicPanelProps {
  teachingPlan: TeachingPlan | null;
  currentStep: number;
  isVideoCompleted?: boolean;
}

export function LogicPanel({ teachingPlan, currentStep, isVideoCompleted }: LogicPanelProps) {
  if (!teachingPlan) {
    return (
      <motion.div
        initial={{ x: 300, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="w-96 h-full bg-slate-900/50 backdrop-blur-xl border-l border-slate-800 p-6"
      >
        <div className="flex flex-col items-center justify-center h-full text-center">
          <PlayCircle className="w-16 h-16 text-slate-700 mb-4" />
          <p className="text-slate-500">
            Teaching plan will appear here after visualization starts
          </p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ x: 300, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="w-96 h-full bg-slate-900/50 backdrop-blur-xl border-l border-slate-800 overflow-y-auto"
    >
      <div className="p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-white mb-2">Teaching Plan</h2>
          <p className="text-sm text-slate-400">{teachingPlan.topic}</p>
        </div>

        <div className="space-y-4">
          <AnimatePresence>
            {teachingPlan.steps.map((step, index) => {
              const isActive = index === currentStep && !isVideoCompleted;
              const isCompleted = index < currentStep || (isVideoCompleted && index === teachingPlan.steps.length - 1);

              return (
                <motion.div
                  key={step.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`p-4 rounded-xl border transition-all ${
                    isActive
                      ? 'bg-blue-500/10 border-blue-500/50'
                      : isCompleted
                      ? 'bg-green-500/10 border-green-500/50'
                      : 'bg-slate-800/30 border-slate-700'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 mt-1">
                      {isCompleted ? (
                        <CheckCircle2 className="w-5 h-5 text-green-400" />
                      ) : isActive ? (
                        <motion.div
                          animate={{ scale: [1, 1.2, 1] }}
                          transition={{ repeat: Infinity, duration: 2 }}
                        >
                          <Circle className="w-5 h-5 text-blue-400 fill-blue-400" />
                        </motion.div>
                      ) : (
                        <Circle className="w-5 h-5 text-slate-600" />
                      )}
                    </div>
                    <div className="flex-1">
                      <h3 className={`font-medium mb-1 ${
                        isActive
                          ? 'text-blue-300'
                          : isCompleted
                          ? 'text-green-300'
                          : 'text-slate-400'
                      }`}>
                        {step.title}
                      </h3>
                      <p className="text-sm text-slate-500">{step.description}</p>
                      <p className="text-xs text-slate-600 mt-2">
                        @ {Math.floor(step.timestamp / 60)}:{String(step.timestamp % 60).padStart(2, '0')}
                      </p>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>

        <div className="mt-6 p-4 bg-slate-800/50 rounded-lg">
          <p className="text-xs text-slate-400 mb-2">Estimated Duration</p>
          <p className="text-lg font-semibold text-white">
            {Math.floor(teachingPlan.estimatedDuration / 60)} min {teachingPlan.estimatedDuration % 60} sec
          </p>
        </div>
      </div>
    </motion.div>
  );
}
