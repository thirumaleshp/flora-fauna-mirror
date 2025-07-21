"""
MongoDB Atlas Integration
Cloud MongoDB database for persistent storage
"""
import streamlit as st
import pandas as pd
import datetime
from typing import Optional, Dict, Any
import json

try:
    from pymongo import MongoClient
    from bson import ObjectId
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

class MongoDBManager:
    """Manage MongoDB Atlas database operations"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        self.collection = None
        self.database_name = "flora_fauna_db"
        self.collection_name = "collected_data"
        self._initialize()
    
    def _initialize(self):
        """Initialize MongoDB client"""
        if not MONGODB_AVAILABLE:
            return
        
        try:
            # Get credentials from Streamlit secrets
            connection_string = st.secrets.get("MONGODB_CONNECTION_STRING", "")
            database_name = st.secrets.get("MONGODB_DATABASE", self.database_name)
            
            if connection_string:
                self.client = MongoClient(connection_string)
                self.db = self.client[database_name]
                self.collection = self.db[self.collection_name]
                
                # Test connection
                self.client.admin.command('ping')
                st.success(f"✅ Connected to MongoDB Atlas! Database: {database_name}")
            else:
                st.warning("🔑 MongoDB credentials not found. Please configure MONGODB_CONNECTION_STRING")
        except Exception as e:
            st.error(f"❌ Failed to initialize MongoDB: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if MongoDB is available and configured"""
        return MONGODB_AVAILABLE and self.client is not None
    
    def save_data(self, data_type: str, filename: str, file_data: bytes = None, 
                  additional_info: Dict = None, location_data: Dict = None) -> Optional[str]:
        """Save data to MongoDB"""
        if not self.is_available():
            return None
        
        try:
            # Prepare document for insertion
            document = {
                "timestamp": datetime.datetime.now(),
                "data_type": data_type,
                "filename": filename,
                "file_data": file_data if file_data else None,
                "mime_type": f"{data_type}/*" if file_data else None
            }
            
            # Add additional info
            if additional_info:
                document.update({
                    "category": additional_info.get("category"),
                    "description": additional_info.get("description"),
                    "tags": additional_info.get("tags", []),
                    "file_size": additional_info.get("file_size"),
                    "original_name": additional_info.get("original_name"),
                    "duration": additional_info.get("duration"),
                    "resolution": additional_info.get("resolution"),
                    "additional_info": additional_info
                })
            
            # Add location data
            if location_data:
                location_doc = location_data.copy()
                if 'coordinates' in location_data:
                    location_doc["latitude"] = location_data['coordinates'].get('latitude')
                    location_doc["longitude"] = location_data['coordinates'].get('longitude')
                document["location"] = location_doc
            
            # Insert document
            result = self.collection.insert_one(document)
            return str(result.inserted_id)
                
        except Exception as e:
            st.error(f"❌ MongoDB save error: {str(e)}")
            return None
    
    def get_all_data(self) -> pd.DataFrame:
        """Get all data from MongoDB"""
        if not self.is_available():
            return pd.DataFrame()
        
        try:
            # Get all documents
            cursor = self.collection.find().sort("timestamp", -1)
            documents = list(cursor)
            
            if documents:
                # Convert ObjectId to string for pandas
                for doc in documents:
                    doc['_id'] = str(doc['_id'])
                    if 'timestamp' in doc and hasattr(doc['timestamp'], 'isoformat'):
                        doc['timestamp'] = doc['timestamp'].isoformat()
                
                df = pd.DataFrame(documents)
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"❌ MongoDB fetch error: {str(e)}")
            return pd.DataFrame()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.is_available():
            return {'total_records': 0, 'type_counts': {}, 'db_size': 0}
        
        try:
            # Get total count
            total_records = self.collection.count_documents({})
            
            # Get type counts using aggregation
            pipeline = [
                {"$group": {"_id": "$data_type", "count": {"$sum": 1}}}
            ]
            type_results = list(self.collection.aggregate(pipeline))
            type_counts = {result['_id']: result['count'] for result in type_results}
            
            # Estimate database size
            stats = self.db.command("collStats", self.collection_name)
            db_size = stats.get('size', 0)
            
            return {
                'total_records': total_records,
                'type_counts': type_counts,
                'db_size': db_size
            }
            
        except Exception as e:
            st.error(f"❌ MongoDB stats error: {str(e)}")
            return {'total_records': 0, 'type_counts': {}, 'db_size': 0}
    
    def delete_record(self, record_id: str) -> bool:
        """Delete a record by ID"""
        if not self.is_available():
            return False
        
        try:
            result = self.collection.delete_one({"_id": ObjectId(record_id)})
            return result.deleted_count > 0
        except Exception as e:
            st.error(f"❌ Delete error: {str(e)}")
            return False
    
    def update_record(self, record_id: str, updates: Dict[str, Any]) -> bool:
        """Update a record by ID"""
        if not self.is_available():
            return False
        
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(record_id)}, 
                {"$set": updates}
            )
            return result.modified_count > 0
        except Exception as e:
            st.error(f"❌ Update error: {str(e)}")
            return False

# Global instance
mongodb_manager = MongoDBManager()
