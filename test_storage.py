"""
Quick test to check if Supabase Storage upload works
"""

from supabase import create_client, Client
import streamlit as st

def test_supabase_storage():
    try:
        # Get credentials
        supabase_url = st.secrets.supabase.url
        supabase_key = st.secrets.supabase.key
        
        # Create client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Test content
        test_content = b"Test image content"
        
        # Try upload
        response = supabase.storage.from_("images").upload(
            path="test/test.jpg",
            file=test_content,
            file_options={"content-type": "image/jpeg", "upsert": True}
        )
        
        if response:
            url = supabase.storage.from_("images").get_public_url("test/test.jpg")
            print(f"✅ Upload successful: {url}")
            
            # Cleanup
            supabase.storage.from_("images").remove(["test/test.jpg"])
            return True
        else:
            print("❌ Upload failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Supabase Storage...")
    test_supabase_storage()
