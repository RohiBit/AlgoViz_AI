import { useState, useRef } from 'react';
import { Sidebar } from './Sidebar';
import { InputZone } from './InputZone';
import { VisualizationCanvas } from './VisualizationCanvas';
import { apiService } from '../services/api';
import { TopicItem, RenderTask, InputMode, CodeInput } from '../types';

export function Dashboard() {
  const [selectedTopic, setSelectedTopic] = useState<TopicItem | null>(null);
  const [renderTask, setRenderTask] = useState<RenderTask | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const handleTopicSelect = (topic: TopicItem) => {
    setSelectedTopic(topic);
    setRenderTask(null);
  };

  const handleVisualize = async (input: string, mode: InputMode, codeInput?: CodeInput) => {
    setIsProcessing(true);

    try {
      // Generate plan and render video
      const plan = await apiService.generatePlan(input, mode === 'code' ? 'code' : 'text');
      
      const { task } = await apiService.startRenderTask(plan);
      
      // Poll for task completion
      const progressInterval = setInterval(async () => {
        try {
          const updatedTask = await apiService.getTaskStatus(task.id);
          setRenderTask(updatedTask);

          if (updatedTask.status === 'completed' || updatedTask.progress >= 100) {
            clearInterval(progressInterval);
            setRenderTask({ ...updatedTask, status: 'completed', progress: 100 });
            setIsProcessing(false);
          }
        } catch (error) {
          console.error('Error checking task status:', error);
        }
      }, 2000);

      // Fallback timeout
      setTimeout(() => {
        clearInterval(progressInterval);
        setRenderTask(prev => prev ? { ...prev, status: 'completed', progress: 100 } : null);
        setIsProcessing(false);
      }, 30000);
    } catch (error) {
      console.error('Visualization error:', error);
      setIsProcessing(false);
    }
  };

  const handleUploadImage = async (file: File) => {
    setIsProcessing(true);
    try {
      const result = await apiService.uploadVision(file);
      
      const task: RenderTask = {
        id: result.taskId,
        status: result.status === 'completed' ? 'completed' : 'processing',
        progress: result.status === 'completed' ? 100 : 50,
        videoUrl: result.videoUrl,
        teachingPlanId: result.taskId,
        createdAt: new Date().toISOString()
      };
      setRenderTask(task);
      
      if (result.status !== 'completed') {
        const progressInterval = setInterval(async () => {
          try {
            const updatedTask = await apiService.getTaskStatus(result.taskId);
            setRenderTask(updatedTask);
            if (updatedTask.status === 'completed' || updatedTask.progress >= 100) {
              clearInterval(progressInterval);
              setRenderTask({ ...updatedTask, status: 'completed', progress: 100 });
              setIsProcessing(false);
            }
          } catch (error) {
            console.error('Error checking task status:', error);
          }
        }, 2000);
        setTimeout(() => { 
          clearInterval(progressInterval); 
          setIsProcessing(false); 
        }, 60000); // Longer timeout for vision processing
      } else {
        setIsProcessing(false);
      }
    } catch (error) {
      console.error('Image upload error:', error);
      setIsProcessing(false);
    }
  };

  const handleVideoLoaded = (video: HTMLVideoElement) => {
    videoRef.current = video;
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <Sidebar onTopicSelect={handleTopicSelect} selectedTopic={selectedTopic} />
      
      <div className="flex-1 flex flex-col overflow-y-auto p-6 gap-6">
        {/* Extended Input Zone */}
        <InputZone 
          onVisualize={handleVisualize} 
          onUploadImage={handleUploadImage} 
          isProcessing={isProcessing} 
        />
        
        {/* Extended Visualization Canvas */}
        <VisualizationCanvas 
          renderTask={renderTask} 
          onVideoLoaded={handleVideoLoaded}
        />
      </div>
    </div>
  );
}
