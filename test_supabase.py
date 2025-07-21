#!/usr/bin/env python3
"""
Test Supabase connection and table structure
"""
import streamlit as st
from supabase import create_client

# Read secrets
url = st.secrets.get("SUPABASE_URL", "")
key = st.secrets.get("SUPABASE_ANON_KEY", "")

if url and key:
    print(f"✅ Supabase URL: {url}")
    print(f"✅ Supabase Key: {key[:20]}...")
    
    # Create client
    supabase = create_client(url, key)
    
    # Test connection by checking tables
    try:
        # Check if data_entries table exists
        response = supabase.table("data_entries").select("*", count="exact").limit(1).execute()
        print(f"✅ data_entries table exists with {response.count} records")
        
        # Check storage buckets
        buckets = supabase.storage.list_buckets()
        print(f"✅ Storage buckets: {[b.name for b in buckets]}")
        
        # Test insert
        test_record = {
            "entry_type": "test",
            "title": "test_connection",
            "content": "Testing connection",
            "file_path": "test.txt",
            "file_url": None,
            "location_name": "Test Location"
        }
        
        insert_response = supabase.table("data_entries").insert(test_record).execute()
        if insert_response.data:
            print(f"✅ Test insert successful: ID {insert_response.data[0]['id']}")
            
            # Clean up test record
            supabase.table("data_entries").delete().eq("entry_type", "test").execute()
            print("✅ Test record cleaned up")
        else:
            print("❌ Test insert failed")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        
else:
    print("❌ Supabase credentials not found")
