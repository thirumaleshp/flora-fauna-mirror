# Team Setup Guide for Flora & Fauna Data Collection App

## 🎯 Project Overview
Multi-media data collection application with cloud storage for team collaboration.

## 🔧 Setup Instructions

### For Project Owner (You):

1. **Create Supabase Project**
   - Go to https://supabase.com
   - Create new project: "flora-fauna-data"
   - Note down Project URL and anon key

2. **Update App Configuration**
   - Edit `.streamlit/secrets.toml`
   - Replace URL and key with your new project
   - Run the setup in your app to create tables and storage

3. **Share with Team**
   - Give team members the Project URL and anon key
   - Share this setup guide

### For Team Members:

1. **Clone/Download the App**
   - Get the app files from project owner
   - Install dependencies: `pip install -r requirements.txt`

2. **Configure Secrets**
   - Create `.streamlit/secrets.toml` file
   - Add the Supabase credentials provided by project owner

3. **Run the App**
   - `streamlit run app.py`
   - Test upload functionality

## 🗂️ Storage Structure

- **Database**: Metadata stored in Supabase PostgreSQL
- **Files**: Images, audio, video stored in Supabase Storage
- **Buckets**: `images`, `audios`, `videos` (auto-created)

## 📊 Features Available

- ✅ Multi-format file uploads (images, audio, video, text)
- ✅ Location tracking and metadata
- ✅ Real-time data viewing and analytics
- ✅ Data export (CSV, JSON)
- ✅ Team collaboration with shared cloud storage

## 🔐 Security

- All team members use the same anon key (read/write access)
- Files are publicly accessible via URLs (suitable for team projects)
- Database has RLS disabled for easy team access

## 🆘 Troubleshooting

- If uploads fail: Check internet connection and Supabase status
- If data not visible: Refresh the "View Collected Data" section
- If setup issues: Contact project owner

## 📞 Support

Contact project owner for:
- Credential sharing
- Setup assistance
- Access issues
