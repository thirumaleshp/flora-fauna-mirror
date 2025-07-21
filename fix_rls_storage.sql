-- Fix for Supabase Storage RLS when buckets are already public
-- Run this in your Supabase SQL Editor

-- Option 1: Disable RLS entirely on storage.objects (simplest solution)
ALTER TABLE storage.objects DISABLE ROW LEVEL SECURITY;

-- Option 2: If you prefer to keep RLS enabled, create permissive policies
-- (Only use if Option 1 doesn't work or you want to keep RLS)

/*
-- Enable RLS
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Drop all existing policies first
DROP POLICY IF EXISTS "Public Access" ON storage.objects;
DROP POLICY IF EXISTS "Public uploads and access" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated uploads" ON storage.objects;
DROP POLICY IF EXISTS "Public read access" ON storage.objects;
DROP POLICY IF EXISTS "Public upload access" ON storage.objects;

-- Create a single permissive policy for all operations
CREATE POLICY "Allow all for public buckets" ON storage.objects
FOR ALL 
TO public
USING (bucket_id IN ('images', 'audios', 'videos'))
WITH CHECK (bucket_id IN ('images', 'audios', 'videos'));
*/

-- Check current policies (for debugging)
-- SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
-- FROM pg_policies WHERE tablename = 'objects' AND schemaname = 'storage';
