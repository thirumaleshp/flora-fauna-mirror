"""
Unified Database Manager
Handles multiple database providers with a unified interface
"""
import streamlit as st
import pandas as pd
import datetime
import sqlite3
import json
from typing import Optional, Dict, Any, Union

class UnifiedDatabaseManager:
    """Unified interface for different database providers"""
    
    def __init__(self):
        self.current_provider = "Local SQLite (Fallback)"
        self.sqlite_db_path = "data/flora_fauna.db"
        self._init_sqlite()
    
    def _init_sqlite(self):
        """Initialize SQLite database as fallback"""
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collected_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                data_type TEXT NOT NULL,
                filename TEXT NOT NULL,
                category TEXT,
                description TEXT,
                tags TEXT,
                file_size INTEGER,
                original_name TEXT,
                duration REAL,
                resolution TEXT,
                latitude REAL,
                longitude REAL,
                city TEXT,
                region TEXT,
                country TEXT,
                location_method TEXT,
                additional_info TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_active_manager(self):
        """Get the currently active database manager"""
        provider = st.session_state.get('selected_db_provider', 'Local SQLite (Fallback)')
        
        try:
            if provider == "Supabase (PostgreSQL)":
                from supabase_db import supabase_manager
                if supabase_manager.is_available():
                    return supabase_manager, "supabase"
                    
            elif provider == "MongoDB Atlas":
                from mongodb_atlas import mongodb_manager
                if mongodb_manager.is_available():
                    return mongodb_manager, "mongodb"
            
            # Fallback to SQLite
            return self, "sqlite"
            
        except ImportError:
            return self, "sqlite"
    
    def save_data(self, data_type: str, filename: str, file_data: bytes = None, 
                  additional_info: Dict = None, location_data: Dict = None, uploaded_file = None) -> Optional[Union[int, str]]:
        """Save data using the active database provider"""
        manager, provider_type = self.get_active_manager()
        
        # For Supabase, set the uploaded file for cloud storage
        if provider_type == "supabase" and uploaded_file and hasattr(manager, 'set_current_file'):
            manager.set_current_file(uploaded_file)
        
        if provider_type == "sqlite":
            return self._save_to_sqlite(data_type, filename, file_data, additional_info, location_data)
        else:
            return manager.save_data(data_type, filename, file_data, additional_info, location_data)
    
    def _save_to_sqlite(self, data_type: str, filename: str, file_data: bytes = None, 
                        additional_info: Dict = None, location_data: Dict = None) -> Optional[int]:
        """Save data to SQLite database"""
        try:
            conn = sqlite3.connect(self.sqlite_db_path)
            cursor = conn.cursor()
            
            # Extract location information
            latitude = longitude = city = region = country = location_method = None
            if location_data:
                if 'coordinates' in location_data:
                    latitude = location_data['coordinates'].get('latitude')
                    longitude = location_data['coordinates'].get('longitude')
                city = location_data.get('city')
                region = location_data.get('region')
                country = location_data.get('country')
                location_method = location_data.get('detection_method')
            
            # Extract additional info
            category = description = tags = duration = resolution = original_name = None
            file_size = 0
            if additional_info:
                category = additional_info.get('category')
                description = additional_info.get('description')
                tags_list = additional_info.get('tags', [])
                tags = ','.join(tags_list) if tags_list else None
                duration = additional_info.get('duration')
                resolution = additional_info.get('resolution')
                original_name = additional_info.get('original_name')
                file_size = additional_info.get('file_size', 0)
            
            # Insert main data record
            cursor.execute('''
                INSERT INTO collected_data 
                (timestamp, data_type, filename, category, description, tags, file_size, 
                 original_name, duration, resolution, latitude, longitude, city, region, 
                 country, location_method, additional_info)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.datetime.now().isoformat(),
                data_type,
                filename,
                category,
                description,
                tags,
                file_size,
                original_name,
                duration,
                resolution,
                latitude,
                longitude,
                city,
                region,
                country,
                location_method,
                json.dumps(additional_info) if additional_info else None
            ))
            
            data_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return data_id
            
        except Exception as e:
            st.error(f"❌ SQLite save error: {str(e)}")
            return None
    
    def get_all_data(self) -> pd.DataFrame:
        """Get all data using the active database provider"""
        manager, provider_type = self.get_active_manager()
        
        if provider_type == "sqlite":
            return self._get_sqlite_data()
        else:
            return manager.get_all_data()
    
    def _get_sqlite_data(self) -> pd.DataFrame:
        """Get all data from SQLite"""
        try:
            conn = sqlite3.connect(self.sqlite_db_path)
            df = pd.read_sql_query('''
                SELECT id, timestamp, data_type, filename, category, description, tags,
                       file_size, original_name, duration, resolution, latitude, longitude,
                       city, region, country, location_method, created_at
                FROM collected_data
                ORDER BY created_at DESC
            ''', conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"❌ SQLite fetch error: {str(e)}")
            return pd.DataFrame()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics using the active provider"""
        manager, provider_type = self.get_active_manager()
        
        if provider_type == "sqlite":
            return self._get_sqlite_stats()
        else:
            return manager.get_statistics()
    
    def _get_sqlite_stats(self) -> Dict[str, Any]:
        """Get SQLite database statistics"""
        try:
            conn = sqlite3.connect(self.sqlite_db_path)
            cursor = conn.cursor()
            
            # Count by data type
            cursor.execute('SELECT data_type, COUNT(*) FROM collected_data GROUP BY data_type')
            type_counts = dict(cursor.fetchall())
            
            # Total records
            cursor.execute('SELECT COUNT(*) FROM collected_data')
            total_records = cursor.fetchone()[0]
            
            # Database size
            try:
                import os
                db_size = os.path.getsize(self.sqlite_db_path) if os.path.exists(self.sqlite_db_path) else 0
            except Exception:
                db_size = 0
            
            conn.close()
            
            return {
                'total_records': total_records,
                'type_counts': type_counts,
                'db_size': db_size
            }
        except Exception as e:
            st.error(f"❌ SQLite stats error: {str(e)}")
            return {'total_records': 0, 'type_counts': {}, 'db_size': 0}
    
    def get_provider_info(self) -> Dict[str, str]:
        """Get information about the current database provider"""
        manager, provider_type = self.get_active_manager()
        provider_name = st.session_state.get('selected_db_provider', 'Local SQLite (Fallback)')
        
        info = {
            'name': provider_name,
            'type': provider_type,
            'status': 'connected' if manager else 'unavailable'
        }
        
        if provider_type == "sqlite":
            info['description'] = "Local SQLite database file"
            info['location'] = self.sqlite_db_path
        elif provider_type == "supabase":
            info['description'] = "Cloud PostgreSQL database (Supabase)"
            info['location'] = "Cloud hosted"
        elif provider_type == "mongodb":
            info['description'] = "Cloud MongoDB Atlas database"
            info['location'] = "Cloud hosted"
        
        return info

# Global unified database manager
db_manager = UnifiedDatabaseManager()
