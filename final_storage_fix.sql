-- Final solution: Make buckets completely public without RLS
-- This should work with any permission level

-- Method 1: Update bucket settings (most likely to work)
UPDATE storage.buckets 
SET 
  public = true,
  file_size_limit = NULL,
  allowed_mime_types = NULL
WHERE name IN ('images', 'audios', 'videos');

-- Method 2: If you have access to bucket creation, recreate them as public
-- (Only run if Method 1 doesn't work)

/*
-- Drop and recreate buckets as fully public
DROP TABLE IF EXISTS storage.buckets WHERE name IN ('images', 'audios', 'videos');

-- Create new public buckets
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES 
  ('images', 'images', true, NULL, NULL),
  ('audios', 'audios', true, NULL, NULL),
  ('videos', 'videos', true, NULL, NULL)
ON CONFLICT (id) DO UPDATE SET
  public = true,
  file_size_limit = NULL,
  allowed_mime_types = NULL;
*/
