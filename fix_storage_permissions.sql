/*
Run this SQL in your Supabase SQL Editor to fix storage permissions
Go to: Supabase Dashboard > SQL Editor > New Query > Paste this code > Run
*/

-- Enable Row Level Security on storage.objects (if not already enabled)
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist (ignore errors if they don't exist)
DROP POLICY IF EXISTS "Public Access" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated uploads" ON storage.objects;
DROP POLICY IF EXISTS "Public uploads" ON storage.objects;

-- Create a simple policy for public access to our buckets
CREATE POLICY "Public uploads and access" ON storage.objects
FOR ALL 
USING (bucket_id IN ('images', 'audios', 'videos'))
WITH CHECK (bucket_id IN ('images', 'audios', 'videos'));

-- Alternative: If you want separate policies for read and write
-- Uncomment these and comment out the above policy

/*
-- Allow public read access
CREATE POLICY "Public read access" ON storage.objects
FOR SELECT 
USING (bucket_id IN ('images', 'audios', 'videos'));

-- Allow public upload
CREATE POLICY "Public upload access" ON storage.objects
FOR INSERT 
WITH CHECK (bucket_id IN ('images', 'audios', 'videos'));

-- Allow public update/delete (optional)
CREATE POLICY "Public modify access" ON storage.objects
FOR UPDATE 
USING (bucket_id IN ('images', 'audios', 'videos'))
WITH CHECK (bucket_id IN ('images', 'audios', 'videos'));

CREATE POLICY "Public delete access" ON storage.objects
FOR DELETE 
USING (bucket_id IN ('images', 'audios', 'videos'));
*/
