-- Simple Storage Permissions Fix for Supabase
-- Run this in your Supabase SQL Editor

-- First, let's create a simple policy that allows public access
-- This should work with regular user permissions

-- Create policy for public read access to storage buckets
INSERT INTO storage.policies (name, bucket_id, policy_for, check_expression)
VALUES 
  ('Public Read', 'images', 'SELECT', 'true'),
  ('Public Read', 'audios', 'SELECT', 'true'),
  ('Public Read', 'videos', 'SELECT', 'true');

-- Create policy for public upload access
INSERT INTO storage.policies (name, bucket_id, policy_for, check_expression)
VALUES 
  ('Public Upload', 'images', 'INSERT', 'true'),
  ('Public Upload', 'audios', 'INSERT', 'true'),
  ('Public Upload', 'videos', 'INSERT', 'true');

-- Alternative: If the above doesn't work, try this simpler approach
-- Update bucket configuration to allow public access
UPDATE storage.buckets 
SET public = true 
WHERE name IN ('images', 'audios', 'videos');
