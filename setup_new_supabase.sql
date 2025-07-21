-- Database Setup for Flora & Fauna Data Collection
-- Run this in your NEW Supabase project's SQL Editor

-- 1. Create the main data table
CREATE TABLE data_entries (
    id SERIAL PRIMARY KEY,
    entry_type VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    file_path VARCHAR(500),
    file_url VARCHAR(500),
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    location_name VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- 2. Enable Row Level Security
ALTER TABLE data_entries ENABLE ROW LEVEL SECURITY;

-- 3. Create policy to allow all operations for your team
CREATE POLICY "Allow all operations" ON data_entries
FOR ALL 
TO public
USING (true)
WITH CHECK (true);

-- 4. Create storage buckets for files
INSERT INTO storage.buckets (id, name, public) VALUES 
('images', 'images', true),
('audios', 'audios', true),
('videos', 'videos', true);

-- 5. Create storage policies for public access
CREATE POLICY "Public Access Images" ON storage.objects 
FOR ALL TO public 
USING (bucket_id = 'images');

CREATE POLICY "Public Access Audios" ON storage.objects 
FOR ALL TO public 
USING (bucket_id = 'audios');

CREATE POLICY "Public Access Videos" ON storage.objects 
FOR ALL TO public 
USING (bucket_id = 'videos');

-- 6. Verify setup
SELECT 'Tables created successfully' as status;
SELECT bucket_id, count(*) as policy_count 
FROM storage.objects 
GROUP BY bucket_id;
