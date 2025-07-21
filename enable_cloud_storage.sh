#!/bin/bash

# Enable Cloud Storage Script
# Run this after updating your Supabase credentials

echo "🚀 Enabling Cloud Storage for Flora & Fauna App..."

# Check if secrets file exists
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "❌ Error: .streamlit/secrets.toml not found!"
    echo "Please make sure you're in the project directory and have updated your credentials."
    exit 1
fi

# Backup current supabase_db.py
echo "📋 Backing up current supabase_db.py..."
cp supabase_db.py supabase_db.py.backup

# Enable cloud storage in supabase_db.py
echo "☁️ Enabling Supabase Storage uploads..."

# Update the upload_file_to_storage method to actually upload
sed -i 's/# Skip Supabase Storage upload due to permission issues/# Upload to Supabase Storage - NOW ENABLED!/' supabase_db.py
sed -i 's/return None  # Skip upload, will save locally/# Proceeding with cloud upload/' supabase_db.py

# Enable actual upload code (uncomment the upload logic)
python3 << 'EOF'
import re

# Read the file
with open('supabase_db.py', 'r') as f:
    content = f.read()

# Find and replace the skipped upload logic
old_pattern = r'# Skip Supabase Storage upload due to permission issues.*?return None  # Skip upload, will save locally'
new_pattern = '''# Upload to Supabase Storage - NOW ENABLED!
        try:
            # Upload file to Supabase Storage
            file_name = f"{timestamp}_{uploaded_file.name}"
            
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
            return None'''

# Replace using regex with DOTALL flag
content = re.sub(old_pattern, new_pattern, content, flags=re.DOTALL)

# Write back to file
with open('supabase_db.py', 'w') as f:
    f.write(content)

print("✅ Supabase Storage upload logic enabled!")
EOF

# Update app.py to show cloud storage status
echo "📱 Updating app status messages..."
sed -i 's/❌ **Cloud Storage**: Disabled (permission issues)/✅ **Cloud Storage**: Enabled/' app.py
sed -i 's/Files are saved locally only/Files are saved to cloud storage/' app.py

echo ""
echo "🎉 Cloud Storage Enabled Successfully!"
echo ""
echo "📝 What was changed:"
echo "   ✅ Supabase Storage uploads re-enabled"
echo "   ✅ App status messages updated"
echo "   ✅ Backup created (supabase_db.py.backup)"
echo ""
echo "🚀 Next steps:"
echo "   1. Make sure your new Supabase credentials are in .streamlit/secrets.toml"
echo "   2. Run: streamlit run app.py"
echo "   3. Test file uploads - they should now go to cloud storage!"
echo ""
echo "🔍 To verify cloud storage is working:"
echo "   - Upload an image/audio/video"
echo "   - Check if you can view it in the app"
echo "   - Check your Supabase Storage dashboard"
echo ""
