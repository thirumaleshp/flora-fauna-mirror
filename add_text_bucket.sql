-- Add Text Bucket to Existing Supabase Project
-- Run this in your Supabase SQL Editor to add text file storage

-- Create text storage bucket
INSERT INTO storage.buckets (id, name, public) 
VALUES ('texts', 'texts', true)
ON CONFLICT (id) DO NOTHING;

-- Create storage policy for text bucket
CREATE POLICY IF NOT EXISTS "Public Access Texts" ON storage.objects 
FOR ALL TO public 
USING (bucket_id = 'texts');

-- Verify the bucket was created
SELECT 'Text bucket created successfully' as status;
SELECT id, name, public FROM storage.buckets WHERE id = 'texts';
