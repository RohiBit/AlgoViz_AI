export interface TeachingPlanStep {
  id: string;
  title: string;
  description: string;
  timestamp: number;
  status: 'pending' | 'active' | 'completed';
}

export interface TeachingPlan {
  id: string;
  topic: string;
  steps: TeachingPlanStep[];
  estimatedDuration: number;
  createdAt: string;
}

export interface RenderTask {
  id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress: number;
  videoUrl?: string;
  teachingPlanId: string;
  createdAt: string;
}

export interface PipelineStep {
  id: string;
  label: string;
  status: 'pending' | 'in_progress' | 'completed' | 'error';
  icon: string;
}

export type InputMode = 'text' | 'code' | 'file';

export type TopicCategory = 'data-structures' | 'algorithms' | 'ml-fundamentals';

export interface TopicItem {
  id: string;
  name: string;
  category: TopicCategory;
  description: string;
}

export interface CodeInput {
  language: 'python' | 'cpp';
  code: string;
}
