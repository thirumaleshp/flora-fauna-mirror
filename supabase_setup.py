"""
Supabase Setup and Table Creation Script
"""
import streamlit as st
from supabase import create_client, Client

def main():
    st.title("🔧 Supabase Setup & Table Creation")
    
    st.info("""
    This script will help you:
    1. ✅ Verify your Supabase connection
    2. 🏗️ Create the required table
    3. 🧪 Test data insertion
    """)
    
    # Connection test
    st.subheader("1. 🔗 Testing Connection")
    
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
        
        supabase: Client = create_client(url, key)
        st.success("✅ Supabase connection successful!")
        st.write(f"📡 Connected to: {url}")
        
    except Exception as e:
        st.error(f"❌ Connection failed: {e}")
        st.stop()
    
    # Table creation
    st.subheader("2. 🏗️ Create Table")
    
    st.warning("""
    **Important:** You need to create the table manually in your Supabase dashboard.
    
    **Steps:**
    1. Go to [supabase.com/dashboard](https://supabase.com/dashboard)
    2. Open your project
    3. Click "SQL Editor" in the sidebar
    4. Copy and run the SQL below:
    """)
    
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
    file_data TEXT,
    mime_type TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Grant permissions
ALTER TABLE collected_data ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable all operations for all users" ON collected_data FOR ALL USING (true);
    """
    
    st.code(create_table_sql, language="sql")
    
    # Test table existence
    st.subheader("3. 🧪 Test Table")
    
    if st.button("Test Table Existence"):
        try:
            result = supabase.table("collected_data").select("id", count="exact").limit(1).execute()
            st.success("✅ Table 'collected_data' exists and is accessible!")
            st.write(f"📊 Current record count: {result.count}")
            
            # Test insert
            st.subheader("4. 📝 Test Data Insert")
            if st.button("Test Insert Sample Data"):
                test_data = {
                    "data_type": "test",
                    "filename": "test_file.txt",
                    "category": "test_category",
                    "description": "This is a test record",
                    "file_size": 100
                }
                
                insert_result = supabase.table("collected_data").insert(test_data).execute()
                if insert_result.data:
                    st.success("✅ Test data inserted successfully!")
                    st.json(insert_result.data[0])
                else:
                    st.error("❌ Failed to insert test data")
                    
        except Exception as e:
            st.error(f"❌ Table test failed: {e}")
            st.warning("Please create the table using the SQL above in your Supabase dashboard.")

if __name__ == "__main__":
    main()
