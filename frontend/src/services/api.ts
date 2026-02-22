import axios from 'axios';
import { TeachingPlan, RenderTask, PipelineStep } from '../types';

// Create axios client for FastAPI backend
const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  async generatePlan(input: string, mode: 'text' | 'code'): Promise<TeachingPlan> {
    try {
      // Call FastAPI /generate-plan endpoint
      const response = await apiClient.post('/generate-plan', {
        topic: input,
        intent: mode,
        user_input: input
      });
      
      const planData = response.data;
      
      // Convert backend response to TeachingPlan format
      const plan: TeachingPlan = {
        id: planData.task_id,
        topic: planData.topic,
        steps: planData.steps,
        estimatedDuration: planData.estimatedDuration,
        createdAt: new Date().toISOString()
      };
      
      return plan;
    } catch (error) {
      console.error('Error generating plan:', error);
      throw error;
    }
  },

  async startRenderTask(plan: TeachingPlan): Promise<{ task: RenderTask; updatedPlan?: TeachingPlan }> {
    try {
      // Call FastAPI /render endpoint with the plan
      const response = await apiClient.post('/render', {
        task_id: plan.id,
        topic: plan.topic,
        steps: plan.steps
      });
      
      const renderData = response.data;
      
      // Return render task with the task ID
      const taskId = renderData.celery_task_id || renderData.task_id;
      const task: RenderTask = {
        id: taskId,
        status: renderData.status === 'completed' ? 'completed' : 'queued',
        progress: renderData.status === 'completed' ? 100 : 0,
        teachingPlanId: plan.id,
        createdAt: new Date().toISOString()
      };
      
      // Check if there's an updated plan with actual timestamps
      let updatedPlan: TeachingPlan | undefined;
      if (renderData.plan) {
        updatedPlan = {
          id: renderData.plan.task_id || plan.id,
          topic: renderData.plan.topic || plan.topic,
          steps: renderData.plan.steps || plan.steps,
          estimatedDuration: renderData.plan.estimatedDuration || plan.estimatedDuration,
          createdAt: renderData.plan.createdAt || plan.createdAt
        };
      }
      
      return { task, updatedPlan };
    } catch (error) {
      console.error('Error starting render task:', error);
      throw error;
    }
  },

  async getTaskStatus(taskId: string): Promise<RenderTask> {
    try {
      // Call FastAPI /task-status/{task_id} endpoint
      const response = await apiClient.get(`/task-status/${taskId}`);
      
      const statusData = response.data;
      
      // Map backend status to RenderTask status
      let status: 'queued' | 'processing' | 'completed' | 'failed' = 'processing';
      let progress = 0;
      
      if (statusData.status === 'SUCCESS') {
        status = 'completed';
        progress = 100;
      } else if (statusData.status === 'FAILURE') {
        status = 'failed';
        progress = 0;
      } else if (statusData.status === 'PENDING') {
        status = 'queued';
        progress = 0;
      } else {
        status = 'processing';
        progress = 50;
      }
      
      const task: RenderTask = {
        id: taskId,
        status,
        progress,
        videoUrl: status === 'completed' ? `http://localhost:8000/media/${taskId}.mp4` : undefined,
        teachingPlanId: 'unknown',
        createdAt: new Date().toISOString()
      };
      
      return task;
    } catch (error) {
      console.error('Error getting task status:', error);
      throw error;
    }
  },

  async uploadVision(file: File): Promise<{ taskId: string; videoUrl: string; status: string }> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      // Call FastAPI /upload-vision endpoint
      const response = await apiClient.post('/upload-vision', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      const data = response.data;
      
      // Return the task info
      return {
        taskId: data.task_id,
        videoUrl: data.video_url ? `http://localhost:8000/${data.video_url}` : '',
        status: data.status
      };
    } catch (error) {
      console.error('Error uploading vision:', error);
      throw error;
    }
  },

  getPipelineSteps(): PipelineStep[] {
    return [
      {
        id: 'step_1',
        label: 'LLM Identifying Intent',
        status: 'pending',
        icon: 'brain'
      },
      {
        id: 'step_2',
        label: 'Fetching Ground Truth from Knowledge Base',
        status: 'pending',
        icon: 'database'
      },
      {
        id: 'step_3',
        label: 'Generating Teaching Plan',
        status: 'pending',
        icon: 'file-text'
      },
      {
        id: 'step_4',
        label: 'Triggering Manim Worker',
        status: 'pending',
        icon: 'play-circle'
      }
    ];
  },

  async getPipelineStatus(taskId: string): Promise<PipelineStep[]> {
    try {
      // Call FastAPI /pipeline-status/{task_id} endpoint
      const response = await apiClient.get(`/pipeline-status/${taskId}`);
      
      const statusData = response.data;
      
      // Convert backend pipeline stages to PipelineStep format
      const steps: PipelineStep[] = statusData.stages.map((stage: any) => ({
        id: `step_${stage.id}`,
        label: stage.label,
        status: stage.status === 'completed' ? 'completed' : 
               stage.status === 'in_progress' ? 'in_progress' : 
               stage.status === 'error' ? 'error' : 'pending',
        icon: stage.id === 1 ? 'brain' : 
              stage.id === 2 ? 'database' : 
              stage.id === 3 ? 'file-text' : 'play-circle'
      }));
      
      return steps;
    } catch (error) {
      console.error('Error getting pipeline status:', error);
      return this.getPipelineSteps();
    }
  }
};
