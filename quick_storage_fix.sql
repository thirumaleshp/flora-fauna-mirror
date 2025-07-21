-- Quick Storage Setup - Run this in Supabase SQL Editor
-- This creates the storage buckets and policies needed for file uploads

-- Create the three storage buckets
INSERT INTO storage.buckets (id, name, public) 
VALUES 
('images', 'images', true),
('audios', 'audios', true), 
('videos', 'videos', true)
ON CONFLICT (id) DO NOTHING;

-- Create simple public policies for all buckets
CREATE POLICY IF NOT EXISTS "Public Access All" ON storage.objects 
FOR ALL TO public 
USING (true);

-- Verify buckets were created
SELECT id, name, public FROM storage.buckets;
