-- Simple fix to make storage buckets public
-- Run this in Supabase SQL Editor

-- Make the buckets public
UPDATE storage.buckets 
SET public = true 
WHERE name IN ('images', 'audios', 'videos');

-- Alternative: If you want to check current bucket status first
-- SELECT name, public FROM storage.buckets WHERE name IN ('images', 'audios', 'videos');
