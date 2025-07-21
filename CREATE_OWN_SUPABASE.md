# Create Your Own Supabase Project for Cloud Storage

## Why You Need Your Own Project
The current Supabase project has restrictions that prevent cloud file storage. To enable full cloud functionality for your team, you need to create your own Supabase project where you have admin rights.

## Step-by-Step Setup

### 1. Create New Supabase Project
1. Go to https://supabase.com
2. Sign up/Login with your account
3. Click "New Project"
4. Choose your organization
5. Enter project details:
   - Name: `flora-fauna-data-collection`
   - Database Password: Create a strong password (save it!)
   - Region: Choose closest to your location
6. Click "Create new project"
7. Wait 2-3 minutes for project setup

### 2. Get Your New Credentials
1. In your new project dashboard, go to Settings → API
2. Copy these values:
   - **Project URL** (looks like: https://xxxxx.supabase.co)
   - **anon/public key** (starts with eyJhbGciOiJIUzI1NiIs...)

### 3. Update Your App
1. Open `.streamlit/secrets.toml` in your project
2. Replace with your new credentials:
```toml
SUPABASE_URL = "https://YOUR_NEW_PROJECT_URL.supabase.co"
SUPABASE_ANON_KEY = "YOUR_NEW_ANON_KEY"
```

### 4. Set Up Database Tables
Run this SQL in your Supabase SQL Editor (Dashboard → SQL Editor):

```sql
-- Create the data_entries table
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

-- Enable Row Level Security
ALTER TABLE data_entries ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (for your team)
CREATE POLICY "Allow all operations" ON data_entries
FOR ALL 
TO public
USING (true)
WITH CHECK (true);
```

### 5. Set Up Storage Buckets
Run this SQL to create storage buckets:

```sql
-- Create storage buckets
INSERT INTO storage.buckets (id, name, public) VALUES 
('images', 'images', true),
('audios', 'audios', true),
('videos', 'videos', true);

-- Create storage policies for public access
CREATE POLICY "Public Access" ON storage.objects FOR ALL TO public USING (true);
```

### 6. Enable Cloud Storage in App
Once you've updated your credentials, I'll modify the app to re-enable Supabase Storage uploads.

## Benefits of Your Own Project
- ✅ Full admin control
- ✅ True cloud storage for all files
- ✅ Team can access from anywhere
- ✅ No storage limitations
- ✅ Professional setup for internship

## Team Access
Once set up, your team can access the app with:
- The deployed Streamlit URL
- All data stored in the cloud
- Images/files accessible via public URLs
- Real-time collaboration

Let me know when you've created your project and updated the credentials!
                                                                                                                                                                                                                                                                                                                                            