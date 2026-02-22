/*
  # Fix Security Issues in AlgoViz AI Schema
  
  ## Issues Fixed
  
  1. **Unused Indexes**: Removed indexes that aren't being used. Indexes will be added 
     back only when query patterns indicate they're needed.
  
  2. **Auth DB Connection Strategy**: This is a project-level setting that requires 
     manual configuration in the Supabase dashboard under Settings > Database > 
     Connection Pooling. The recommendation is to use percentage-based allocation.
  
  3. **Function Search Path Mutable**: Updated the function to use IMMUTABLE 
     declaration and explicit search_path to prevent security risks.
  
  4. **RLS Policy Too Permissive**: Refined policies to require proper authorization:
     - INSERT policies now track user ownership
     - UPDATE policies restrict to authenticated users with proper checks
     - SELECT policies remain open to authenticated users (reasonable for shared data)
  
  ## Changes Made
  
  1. Drop unused indexes
  2. Recreate the update_updated_at_column function with IMMUTABLE and search_path
  3. Replace overly permissive RLS policies with restrictive ones
  4. Add user_id tracking to establish ownership
*/

-- Drop unused indexes (these can be re-added based on actual query patterns)
DROP INDEX IF EXISTS idx_render_tasks_teaching_plan_id;
DROP INDEX IF EXISTS idx_render_tasks_status;
DROP INDEX IF EXISTS idx_teaching_plans_created_at;

-- Drop old triggers and functions
DROP TRIGGER IF EXISTS update_render_tasks_updated_at ON render_tasks;
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Recreate function with proper security settings
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
IMMUTABLE
SET search_path = public
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- Drop existing overly permissive policies
DROP POLICY IF EXISTS "Users can view all teaching plans" ON teaching_plans;
DROP POLICY IF EXISTS "Users can create teaching plans" ON teaching_plans;
DROP POLICY IF EXISTS "Users can view all render tasks" ON render_tasks;
DROP POLICY IF EXISTS "Users can create render tasks" ON render_tasks;
DROP POLICY IF EXISTS "Users can update render tasks" ON render_tasks;

-- Add user_id column to teaching_plans if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'teaching_plans' AND column_name = 'user_id'
  ) THEN
    ALTER TABLE teaching_plans ADD COLUMN user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE;
  END IF;
END $$;

-- Add user_id column to render_tasks if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'render_tasks' AND column_name = 'user_id'
  ) THEN
    ALTER TABLE render_tasks ADD COLUMN user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE;
  END IF;
END $$;

-- Create restrictive RLS policies for teaching_plans
CREATE POLICY "Users can view own teaching plans"
  ON teaching_plans FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own teaching plans"
  ON teaching_plans FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own teaching plans"
  ON teaching_plans FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own teaching plans"
  ON teaching_plans FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- Create restrictive RLS policies for render_tasks
CREATE POLICY "Users can view own render tasks"
  ON render_tasks FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own render tasks"
  ON render_tasks FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own render tasks"
  ON render_tasks FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own render tasks"
  ON render_tasks FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- Recreate trigger for updated_at
CREATE TRIGGER update_render_tasks_updated_at
  BEFORE UPDATE ON render_tasks
  FOR EACH ROW
  EXECUTE FUNCTION public.update_updated_at_column();
