"""
Simple script to create Supabase Storage buckets
"""

import streamlit as st
from supabase import create_client, Client

def create_storage_buckets():
    """Create storage buckets in Supabase"""
    try:
        # Get credentials from Streamlit secrets
        supabase_url = st.secrets.supabase.url
        supabase_key = st.secrets.supabase.key
        
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Buckets to create
        buckets = ["images", "audios", "videos"]
        
        st.write("🚀 Creating storage buckets...")
        
        for bucket_name in buckets:
            try:
                # Check if bucket exists
                existing_buckets = supabase.storage.list_buckets()
                bucket_exists = any(b.name == bucket_name for b in existing_buckets)
                
                if bucket_exists:
                    st.success(f"✅ Bucket '{bucket_name}' already exists")
                else:
                    # Create bucket
                    supabase.storage.create_bucket(bucket_name, {"public": True})
                    st.success(f"✅ Created bucket: {bucket_name}")
                
            except Exception as e:
                st.error(f"❌ Error with bucket '{bucket_name}': {e}")
        
        st.success("🎉 Storage setup complete! You can now upload files to Supabase Storage.")
        return True
        
    except Exception as e:
        st.error(f"❌ Failed to create buckets: {e}")
        return False

if __name__ == "__main__":
    st.title("🗂️ Supabase Storage Setup")
    
    if st.button("Create Storage Buckets"):
        create_storage_buckets()
