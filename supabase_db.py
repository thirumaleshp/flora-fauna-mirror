"""
Supabase Database Integration
Cloud PostgreSQL database for persistent storage
"""
import streamlit as st
import pandas as pd
import datetime
import json
from typing import Optional, Dict, Any, List

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

class SupabaseManager:
    """Manage Supabase database operations"""
    
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.table_name = "collected_data"
        self._initialize()
    
    def _initialize(self):
        """Initialize Supabase client"""
        if not SUPABASE_AVAILABLE:
            return
        
        try:
            # Get credentials from Streamlit secrets
            url = st.secrets.get("SUPABASE_URL", "")
            key = st.secrets.get("SUPABASE_ANON_KEY", "")
            
            if url and key:
                self.supabase = create_client(url, key)
                self._create_table_if_not_exists()
            else:
                st.warning("🔑 Supabase credentials not found in secrets. Please configure SUPABASE_URL and SUPABASE_ANON_KEY")
        except Exception as e:
            st.error(f"❌ Failed to initialize Supabase: {str(e)}")
    
    def _create_table_if_not_exists(self):
        """Create the table if it doesn't exist"""
        if not self.supabase:
            return
        
        try:
            # Check if table exists by trying to count rows
            response = self.supabase.table("data_entries").select("id", count="exact").limit(1).execute()
            st.success(f"✅ Connected to Supabase! Table 'data_entries' is ready.")
        except Exception as e:
            # Table might not exist, show instructions to create it
            st.warning(f"""
            🏗️ **Table Setup Required**
            
            Please create the table in your Supabase database by running the SQL script: `setup_new_supabase.sql`
            
            Or manually run this SQL in your Supabase SQL Editor:
            ```sql
            CREATE TABLE data_entries (
                id SERIAL PRIMARY KEY,
                entry_type VARCHAR(20) NOT NULL,
                title VARCHAR(255) NOT NULL,
                content TEXT,
                file_path VARCHAR(500),
                file_url VARCHAR(500),
                location_lat DECIMAL(10, 8),
                location_lng DECIMAL(11, 8),
                location_name VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB
            );
            ```
            """)
    
    def is_available(self) -> bool:
        """Check if Supabase is available and configured"""
        return SUPABASE_AVAILABLE and self.supabase is not None
    
    def upload_file_to_storage(self, uploaded_file, bucket: str) -> Optional[str]:
        """Upload file to Supabase Storage and return public URL"""
        if not self.is_available():
            return None
        
        try:
            # Create unique filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = uploaded_file.name.split('.')[-1] if '.' in uploaded_file.name else ''
            file_name = f"{timestamp}_{uploaded_file.name}"
            
            # Upload file to Supabase Storage
            response = self.supabase.storage.from_(bucket).upload(
                file_name, 
                uploaded_file.getvalue(),
                file_options={"content-type": uploaded_file.type}
            )
            
            if response:
                # Get public URL
                public_url = self.supabase.storage.from_(bucket).get_public_url(file_name)
                return public_url
            else:
                st.error(f"Failed to upload {uploaded_file.name} to cloud storage")
                return None
                
        except Exception as e:
            st.error(f"Cloud storage error: {str(e)}")
            return None

    def upload_text_to_storage(self, text_content: str, filename: str) -> Optional[str]:
        """Upload text content to Supabase Storage as a text file"""
        if not self.is_available():
            return None
        
        try:
            # Create text file content
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{timestamp}_{filename}"
            
            # Convert text to bytes
            text_bytes = text_content.encode('utf-8')
            
            # Upload to texts bucket
            response = self.supabase.storage.from_('texts').upload(
                file_name, 
                text_bytes,
                file_options={"content-type": "text/plain"}
            )
            
            if response:
                # Get public URL
                public_url = self.supabase.storage.from_('texts').get_public_url(file_name)
                return public_url
            else:
                st.error(f"Failed to upload text to cloud storage")
                return None
                
        except Exception as e:
            st.error(f"Text cloud storage error: {str(e)}")
            return None

    def save_data(self, data_type: str, filename: str, file_data: bytes = None, 
                  additional_info: Dict = None, location_data: Dict = None) -> Optional[int]:
        """Save data to Supabase"""
        if not self.is_available():
            return None
        
        try:
            # Upload file to cloud storage
            file_url = None
            
            # Handle text data differently
            if data_type == 'text' and additional_info and additional_info.get('content'):
                # For text data, upload content as text file
                text_content = additional_info.get('content')
                file_url = self.upload_text_to_storage(text_content, filename)
            
            elif file_data and hasattr(self, '_current_uploaded_file'):
                # For other file types, upload the file
                bucket_mapping = {
                    'image': 'images',
                    'audio': 'audios', 
                    'video': 'videos'
                }
                bucket = bucket_mapping.get(data_type, 'images')
                file_url = self.upload_file_to_storage(self._current_uploaded_file, bucket)
            
            # Prepare data for insertion
            record = {
                "entry_type": data_type,
                "title": filename,
                "content": additional_info.get("content", "") if additional_info else "",  # Store actual text content
                "file_path": filename,  # Local filename for reference
                "file_url": file_url,   # Cloud storage URL
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Add location data
            if location_data:
                if 'coordinates' in location_data:
                    record["location_lat"] = location_data['coordinates'].get('latitude')
                    record["location_lng"] = location_data['coordinates'].get('longitude')
                record["location_name"] = f"{location_data.get('city', '')}, {location_data.get('country', '')}"
            
            # Add additional metadata
            if additional_info:
                record["metadata"] = additional_info
            
            # Insert data
            response = self.supabase.table("data_entries").insert(record).execute()
            
            if response.data:
                return response.data[0]['id']
            else:
                return None
                
        except Exception as e:
            st.error(f"❌ Supabase save error: {str(e)}")
            return None

    def set_current_file(self, uploaded_file):
        """Set the current uploaded file for storage operations"""
        self._current_uploaded_file = uploaded_file
    
    def get_all_data(self) -> pd.DataFrame:
        """Get all data from Supabase"""
        if not self.is_available():
            return pd.DataFrame()
        
        try:
            response = self.supabase.table("data_entries").select("*").order("timestamp", desc=True).execute()
            
            if response.data:
                df = pd.DataFrame(response.data)
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"❌ Supabase fetch error: {str(e)}")
            return pd.DataFrame()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.is_available():
            return {'total_records': 0, 'type_counts': {}, 'db_size': 0}
        
        try:
            # Get total count
            total_response = self.supabase.table("data_entries").select("id", count="exact").execute()
            total_records = total_response.count if total_response.count else 0
            
            # Get type counts
            type_response = self.supabase.table("data_entries").select("entry_type").execute()
            type_counts = {}
            if type_response.data:
                for record in type_response.data:
                    entry_type = record['entry_type']
                    type_counts[entry_type] = type_counts.get(entry_type, 0) + 1
            
            return {
                'total_records': total_records,
                'type_counts': type_counts,
                'db_size': total_records * 1024  # Rough estimate
            }
            
        except Exception as e:
            st.error(f"❌ Supabase stats error: {str(e)}")
            return {'total_records': 0, 'type_counts': {}, 'db_size': 0}
    
    def delete_record(self, record_id: int) -> bool:
        """Delete a record by ID"""
        if not self.is_available():
            return False
        
        try:
            self.supabase.table("data_entries").delete().eq("id", record_id).execute()
            return True
        except Exception as e:
            st.error(f"❌ Delete error: {str(e)}")
            return False
    
    def update_record(self, record_id: int, updates: Dict[str, Any]) -> bool:
        """Update a record by ID"""
        if not self.is_available():
            return False
        
        try:
            self.supabase.table("data_entries").update(updates).eq("id", record_id).execute()
            return True
        except Exception as e:
            st.error(f"❌ Update error: {str(e)}")
            return False

# Global instance
supabase_manager = SupabaseManager()
