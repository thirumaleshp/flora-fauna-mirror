# 🌐 Cloud Database Setup Guide

This application supports multiple cloud database providers for persistent data storage. Choose the one that best fits your needs:

## 🟢 Supabase (PostgreSQL) - **Recommended**

**Why Supabase?**
- Free tier: 500MB database, 2GB bandwidth
- Real-time updates
- Built-in authentication
- Easy to use dashboard

**Setup Steps:**
1. Go to [supabase.com](https://supabase.com) and create an account
2. Create a new project
3. Go to **Settings** → **API** in your project dashboard
4. Copy your **Project URL** and **anon key**
5. Create the table in your database:

```sql
CREATE TABLE collected_data (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    data_type TEXT NOT NULL,
    filename TEXT NOT NULL,
    category TEXT,
    description TEXT,
    tags TEXT,
    file_size BIGINT,
    original_name TEXT,
    duration REAL,
    resolution TEXT,
    latitude REAL,
    longitude REAL,
    city TEXT,
    region TEXT,
    country TEXT,
    location_method TEXT,
    additional_info JSONB,
    file_data BYTEA,
    mime_type TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

6. Add to your Streamlit secrets:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
```

## 🔵 MongoDB Atlas

**Why MongoDB Atlas?**
- Free tier: 512MB storage
- Flexible document structure
- Global clusters
- Rich query capabilities

**Setup Steps:**
1. Go to [mongodb.com/atlas](https://mongodb.com/atlas) and create account
2. Create a free M0 cluster
3. Create a database user with read/write permissions
4. Whitelist your IP address (or use 0.0.0.0/0 for all IPs)
5. Get your connection string from **Connect** → **Connect your application**
6. Add to your Streamlit secrets:
```toml
MONGODB_CONNECTION_STRING = "mongodb+srv://username:password@cluster.mongodb.net/"
MONGODB_DATABASE = "flora_fauna_db"
```

## 🟠 Airtable

**Why Airtable?**
- Spreadsheet-like interface
- Easy data viewing and editing
- Good for non-technical users
- Free tier: 1,200 records per base

**Setup Steps:**
1. Go to [airtable.com](https://airtable.com) and create account
2. Create a new base with a table named "collected_data"
3. Get your API key from [airtable.com/create/tokens](https://airtable.com/create/tokens)
4. Get your base ID from the URL or API documentation
5. Add to your Streamlit secrets:
```toml
AIRTABLE_API_KEY = "your-api-key"
AIRTABLE_BASE_ID = "your-base-id"
AIRTABLE_TABLE_NAME = "collected_data"
```

## 🟡 Firebase Firestore

**Why Firebase?**
- Google Cloud integration
- Real-time synchronization
- Generous free tier
- Strong security rules

**Setup Steps:**
1. Go to [console.firebase.google.com](https://console.firebase.google.com)
2. Create a new project
3. Enable Firestore Database
4. Go to **Project Settings** → **Service Accounts**
5. Generate a new private key (downloads JSON file)
6. Add the JSON contents to your Streamlit secrets:
```toml
FIREBASE_PROJECT_ID = "your-project-id"
[FIREBASE_CREDENTIALS]
# Paste the contents of your service account JSON here
```

## 🚀 Quick Start

1. **Install Dependencies:**
```bash
pip install supabase pymongo pyairtable firebase-admin
```

2. **Configure Secrets:**
   - Copy `secrets.template.toml` to `.streamlit/secrets.toml`
   - Fill in your credentials for chosen provider(s)
   - For Streamlit Cloud: Add secrets in app settings

3. **Run Application:**
```bash
streamlit run app.py
```

4. **Select Database:**
   - Use the sidebar to choose your database provider
   - The app will automatically connect and create tables

## 🔧 Local Development

For local development, create `.streamlit/secrets.toml`:
```toml
# Choose your provider and add credentials
SUPABASE_URL = "your-url"
SUPABASE_ANON_KEY = "your-key"
```

## ☁️ Streamlit Cloud Deployment

1. Push your code to GitHub (without secrets!)
2. Deploy on [share.streamlit.io](https://share.streamlit.io)
3. In app settings, add your secrets under "Secrets"
4. The app will automatically use cloud database

## 🛡️ Security Best Practices

- **Never commit credentials** to version control
- Add `.streamlit/secrets.toml` to `.gitignore`
- Use **read-only keys** when possible
- **Rotate credentials** regularly
- **Monitor usage** to avoid unexpected charges

## 🔍 Troubleshooting

**Database not connecting?**
- Check credentials are correct
- Verify IP whitelist settings
- Ensure required permissions are granted

**Data not saving?**
- Check table structure matches requirements
- Verify write permissions
- Check for quota limits

**Need help?**
- Check the setup guide in the app sidebar
- Review provider documentation
- Check Streamlit logs for error messages

## 📊 Comparison Table

| Provider | Free Tier | Best For | Complexity |
|----------|-----------|----------|------------|
| Supabase | 500MB | General use, real-time | Low |
| MongoDB | 512MB | Flexible data, scaling | Medium |
| Airtable | 1,200 records | Non-technical users | Low |
| Firebase | 1GB | Google ecosystem | Medium |

## 🎯 Recommendation

For most users, **Supabase** is recommended because:
- Easy setup and configuration
- Generous free tier
- Real-time capabilities
- Strong PostgreSQL foundation
- Good documentation and community

Choose MongoDB Atlas if you need flexible document storage or plan to scale significantly.
