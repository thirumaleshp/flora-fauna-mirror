"""
Cloud Database Configuration
Supports multiple cloud database providers
"""
import os
import streamlit as st
from typing import Optional, Dict, Any
import json

class DatabaseConfig:
    """Manage cloud database configurations"""
    
    @staticmethod
    def get_supabase_config():
        """Get Supabase configuration"""
        return {
            'url': st.secrets.get("SUPABASE_URL", ""),
            'key': st.secrets.get("SUPABASE_ANON_KEY", ""),
            'service_key': st.secrets.get("SUPABASE_SERVICE_KEY", "")
        }
    
    @staticmethod
    def get_mongodb_config():
        """Get MongoDB Atlas configuration"""
        return {
            'connection_string': st.secrets.get("MONGODB_CONNECTION_STRING", ""),
            'database_name': st.secrets.get("MONGODB_DATABASE", "flora_fauna_db")
        }
    
    @staticmethod
    def get_airtable_config():
        """Get Airtable configuration"""
        return {
            'api_key': st.secrets.get("AIRTABLE_API_KEY", ""),
            'base_id': st.secrets.get("AIRTABLE_BASE_ID", ""),
            'table_name': st.secrets.get("AIRTABLE_TABLE_NAME", "collected_data")
        }
    
    @staticmethod
    def get_firebase_config():
        """Get Firebase configuration"""
        return {
            'credentials': st.secrets.get("FIREBASE_CREDENTIALS", {}),
            'project_id': st.secrets.get("FIREBASE_PROJECT_ID", "")
        }

class CloudDatabaseSelector:
    """Select and initialize cloud database"""
    
    PROVIDERS = {
        "Supabase (PostgreSQL)": "supabase",
        "MongoDB Atlas": "mongodb", 
        "Airtable": "airtable",
        "Firebase Firestore": "firebase",
        "Local SQLite (Fallback)": "sqlite"
    }
    
    @classmethod
    def get_available_providers(cls):
        """Get list of configured providers"""
        available = []
        
        # Check Supabase
        supabase_config = DatabaseConfig.get_supabase_config()
        if supabase_config['url'] and supabase_config['key']:
            available.append("Supabase (PostgreSQL)")
        
        # Check MongoDB
        mongodb_config = DatabaseConfig.get_mongodb_config()
        if mongodb_config['connection_string']:
            available.append("MongoDB Atlas")
        
        # Check Airtable
        airtable_config = DatabaseConfig.get_airtable_config()
        if airtable_config['api_key'] and airtable_config['base_id']:
            available.append("Airtable")
        
        # Check Firebase
        firebase_config = DatabaseConfig.get_firebase_config()
        if firebase_config['credentials'] and firebase_config['project_id']:
            available.append("Firebase Firestore")
        
        # SQLite is always available as fallback
        available.append("Local SQLite (Fallback)")
        
        return available
    
    @classmethod
    def show_setup_instructions(cls, provider: str):
        """Show setup instructions for each provider"""
        if provider == "Supabase (PostgreSQL)":
            st.info("""
            **🟢 Supabase Setup Instructions:**
            
            1. **Create Account**: Go to [supabase.com](https://supabase.com) and create a free account
            2. **Create Project**: Click "New Project" and choose a database password
            3. **Get API Keys**: Go to Settings → API → Copy your URL and anon key
            4. **Add to Secrets**: In Streamlit Cloud, add these secrets:
               ```
               SUPABASE_URL = "your-project-url"
               SUPABASE_ANON_KEY = "your-anon-key"
               ```
            
            **✅ Benefits**: Real-time updates, PostgreSQL power, generous free tier (500MB)
            """)
        
        elif provider == "MongoDB Atlas":
            st.info("""
            **🔵 MongoDB Atlas Setup Instructions:**
            
            1. **Create Account**: Go to [mongodb.com/atlas](https://mongodb.com/atlas) 
            2. **Create Cluster**: Choose free M0 cluster
            3. **Setup Access**: Create database user and whitelist IP addresses
            4. **Get Connection String**: Click "Connect" → "Connect your application"
            5. **Add to Secrets**: In Streamlit Cloud, add:
               ```
               MONGODB_CONNECTION_STRING = "mongodb+srv://username:password@cluster.mongodb.net/"
               MONGODB_DATABASE = "flora_fauna_db"
               ```
            
            **✅ Benefits**: Document storage, flexible schema, 512MB free
            """)
        
        elif provider == "Airtable":
            st.info("""
            **🟠 Airtable Setup Instructions:**
            
            1. **Create Account**: Go to [airtable.com](https://airtable.com)
            2. **Create Base**: Create a new base with a table for your data
            3. **Get API Key**: Go to Account → Generate API key
            4. **Get Base ID**: From your base URL: `https://airtable.com/BASE_ID/...`
            5. **Add to Secrets**: In Streamlit Cloud, add:
               ```
               AIRTABLE_API_KEY = "your-api-key"
               AIRTABLE_BASE_ID = "your-base-id"
               AIRTABLE_TABLE_NAME = "collected_data"
               ```
            
            **✅ Benefits**: Spreadsheet interface, easy to use, good for non-technical users
            """)
        
        elif provider == "Firebase Firestore":
            st.info("""
            **🟡 Firebase Setup Instructions:**
            
            1. **Create Project**: Go to [console.firebase.google.com](https://console.firebase.google.com)
            2. **Enable Firestore**: Go to Firestore Database → Create database
            3. **Create Service Account**: Go to Project Settings → Service accounts → Generate key
            4. **Add to Secrets**: In Streamlit Cloud, add the entire JSON as:
               ```
               FIREBASE_CREDENTIALS = {your-service-account-json}
               FIREBASE_PROJECT_ID = "your-project-id"
               ```
            
            **✅ Benefits**: Real-time sync, Google integration, generous free tier
            """)
