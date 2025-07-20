"""
Data processing utilities for the collection app
"""

import os
import json
import pandas as pd
from datetime import datetime
import shutil

class DataProcessor:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.metadata_file = os.path.join(data_dir, "metadata.json")
    
    def load_metadata(self):
        """Load metadata from JSON file"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return []
    
    def get_data_summary(self):
        """Get summary of collected data"""
        metadata = self.load_metadata()
        
        if not metadata:
            return {"total_files": 0, "data_types": {}}
        
        summary = {
            "total_files": len(metadata),
            "data_types": {},
            "date_range": {
                "earliest": None,
                "latest": None
            }
        }
        
        # Count by data type
        for item in metadata:
            data_type = item.get("data_type", "unknown")
            if data_type not in summary["data_types"]:
                summary["data_types"][data_type] = 0
            summary["data_types"][data_type] += 1
        
        # Date range
        timestamps = [item["timestamp"] for item in metadata if "timestamp" in item]
        if timestamps:
            timestamps.sort()
            summary["date_range"]["earliest"] = timestamps[0]
            summary["date_range"]["latest"] = timestamps[-1]
        
        return summary
    
    def export_metadata_csv(self, output_file="metadata_export.csv"):
        """Export metadata to CSV"""
        metadata = self.load_metadata()
        
        if not metadata:
            print("No metadata to export")
            return False
        
        # Flatten the data for CSV export
        flattened_data = []
        for item in metadata:
            flat_item = {
                "filename": item.get("filename", ""),
                "data_type": item.get("data_type", ""),
                "timestamp": item.get("timestamp", "")
            }
            
            # Add additional info if available
            additional_info = item.get("additional_info", {})
            if isinstance(additional_info, dict):
                for key, value in additional_info.items():
                    flat_item[f"info_{key}"] = value
            
            flattened_data.append(flat_item)
        
        df = pd.DataFrame(flattened_data)
        df.to_csv(output_file, index=False)
        print(f"Metadata exported to {output_file}")
        return True
    
    def cleanup_old_files(self, days_old=30):
        """Remove files older than specified days"""
        metadata = self.load_metadata()
        current_time = datetime.now()
        
        files_to_remove = []
        updated_metadata = []
        
        for item in metadata:
            file_timestamp = datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
            days_diff = (current_time - file_timestamp).days
            
            if days_diff > days_old:
                # Mark for removal
                file_path = os.path.join(self.data_dir, item["data_type"], item["filename"])
                if os.path.exists(file_path):
                    files_to_remove.append((file_path, item["filename"]))
            else:
                updated_metadata.append(item)
        
        # Remove old files
        for file_path, filename in files_to_remove:
            try:
                os.remove(file_path)
                print(f"Removed old file: {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")
        
        # Update metadata
        if files_to_remove:
            with open(self.metadata_file, 'w') as f:
                json.dump(updated_metadata, f, indent=2)
            print(f"Cleaned up {len(files_to_remove)} old files")
        
        return len(files_to_remove)
    
    def backup_data(self, backup_dir="backup"):
        """Create backup of all collected data"""
        if not os.path.exists(self.data_dir):
            print("No data directory found")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{backup_dir}/data_backup_{timestamp}"
        
        try:
            shutil.copytree(self.data_dir, backup_path)
            print(f"Data backed up to: {backup_path}")
            return True
        except Exception as e:
            print(f"Backup failed: {e}")
            return False
    
    def get_file_stats(self):
        """Get file statistics by type"""
        stats = {}
        
        for data_type in ["text", "audio", "video", "images"]:
            type_dir = os.path.join(self.data_dir, data_type)
            if os.path.exists(type_dir):
                files = os.listdir(type_dir)
                total_size = 0
                
                for file in files:
                    file_path = os.path.join(type_dir, file)
                    if os.path.isfile(file_path):
                        total_size += os.path.getsize(file_path)
                
                stats[data_type] = {
                    "count": len(files),
                    "total_size_mb": round(total_size / (1024 * 1024), 2)
                }
            else:
                stats[data_type] = {"count": 0, "total_size_mb": 0}
        
        return stats

# Example usage
if __name__ == "__main__":
    processor = DataProcessor()
    
    # Print summary
    summary = processor.get_data_summary()
    print("Data Summary:")
    print(f"Total files: {summary['total_files']}")
    print(f"Data types: {summary['data_types']}")
    
    # Print file statistics
    print("\nFile Statistics:")
    stats = processor.get_file_stats()
    for data_type, stat in stats.items():
        print(f"{data_type}: {stat['count']} files, {stat['total_size_mb']} MB")
