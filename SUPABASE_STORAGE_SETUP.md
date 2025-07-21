"""
🌐 Supabase Storage Setup Guide

This guide will help you set up Supabase Storage to view uploaded images directly in Supabase.
"""

# Method 1: Using Supabase Dashboard (Recommended)

## Step 1: Create Storage Buckets in Supabase Dashboard

1. **Go to your Supabase project dashboard**
   - Visit: https://supabase.com/dashboard
   - Select your project

2. **Navigate to Storage**
   - Click on "Storage" in the left sidebar
   - Click "Create a new bucket"

3. **Create these buckets:**

   **For Images:**
   - Bucket name: `images`
   - Make it public: ✅ Yes
   - Allowed MIME types: `image/jpeg, image/png, image/gif, image/webp, image/bmp`
   
   **For Audio:**
   - Bucket name: `audios`
   - Make it public: ✅ Yes
   - Allowed MIME types: `audio/mpeg, audio/wav, audio/ogg, audio/mp3, audio/m4a`
   
   **For Videos:**
   - Bucket name: `videos`
   - Make it public: ✅ Yes
   - Allowed MIME types: `video/mp4, video/avi, video/mov, video/wmv, video/webm`

## Step 2: Update Your App (Automatic)

Your app is already configured to:
- ✅ Upload files to Supabase Storage
- ✅ Store file URLs in the database
- ✅ Display images from Supabase Storage URLs

## Step 3: Test the Setup

1. **Upload a new image** in your app
2. **Check the View Data tab** - you should see "☁️ Cloud Stored" for new uploads
3. **Click "View"** to see the image displayed from Supabase Storage
4. **Visit your Supabase Storage dashboard** to see the uploaded files

---

# Method 2: Using SQL in Supabase (Alternative)

If you prefer SQL, run these commands in your Supabase SQL Editor:

```sql
-- Enable Storage (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "storage" SCHEMA "extensions";

-- Create storage buckets
INSERT INTO storage.buckets (id, name, public) VALUES 
('images', 'images', true),
('audios', 'audios', true), 
('videos', 'videos', true);

-- Set up RLS policies for public access
CREATE POLICY "Public Access" ON storage.objects
FOR ALL USING (bucket_id IN ('images', 'audios', 'videos'));
```

---

# How to View Images in Supabase

## Option 1: Through Your App (Recommended)
1. Go to "📈 View Collected Data" tab
2. Find an image record with "☁️ Cloud Stored" indicator
3. Click "👁️ View" to see the image preview
4. The image loads directly from Supabase Storage

## Option 2: Through Supabase Dashboard
1. Go to Storage → images bucket in your Supabase dashboard
2. Click on any uploaded image to view it
3. Use the "Copy URL" button to get the direct link

## Option 3: Direct URL Access
- Images are accessible via public URLs like:
- `https://your-project.supabase.co/storage/v1/object/public/images/your-image.jpg`

---

# Current Status

✅ **App Features Ready:**
- File upload with cloud storage
- Metadata stored in database
- File URLs stored for easy access
- Image preview from cloud URLs
- Local fallback for existing files

⚠️ **Setup Required:**
- Create storage buckets in Supabase (Steps above)
- Test with a new image upload

🎯 **Next Steps:**
1. Create the storage buckets
2. Upload a new image to test
3. Enjoy viewing images directly from Supabase!

---

**Note:** Existing files uploaded before setting up Supabase Storage will remain as local files. New uploads will automatically go to Supabase Storage once buckets are created.
