"""
Supabase Storage Setup Script
This script will help you create storage buckets in Supabase for images, audio, and video files.
"""

import os
import sys
from supabase import create_client, Client
import streamlit as st

def setup_supabase_storage():
    """Set up Supabase Storage buckets"""
    
    # Get credentials from Streamlit secrets or environment
    try:
        if hasattr(st, 'secrets') and 'supabase' in st.secrets:
            supabase_url = st.secrets.supabase.url
            supabase_key = st.secrets.supabase.key
        else:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Error: Supabase credentials not found")
            print("Please add SUPABASE_URL and SUPABASE_KEY to:")
            print("- Streamlit secrets (.streamlit/secrets.toml)")
            print("- Environment variables")
            return False
        
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase")
        
        # Buckets to create
        buckets = [
            {
                "id": "images",
                "name": "images",
                "public": True,
                "allowed_mime_types": ["image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp"]
            },
            {
                "id": "audios", 
                "name": "audios",
                "public": True,
                "allowed_mime_types": ["audio/mpeg", "audio/wav", "audio/ogg", "audio/mp3", "audio/m4a"]
            },
            {
                "id": "videos",
                "name": "videos", 
                "public": True,
                "allowed_mime_types": ["video/mp4", "video/avi", "video/mov", "video/wmv", "video/webm"]
            }
        ]
        
        # Create buckets
        for bucket in buckets:
            try:
                # Check if bucket exists
                existing_buckets = supabase.storage.list_buckets()
                bucket_exists = any(b.name == bucket["id"] for b in existing_buckets)
                
                if bucket_exists:
                    print(f"📁 Bucket '{bucket['id']}' already exists")
                else:
                    # Create bucket
                    response = supabase.storage.create_bucket(
                        bucket["id"],
                        options={
                            "public": bucket["public"],
                            "allowed_mime_types": bucket["allowed_mime_types"]
                        }
                    )
                    print(f"✅ Created bucket: {bucket['id']}")
                
            except Exception as e:
                print(f"⚠️ Error with bucket '{bucket['id']}': {e}")
        
        print("\n🎉 Supabase Storage setup complete!")
        print("\nNext steps:")
        print("1. Your app can now upload files to Supabase Storage")
        print("2. File URLs will be stored in your database")
        print("3. Images will be viewable directly in the app and Supabase dashboard")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def test_storage_upload():
    """Test storage upload with a sample file"""
    try:
        if hasattr(st, 'secrets') and 'supabase' in st.secrets:
            supabase_url = st.secrets.supabase.url
            supabase_key = st.secrets.supabase.key
        else:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
        
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Test with a simple text file
        test_content = b"This is a test file for Supabase Storage"
        storage_path = "test/test_file.txt"
        
        # Upload test file
        response = supabase.storage.from_("images").upload(
            path=storage_path,
            file=test_content,
            file_options={
                "content-type": "text/plain",
                "upsert": True
            }
        )
        
        if response:
            # Get public URL
            public_url = supabase.storage.from_("images").get_public_url(storage_path)
            print(f"✅ Test upload successful!")
            print(f"🔗 Public URL: {public_url}")
            
            # Clean up test file
            supabase.storage.from_("images").remove([storage_path])
            print("🧹 Test file cleaned up")
            
            return True
        else:
            print("❌ Test upload failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up Supabase Storage...")
    print("=" * 50)
    
    # Setup storage buckets
    if setup_supabase_storage():
        print("\n" + "=" * 50)
        print("🧪 Testing storage upload...")
        test_storage_upload()
    
    print("\n" + "=" * 50)
    print("✨ Setup complete!")
