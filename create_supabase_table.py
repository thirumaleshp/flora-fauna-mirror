"""
Create Supabase Table
This script will create the required table in your Supabase database
"""
from supabase import create_client, Client

def create_supabase_table():
    try:
        # Get credentials
        url = "https://zbwvjaqvqfdywxxpsekd.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpid3ZqYXF2cWZkeXd4eHBzZWtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMwMzk0NTAsImV4cCI6MjA2ODYxNTQ1MH0.xcXGJHBFYp6Aj77ZNJTjD8L6EWZ5ErJ-iDzDGhK2yAw"
        
        # Create client
        supabase: Client = create_client(url, key)
        
        # SQL to create the table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS collected_data (
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
        """
        
        print("🏗️ Creating table 'collected_data' in Supabase...")
        
        # Execute the SQL using the rpc function
        # Note: This requires the SQL to be executed via the Supabase dashboard or CLI
        # The Python client doesn't directly support DDL operations
        
        print("⚠️ Please create the table manually in your Supabase dashboard:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Open your project: zbwvjaqvqfdywxxpsekd")
        print("3. Go to 'SQL Editor' or 'Table Editor'")
        print("4. Run this SQL:")
        print("\n" + "="*60)
        print(create_table_sql)
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_supabase_table()
