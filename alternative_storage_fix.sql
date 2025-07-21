-- Alternative approach for Supabase Storage permissions
-- This should work with regular user permissions

-- Method 1: Create policies without modifying table structure
-- First, let's create a policy that allows all operations for public buckets

INSERT INTO storage.policies (name, bucket_id, policy_for, check_expression)
VALUES 
  ('Allow public uploads', 'images', 'INSERT', 'true'),
  ('Allow public uploads', 'audios', 'INSERT', 'true'),
  ('Allow public uploads', 'videos', 'INSERT', 'true'),
  ('Allow public reads', 'images', 'SELECT', 'true'),
  ('Allow public reads', 'audios', 'SELECT', 'true'),
  ('Allow public reads', 'videos', 'SELECT', 'true')
ON CONFLICT (name, bucket_id, policy_for) DO NOTHING;

-- Method 2: If the above doesn't work, try this simpler approach
-- Update bucket configuration to be fully public
UPDATE storage.buckets 
SET 
  public = true,
  file_size_limit = NULL,
  allowed_mime_types = NULL
WHERE name IN ('images', 'audios', 'videos');
