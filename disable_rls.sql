-- Disable Row Level Security (RLS) for Supabase Storage
-- This is the simplest and most effective solution

-- Disable RLS on the storage.objects table
ALTER TABLE storage.objects DISABLE ROW LEVEL SECURITY;

-- Optional: Also disable RLS on storage.buckets if needed
ALTER TABLE storage.buckets DISABLE ROW LEVEL SECURITY;

-- Verify RLS is disabled (this will show you the current status)
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'storage' 
AND tablename IN ('objects', 'buckets');
