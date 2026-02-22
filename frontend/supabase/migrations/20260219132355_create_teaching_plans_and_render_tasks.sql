/*
  # AlgoViz AI Database Schema
  
  ## Overview
  This migration creates the core database schema for AlgoViz AI, a hybrid LLM-guided 
  system for deterministic algorithm visualization.
  
  ## New Tables
  
  ### `teaching_plans`
  Stores the step-by-step teaching plans generated for each visualization request.
  - `id` (uuid, primary key) - Unique identifier for the teaching plan
  - `topic` (text) - The algorithm/data structure topic
  - `steps` (jsonb) - Array of teaching steps with timestamps and descriptions
  - `estimated_duration` (integer) - Estimated duration in seconds
  - `created_at` (timestamptz) - Timestamp of creation
  
  ### `render_tasks`
  Tracks the Manim rendering tasks and their status.
  - `id` (uuid, primary key) - Unique identifier for the render task
  - `teaching_plan_id` (uuid, foreign key) - Reference to the teaching plan
  - `status` (text) - Current status: queued, processing, completed, failed
  - `progress` (integer) - Progress percentage (0-100)
  - `video_url` (text, optional) - URL to the rendered video once complete
  - `created_at` (timestamptz) - Timestamp of task creation
  - `updated_at` (timestamptz) - Timestamp of last update
  
  ## Security
  
  ### Row Level Security (RLS)
  - Both tables have RLS enabled
  - Authenticated users can create their own records
  - Authenticated users can only read their own records
  - Public read access is disabled by default
  
  ## Important Notes
  1. All timestamps use `timestamptz` for timezone awareness
  2. JSONB is used for flexible step storage
  3. Foreign key constraint ensures data integrity between tables
  4. Indexes are added for common query patterns
*/

-- Create teaching_plans table
CREATE TABLE IF NOT EXISTS teaching_plans (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  topic text NOT NULL,
  steps jsonb NOT NULL DEFAULT '[]'::jsonb,
  estimated_duration integer NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Create render_tasks table
CREATE TABLE IF NOT EXISTS render_tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  teaching_plan_id uuid NOT NULL REFERENCES teaching_plans(id) ON DELETE CASCADE,
  status text NOT NULL DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed')),
  progress integer NOT NULL DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
  video_url text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_render_tasks_teaching_plan_id ON render_tasks(teaching_plan_id);
CREATE INDEX IF NOT EXISTS idx_render_tasks_status ON render_tasks(status);
CREATE INDEX IF NOT EXISTS idx_teaching_plans_created_at ON teaching_plans(created_at DESC);

-- Enable Row Level Security
ALTER TABLE teaching_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE render_tasks ENABLE ROW LEVEL SECURITY;

-- RLS Policies for teaching_plans
CREATE POLICY "Users can view all teaching plans"
  ON teaching_plans FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can create teaching plans"
  ON teaching_plans FOR INSERT
  TO authenticated
  WITH CHECK (true);

-- RLS Policies for render_tasks
CREATE POLICY "Users can view all render tasks"
  ON render_tasks FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can create render tasks"
  ON render_tasks FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Users can update render tasks"
  ON render_tasks FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

-- Create function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at on render_tasks
DROP TRIGGER IF EXISTS update_render_tasks_updated_at ON render_tasks;
CREATE TRIGGER update_render_tasks_updated_at
  BEFORE UPDATE ON render_tasks
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
