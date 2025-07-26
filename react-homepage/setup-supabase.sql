-- React + Supabase Homepage Database Setup
-- Run this script in your Supabase SQL Editor to set up the required tables

-- 1. Create posts table
CREATE TABLE IF NOT EXISTS posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  content TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Insert sample data
INSERT INTO posts (title, content) VALUES
('Welcome to our homepage', 'This is our first post showcasing the Supabase integration. You can customize this content or add your own posts through the Supabase dashboard.'),
('React + Supabase = Amazing', 'Building modern web apps has never been easier with this powerful combination. React provides the interactive frontend while Supabase handles the backend infrastructure.'),
('Getting Started Guide', 'Follow our comprehensive guide to set up your own project like this one. Check out the README file for detailed instructions.'),
('Responsive Design', 'This homepage is built with mobile-first responsive design principles using Tailwind CSS, ensuring it looks great on all devices.'),
('Real-time Updates', 'Supabase provides real-time capabilities out of the box. You can easily add real-time features to your application as it grows.')
ON CONFLICT DO NOTHING;

-- 3. Enable Row Level Security (recommended for production)
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- 4. Create a policy to allow public read access to posts
CREATE POLICY IF NOT EXISTS "Posts are publicly readable" ON posts
  FOR SELECT USING (true);

-- 5. Create a policy to allow authenticated users to insert posts (optional)
-- Uncomment the following lines if you want to allow authenticated users to create posts
-- CREATE POLICY IF NOT EXISTS "Users can insert posts" ON posts
--   FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- 6. Create a policy to allow authenticated users to update their own posts (optional)
-- Uncomment the following lines if you want to allow users to edit posts
-- CREATE POLICY IF NOT EXISTS "Users can update own posts" ON posts
--   FOR UPDATE USING (auth.uid() = user_id)
--   WITH CHECK (auth.uid() = user_id);

-- Note: If you want to add user ownership to posts, you can add a user_id column:
-- ALTER TABLE posts ADD COLUMN user_id UUID REFERENCES auth.users(id);

-- Success message
SELECT 'Database setup completed successfully! Your React homepage is ready to display posts.' as message;