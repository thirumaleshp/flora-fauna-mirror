"""
Test Supabase Connection
"""
import streamlit as st
from supabase import create_client, Client

def test_supabase_connection():
    try:
        # Get credentials from secrets
        url = "https://zbwvjaqvqfdywxxpsekd.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpid3ZqYXF2cWZkeXd4eHBzZWtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMwMzk0NTAsImV4cCI6MjA2ODYxNTQ1MH0.xcXGJHBFYp6Aj77ZNJTjD8L6EWZ5ErJ-iDzDGhK2yAw"
        
        # Create client
        supabase: Client = create_client(url, key)
        
        # Test connection by trying to select from a simple table
        print("✅ Supabase client created successfully!")
        print(f"📡 Connected to: {url}")
        
        # Try to check if our table exists
        try:
            result = supabase.table("collected_data").select("id", count="exact").limit(1).execute()
            print("✅ Table 'collected_data' exists and is accessible!")
            print(f"📊 Current record count: {result.count}")
            return True
        except Exception as table_error:
            print("⚠️ Table 'collected_data' doesn't exist yet. This is normal for new projects.")
            print("🛠️ You'll need to create the table first.")
            print(f"Error details: {table_error}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Supabase Connection...")
    success = test_supabase_connection()
    if success:
        print("🎉 Supabase is ready to use!")
    else:
        print("🔧 Setup required - see instructions below.")
