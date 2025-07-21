-- COMPLETE SETUP SCRIPT for Your New Supabase Project
-- Copy and paste this ENTIRE script into your Supabase SQL Editor and run it

-- 1. Create the data_entries table
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

-- 3. Create policy to allow all operations (for your team)
CREATE POLICY "Allow all operations" ON data_entries
FOR ALL 
TO public
USING (true)
WITH CHECK (true);

-- 4. Create storage buckets for files
INSERT INTO storage.buckets (id, name, public) VALUES 
('images', 'images', true),
('audios', 'audios', true),
('videos', 'videos', true),
('texts', 'texts', true);

-- 5. Create storage policies for public access
CREATE POLICY "Public Access All" ON storage.objects 
FOR ALL TO public 
USING (true);

-- 6. Verify setup (run this to check everything worked)
SELECT 'Database table created successfully' as status;
SELECT 'Storage buckets:' as info, id, name, public FROM storage.buckets;
