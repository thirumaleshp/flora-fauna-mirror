import streamlit as st
import os
import datetime
import pandas as pd
import time
import requests

# Configure page - MUST be first Streamlit command
st.set_page_config(
    page_title="Flora and Fauna Data Collection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cloud database imports (after page config)
try:
    from supabase_db import supabase_manager
    CLOUD_DB_AVAILABLE = True
except ImportError:
    CLOUD_DB_AVAILABLE = False
    st.error("❌ Cloud database modules not available")

# Main title
st.title("🌿 Flora and Fauna Data Collection")
st.markdown("*Document and preserve biodiversity through multi-media data collection*")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("🗂️ Data Collection Types")
data_type = st.sidebar.radio(
    "Select data type to collect:",
    ["📝 Text Data", "🎵 Audio Data", "🎥 Video Data", "🖼️ Image Data", "📈 View Collected Data"]
)

# Show current database status
st.sidebar.markdown("---")
st.sidebar.title("💾 Database Status")
if CLOUD_DB_AVAILABLE:
    if supabase_manager.is_available():
        st.sidebar.success("✅ Supabase Connected")
        st.sidebar.info("☁️ Cloud Storage Active")
    else:
        st.sidebar.error("❌ Supabase Not Connected")
        st.sidebar.warning("Check credentials in secrets.toml")
else:
    st.sidebar.error("❌ Cloud database not available")

st.sidebar.markdown("---")

def display_file_preview(row, idx):
    """Display a preview of the file based on its type"""
    data_type = row['entry_type']  # Fixed column name
    filename = row['title']        # Fixed column name
    
    with st.expander(f"🔍 Preview: {filename}", expanded=True):
        
        # Check if file is stored in Supabase Storage (has URL)
        if pd.notna(row.get('file_url')) and isinstance(row['file_url'], str) and row['file_url'].startswith('http'):
            st.success("☁️ File stored in Supabase Storage")
            
            if data_type == 'image':
                try:
                    st.image(row['file_url'], caption=filename, use_column_width=True)
                    st.markdown(f"🔗 [Open in new tab]({row['file_url']})")
                except Exception:
                    st.error("❌ Could not display image")
                    st.markdown(f"🔗 [View file directly]({row['file_url']})")
            
            elif data_type == 'audio':
                try:
                    st.audio(row['file_url'])
                    st.markdown(f"🔗 [Download audio]({row['file_url']})")
                except Exception:
                    st.error("❌ Could not play audio")
                    st.markdown(f"🔗 [Download file directly]({row['file_url']})")
            
            elif data_type == 'video':
                try:
                    st.video(row['file_url'])
                    st.markdown(f"🔗 [Download video]({row['file_url']})")
                except Exception:
                    st.error("❌ Could not play video")
                    st.markdown(f"🔗 [Download file directly]({row['file_url']})")
            
            elif data_type == 'text':
                try:
                    # First, try to show content from database
                    if pd.notna(row.get('content')) and row['content'].strip():
                        st.text_area("📝 Text Content:", row['content'], height=200, key=f"text_content_{idx}")
                    
                    # Show additional text info if available
                    if pd.notna(row.get('description')) and row['description'] != row.get('content'):
                        st.text_area("📄 Description:", row['description'], height=100, key=f"text_desc_{idx}")
                    
                    # If there's a cloud file URL, show it and allow download
                    if row['file_url']:
                        st.markdown(f"🔗 [Download text file]({row['file_url']})")
                        
                        # Try to fetch and display cloud text file content
                        try:
                            response = requests.get(row['file_url'])
                            if response.status_code == 200:
                                cloud_content = response.text
                                if cloud_content.strip() and cloud_content != row.get('content', ''):
                                    st.text_area("☁️ Cloud File Content:", cloud_content, height=150, key=f"cloud_text_{idx}")
                        except Exception:
                            st.info("💡 Click the link above to view the cloud-stored text file")
                    
                except Exception:
                    st.error("❌ Could not display text")
            
            else:
                st.markdown(f"🔗 [View/Download file]({row['file_url']})")
        
        # Fallback: Try to load from local storage
        else:
            st.info("💾 File stored locally")
            data_dir = "data"
            local_path = os.path.join(data_dir, data_type + 's', filename)
            
            if os.path.exists(local_path):
                if data_type == 'text':
                    try:
                        # First check if content is in database
                        if pd.notna(row.get('content')) and row['content'].strip():
                            st.text_area("📝 Text Content (from database):", row['content'], height=200, key=f"text_db_{idx}")
                        
                        # Also try to read from file if it exists
                        with open(local_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        if file_content.strip():
                            st.text_area("📄 Text Content (from file):", file_content, height=200, key=f"text_file_{idx}")
                    except Exception as e:
                        # If file reading fails, still show database content
                        if pd.notna(row.get('content')) and row['content'].strip():
                            st.text_area("📝 Text Content:", row['content'], height=200, key=f"text_fallback_{idx}")
                        else:
                            st.error(f"❌ Could not read text content: {e}")
                
                elif data_type == 'image':
                    try:
                        st.image(local_path, caption=filename, use_column_width=True)
                    except Exception as e:
                        st.error(f"❌ Could not display image: {e}")
                
                elif data_type == 'audio':
                    try:
                        with open(local_path, 'rb') as f:
                            st.audio(f.read())
                    except Exception as e:
                        st.error(f"❌ Could not play audio: {e}")
                
                elif data_type == 'video':
                    try:
                        with open(local_path, 'rb') as f:
                            st.video(f.read())
                    except Exception as e:
                        st.error(f"❌ Could not play video: {e}")
            
            else:
                # File not found locally, but check if we have content in database
                if data_type == 'text' and pd.notna(row.get('content')) and row['content'].strip():
                    st.text_area("📝 Text Content (from database):", row['content'], height=200, key=f"text_db_only_{idx}")
                else:
                    st.warning("⚠️ File not found in local storage")
        
        # Display metadata
        st.markdown("---")
        st.markdown("📋 **Metadata Information:**")
        metadata_cols = ['timestamp', 'file_size', 'category', 'description', 'tags', 
                        'city', 'region', 'country', 'latitude', 'longitude']
        
        metadata_found = False
        for col in metadata_cols:
            if pd.notna(row.get(col)):
                metadata_found = True
                if col in ['latitude', 'longitude']:
                    st.write(f"**{col.title()}:** {row[col]:.6f}")
                elif col == 'file_size':
                    try:
                        size_mb = float(row[col]) / (1024 * 1024)
                        if size_mb < 1:
                            size_kb = float(row[col]) / 1024
                            st.write(f"**File Size:** {size_kb:.1f} KB")
                        else:
                            st.write(f"**File Size:** {size_mb:.1f} MB")
                    except Exception:
                        st.write(f"**File Size:** {row[col]}")
                else:
                    st.write(f"**{col.title()}:** {row[col]}")
        
        if not metadata_found:
            st.info("No additional metadata available")
        
        # Close preview button
        if st.button("❌ Close Preview", key=f"close_{idx}"):
            st.session_state[f"show_preview_{idx}"] = False
            st.rerun()

# Location Component
def get_auto_location():
    """Get location automatically using IP geolocation (mandatory for all uploads)"""
    
    # Add manual location override at the top
    st.markdown("### 📍 Location Setting")
    
    # Check if user wants to set location manually
    manual_override = st.checkbox("🔧 Set location manually (recommended for accuracy)")
    
    if manual_override:
        col1, col2 = st.columns(2)
        with col1:
            manual_city = st.text_input("🏙️ City:", value="Mumbai", placeholder="Enter your city")
            manual_country = st.text_input("🌍 Country:", value="India", placeholder="Enter your country")
        with col2:
            manual_lat = st.number_input("📍 Latitude:", value=19.076090, format="%.6f")
            manual_lon = st.number_input("📍 Longitude:", value=72.877426, format="%.6f")
        
        if st.button("💾 Set Location") and manual_city and manual_country:
            location_data = {
                "city": manual_city.strip(),
                "region": "Manual Entry",
                "country": manual_country.strip(),
                "latitude": float(manual_lat),
                "longitude": float(manual_lon),
                "detection_method": "manual_override",
                "timestamp": time.time(),
                "service": "manual"
            }
            st.session_state['auto_location'] = location_data
            st.success(f"✅ Location set to {manual_city}, {manual_country}")
            st.rerun()
    
    # Return early if manual override is selected but location not yet set
    if manual_override and ('auto_location' not in st.session_state or 
                           st.session_state['auto_location'].get('detection_method') != 'manual_override'):
        st.warning("⚠️ Please set your location manually above")
        return None
    
    current_time = time.time()
    
    # Check if we have recent location data (less than 5 minutes old)
    if ('auto_location' in st.session_state and 
        'timestamp' in st.session_state.get('auto_location', {}) and
        current_time - st.session_state['auto_location']['timestamp'] < 300):  # 5 minutes
        location_data = st.session_state['auto_location']
    elif not manual_override:  # Only try auto-detection if not manual override
        # Get fresh location data using IP geolocation
        with st.spinner("🌐 Detecting your current location..."):
            location_data = None
            try:
                # Try ipapi.co first (more reliable)
                response = requests.get('https://ipapi.co/json/', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    location_data = {
                        "city": data.get("city", "Unknown"),
                        "region": data.get("region", "Unknown"),
                        "country": data.get("country_name", "Unknown"),
                        "country_code": data.get("country_code", ""),
                        "latitude": data.get("latitude"),
                        "longitude": data.get("longitude"),
                        "timezone": data.get("timezone", "Unknown"),
                        "isp": data.get("org", "Unknown"),
                        "ip_address": data.get("ip", "Unknown"),
                        "detection_method": "ip_geolocation",
                        "timestamp": current_time,
                        "service": "ipapi.co"
                    }
                    st.session_state['auto_location'] = location_data
                    
            except Exception as e:
                # Fallback to ip-api.com
                try:
                    response = requests.get('http://ip-api.com/json/', timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        location_data = {
                            "city": data.get("city", "Unknown"),
                            "region": data.get("regionName", "Unknown"),
                            "country": data.get("country", "Unknown"),
                            "country_code": data.get("countryCode", ""),
                            "latitude": data.get("lat"),
                            "longitude": data.get("lon"),
                            "timezone": data.get("timezone", "Unknown"),
                            "isp": data.get("isp", "Unknown"),
                            "detection_method": "ip_geolocation",
                            "timestamp": current_time,
                            "service": "ip-api.com"
                        }
                        st.session_state['auto_location'] = location_data
                except Exception as e2:
                    st.error(f"Location detection failed: {str(e2)}")
                    location_data = None
    else:
        location_data = st.session_state.get('auto_location')
    
    # Display current location with enhanced details
    if st.session_state.get('auto_location'):
        location_data = st.session_state['auto_location']
        
        # Enhanced location display with coordinates
        if location_data.get('latitude') and location_data.get('longitude') and location_data['latitude'] != 0:
            coords_text = f" ({location_data['latitude']:.4f}, {location_data['longitude']:.4f})"
            accuracy_indicator = "🎯"  # Precise coordinates available
        else:
            coords_text = " (coordinates unavailable)"
            accuracy_indicator = "📍"  # Basic location only
            
        st.info(f"{accuracy_indicator} **Current Location**: {location_data['city']}, {location_data['country']}{coords_text}")
        
        # Show detailed location information
        with st.expander("📊 Location Details"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**🏙️ City:** {location_data.get('city', 'Unknown')}")
                st.write(f"**🌍 Country:** {location_data.get('country', 'Unknown')} ({location_data.get('country_code', 'N/A')})")
                st.write(f"**📍 Coordinates:** {location_data.get('latitude', 0):.6f}, {location_data.get('longitude', 0):.6f}")
            with col2:
                st.write(f"**🌐 ISP:** {location_data.get('isp', 'Unknown')}")
                st.write(f"**⏰ Timezone:** {location_data.get('timezone', 'Unknown')}")
                st.write(f"**🔍 Service:** {location_data.get('service', 'Unknown')}")
                if location_data.get('ip_address'):
                    st.write(f"**🌐 IP:** {location_data['ip_address']}")
        
        # Show service used and age of data
        if 'timestamp' in location_data:
            age_minutes = (time.time() - location_data['timestamp']) / 60
            accuracy_text = "High accuracy with precise coordinates" if location_data.get('latitude', 0) != 0 else "Basic location only"
            st.caption(f"🕒 Detected {age_minutes:.0f} minutes ago via {location_data.get('service', 'unknown service')} | {accuracy_text}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Location", help="Get fresh location with precise coordinates"):
                # Clear cached location to force refresh
                if 'auto_location' in st.session_state:
                    del st.session_state['auto_location']
                st.rerun()
        with col2:
            override = st.checkbox("✏️ Edit location")
        
        # Show debug info if location seems wrong
        if location_data.get('city') == 'The Dalles' or location_data.get('country') == 'United States':
            st.warning("⚠️ Location may be incorrect due to proxy/CDN. Use 'Edit location' to set manually.")
            with st.expander("🔍 Debug Info"):
                st.json({
                    "detected_city": location_data.get('city'),
                    "detected_country": location_data.get('country'),
                    "service_used": location_data.get('service'),
                    "detection_method": location_data.get('detection_method'),
                    "note": "This may be Streamlit Cloud's server location, not your actual location"
                })
        
        if override:
            st.markdown("**🇮🇳 Common Indian Cities (click to auto-fill):**")
            
            indian_cities = [
                ("Mumbai", "India", "19.0760, 72.8777"),
                ("Delhi", "India", "28.7041, 77.1025"),
                ("Bangalore", "India", "12.9716, 77.5946"),
                ("Hyderabad", "India", "17.3850, 78.4867"),
                ("Chennai", "India", "13.0827, 80.2707"),
                ("Kolkata", "India", "22.5726, 88.3639"),
                ("Pune", "India", "18.5204, 73.8567"),
                ("Ahmedabad", "India", "23.0225, 72.5714"),
                ("Jaipur", "India", "26.9124, 75.7873"),
                ("Surat", "India", "21.1702, 72.8311"),
                ("Lucknow", "India", "26.8467, 80.9462"),
                ("Kanpur", "India", "26.4499, 80.3319"),
                ("Nagpur", "India", "21.1458, 79.0882"),
                ("Indore", "India", "22.7196, 75.8577"),
                ("Thane", "India", "19.2183, 72.9781"),
                ("Bhopal", "India", "23.2599, 77.4126"),
                ("Visakhapatnam", "India", "17.6868, 83.2185"),
                ("Pimpri-Chinchwad", "India", "18.6298, 73.7997"),
                ("Patna", "India", "25.5941, 85.1376"),
                ("Vadodara", "India", "22.3072, 73.1812")
            ]
            
            # Create columns for city buttons
            cols = st.columns(4)
            for i, (city, country, coords) in enumerate(indian_cities):
                with cols[i % 4]:
                    if st.button(f"{city}", key=f"city_{i}", help=f"Set location to {city}, {country}"):
                        lat, lon = map(float, coords.split(', '))
                        st.session_state['auto_location'] = {
                            "city": city,
                            "region": "Unknown",
                            "country": country,
                            "latitude": lat,
                            "longitude": lon,
                            "detection_method": "manual_selection",
                            "timestamp": current_time,
                            "service": "manual"
                        }
                        st.success(f"✅ Location set to {city}, {country}")
                        st.rerun()
            
            st.markdown("**Or enter custom location:**")
            new_city = st.text_input("City:", value=location_data.get('city', ''))
            new_country = st.text_input("Country:", value=location_data.get('country', ''))
            
            # Auto-suggest coordinates for common countries
            coord_help = "Format: latitude, longitude (e.g., 28.7041, 77.1025 for Delhi)"
            if new_country.lower() == 'india':
                coord_help += " | For India, latitude ≈ 8-37, longitude ≈ 68-97"
            
            current_coords = ""
            if location_data.get('latitude') and location_data.get('longitude'):
                current_coords = f"{location_data['latitude']}, {location_data['longitude']}"
            
            new_coords = st.text_input("Coordinates:", value=current_coords, help=coord_help)
            
            if st.button("💾 Update Location") and new_city and new_country:
                try:
                    if new_coords and ',' in new_coords:
                        lat, lon = map(float, new_coords.split(','))
                    else:
                        lat, lon = None, None
                    
                    st.session_state['auto_location'] = {
                        "city": new_city.strip(),
                        "region": "Custom",
                        "country": new_country.strip(),
                        "latitude": lat,
                        "longitude": lon,
                        "detection_method": "manual_override",
                        "timestamp": time.time(),
                        "service": "manual"
                    }
                    st.success(f"✅ Location updated to {new_city}, {new_country}")
                    st.rerun()
                except ValueError:
                    st.error("❌ Invalid coordinates format. Use: latitude, longitude")
        
        return location_data
    else:
        st.error("❌ Location detection failed. Location is required for uploads.")
        return None

def validate_location_before_upload():
    """Validate that location is set before allowing any data upload"""
    location_data = st.session_state.get('auto_location')
    
    if not location_data:
        st.error("🚫 **Location Required**: Please set your location before uploading any data.")
        st.info("👆 Use the location detection above or set your location manually.")
        return False
    
    if (location_data.get('detection_method') == 'pending' or 
        location_data.get('city') == 'Unknown Location' or
        not location_data.get('city')):
        st.error("🚫 **Valid Location Required**: Please provide a valid location before uploading.")
        st.info("👆 Use device location detection or manual entry above.")
        return False
    
    return True

def require_location_wrapper(upload_function):
    """Wrapper function to enforce location requirement for uploads"""
    if not validate_location_before_upload():
        st.warning("⚠️ **Upload blocked**: Location must be set first.")
        return False
    return upload_function()

# Text Data Collection
if data_type == "📝 Text Data":
    st.header("📝 Text Data Collection")
    
    # Mandatory Auto-Location Detection
    st.subheader("📍 Location (Auto-Detected)")
    
    # Use the centralized location function
    location_data = get_auto_location()
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Enter your text data:")
        
        # Text input options
        input_method = st.radio("Choose input method:", ["Single Text Entry", "Multi-line Text", "CSV Upload"])
        
        if input_method == "Single Text Entry":
            text_input = st.text_input("Enter text:", placeholder="Type your text here...")
            category = st.selectbox("Category:", ["General", "Research", "Survey", "Feedback", "Other"])
            
            if st.button("Save Text") and text_input:
                # Validate location is set before saving
                if not validate_location_before_upload():
                    st.stop()  # Stop execution if location is not valid
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"text_{timestamp}.txt"
                
                # Create data directory if it doesn't exist
                os.makedirs("data/text", exist_ok=True)
                filepath = f"data/text/{filename}"
                
                # Save to file system (for backward compatibility)
                with open(filepath, 'w') as f:
                    f.write(f"Category: {category}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Content: {text_input}\n")
                
                # Save to unified database (cloud or local)
                file_data = text_input.encode('utf-8')
                additional_info = {
                    "category": category, 
                    "method": "single_entry",
                    "file_size": len(file_data),
                    "content": text_input
                }
                
                if CLOUD_DB_AVAILABLE:
                    data_id = supabase_manager.save_data("text", filename, file_data, additional_info, location_data)
                    st.success(f"✅ Text saved successfully as {filename}")
                    st.info(f"💾 Stored in: Supabase (ID: {data_id})")
                    st.info(f"📍 Location: {location_data['city']}, {location_data['country']}")
                else:
                    st.error("❌ Failed to save to cloud storage. Please check your Supabase connection.")
        
        elif input_method == "Multi-line Text":
            text_area = st.text_area("Enter multi-line text:", height=200, placeholder="Enter your multi-line text here...")
            category = st.selectbox("Category:", ["General", "Research", "Survey", "Feedback", "Other"], key="multiline_category")
            
            if st.button("Save Multi-line Text") and text_area:
                # Validate location is set before saving
                if not validate_location_before_upload():
                    st.stop()  # Stop execution if location is not valid
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"multitext_{timestamp}.txt"
                
                # Create data directory if it doesn't exist
                os.makedirs("data/text", exist_ok=True)
                filepath = f"data/text/{filename}"
                
                # Save to file system (for backward compatibility)
                with open(filepath, 'w') as f:
                    f.write(f"Category: {category}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Content:\n{text_area}\n")
                
                # Save to unified database (cloud or local)
                file_data = text_area.encode('utf-8')
                additional_info = {
                    "category": category, 
                    "method": "multi_line",
                    "file_size": len(file_data),
                    "content": text_area
                }
                
                if CLOUD_DB_AVAILABLE:
                    data_id = supabase_manager.save_data("text", filename, file_data, additional_info, location_data)
                    st.success(f"✅ Multi-line text saved successfully as {filename}")
                    st.info(f"💾 Stored in: Supabase (ID: {data_id})")
                    st.info(f"📍 Location: {location_data['city']}, {location_data['country']}")
                else:
                    st.error("❌ Failed to save to cloud storage. Please check your Supabase connection.")
        
        else:  # CSV Upload
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                st.write("Preview of uploaded data:")
                st.dataframe(df.head())
                
                if st.button("Save CSV Data"):
                    # Validate location is set before saving
                    if not validate_location_before_upload():
                        st.stop()  # Stop execution if location is not valid
                    
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"csv_{timestamp}.csv"
                    
                    # Create data directory if it doesn't exist
                    os.makedirs("data/text", exist_ok=True)
                    filepath = f"data/text/{filename}"
                    df.to_csv(filepath, index=False)
                    
                    # Save to unified database (cloud or local)
                    csv_content = df.to_csv(index=False)
                    file_data = csv_content.encode('utf-8')
                    additional_info = {
                        "method": "csv_upload", 
                        "rows": len(df), 
                        "columns": list(df.columns),
                        "file_size": len(file_data),
                        "content": csv_content
                    }
                    
                    if CLOUD_DB_AVAILABLE:
                        data_id = supabase_manager.save_data("text", filename, file_data, additional_info, location_data)
                        st.success(f"✅ CSV data saved successfully as {filename}")
                        st.info(f"💾 Stored in: Supabase (ID: {data_id})")
                        st.info(f"📍 Location: {location_data['city']}, {location_data['country']}")
                    else:
                        st.error("❌ Failed to save to cloud storage. Please check your Supabase connection.")
    
    with col2:
        st.subheader("Instructions:")
        st.info("""
        📝 **Text Data Collection**
        
        • **Single Text**: For short entries
        • **Multi-line**: For longer content
        • **CSV Upload**: For bulk data import
        
        All text data will be saved with timestamps and categories for easy organization.
        """)

# Audio Data Collection
elif data_type == "🎵 Audio Data":
    st.header("🎵 Audio Data Collection")
    
    # Mandatory Auto-Location Detection
    st.subheader("📍 Location (Auto-Detected)")
    
    # Use the centralized location function
    location_data = get_auto_location()
        
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload or record audio:")
        
        # Audio upload
        uploaded_audio = st.file_uploader("Upload audio file", type=['mp3', 'wav', 'ogg', 'm4a'])
        
        if uploaded_audio is not None:
            st.audio(uploaded_audio, format='audio/wav')
            
            # Audio metadata
            audio_category = st.selectbox("Audio Category:", ["Speech", "Music", "Nature Sounds", "Interview", "Other"])
            duration = st.number_input("Duration (seconds):", min_value=0.0, step=0.1)
            description = st.text_area("Description:", placeholder="Describe the audio content...")
            
            if st.button("Save Audio"):
                # Validate location is set before saving
                if not validate_location_before_upload():
                    st.stop()  # Stop execution if location is not valid
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_extension = uploaded_audio.name.split('.')[-1]
                filename = f"audio_{timestamp}.{file_extension}"
                
                # Create data directory if it doesn't exist
                os.makedirs("data/audio", exist_ok=True)
                filepath = f"data/audio/{filename}"
                
                # Get file data
                file_data = uploaded_audio.getbuffer()
                file_bytes = bytes(file_data)  # Convert memoryview to bytes
                
                # Save to file system (for backward compatibility)
                with open(filepath, 'wb') as f:
                    f.write(file_bytes)
                
                # Save to unified database (cloud or local)
                additional_info = {
                    "category": audio_category,
                    "duration": duration,
                    "description": description,
                    "original_name": uploaded_audio.name,
                    "file_size": len(file_bytes)
                }
                
                if CLOUD_DB_AVAILABLE:
                    data_id = supabase_manager.save_data("audio", filename, file_bytes, additional_info, location_data)
                    st.success(f"✅ Audio saved successfully as {filename}")
                    st.info(f"💾 Stored in: Supabase (ID: {data_id})")
                    st.info(f"📍 Location: {location_data['city']}, {location_data['country']}")
                else:
                    st.error("❌ Failed to save to cloud storage. Please check your Supabase connection.")
        
        # Recording instructions
        st.markdown("### 🎙️ Recording Audio")
        st.info("For audio recording, you can use your device's built-in recorder and upload the file above.")
    
    with col2:
        st.subheader("Instructions:")
        st.info("""
        🎵 **Audio Data Collection**
        
        • **Supported formats**: MP3, WAV, OGG, M4A
        • **Categories**: Speech, Music, Nature, Interview
        • **Metadata**: Duration, description, category
        
        Upload audio files and provide detailed descriptions for better organization.
        """)

# Video Data Collection
elif data_type == "🎥 Video Data":
    st.header("🎥 Video Data Collection")
    
    # Mandatory Auto-Location Detection
    st.subheader("📍 Location (Auto-Detected)")
    
    # Use the centralized location function
    location_data = get_auto_location()
        
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload video:")
        
        uploaded_video = st.file_uploader("Upload video file", type=['mp4', 'avi', 'mov', 'wmv'])
        
        if uploaded_video is not None:
            st.video(uploaded_video)
            
            # Video metadata
            video_category = st.selectbox("Video Category:", ["Educational", "Documentation", "Interview", "Presentation", "Other"])
            duration = st.number_input("Duration (seconds):", min_value=0.0, step=0.1)
            resolution = st.selectbox("Resolution:", ["HD (720p)", "Full HD (1080p)", "4K", "Other"])
            description = st.text_area("Description:", placeholder="Describe the video content...")
            tags = st.text_input("Tags (comma-separated):", placeholder="tag1, tag2, tag3")
            
            if st.button("Save Video"):
                # Validate location is set before saving
                if not validate_location_before_upload():
                    st.stop()  # Stop execution if location is not valid
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_extension = uploaded_video.name.split('.')[-1]
                filename = f"video_{timestamp}.{file_extension}"
                
                # Create data directory if it doesn't exist
                os.makedirs("data/video", exist_ok=True)
                filepath = f"data/video/{filename}"
                
                # Get file data
                file_data = uploaded_video.getbuffer()
                file_bytes = bytes(file_data)  # Convert memoryview to bytes
                
                # Save to file system (for backward compatibility)
                with open(filepath, 'wb') as f:
                    f.write(file_bytes)
                
                # Save to unified database (cloud or local)
                additional_info = {
                    "category": video_category,
                    "duration": duration,
                    "resolution": resolution,
                    "description": description,
                    "tags": tags,
                    "original_name": uploaded_video.name,
                    "file_size": len(file_bytes)
                }
                
                if CLOUD_DB_AVAILABLE:
                    data_id = supabase_manager.save_data("video", filename, file_bytes, additional_info, location_data)
                    st.success(f"✅ Video saved successfully as {filename}")
                    st.info(f"💾 Stored in: Supabase (ID: {data_id})")
                    st.info(f"📍 Location: {location_data['city']}, {location_data['country']}")
                else:
                    st.error("❌ Failed to save to cloud storage. Please check your Supabase connection.")
    
    with col2:
        st.subheader("Instructions:")
        st.info("""
        🎥 **Video Data Collection**
        
        • **Supported formats**: MP4, AVI, MOV, WMV
        • **Categories**: Educational, Documentation, Interview
        • **Metadata**: Duration, resolution, tags
        
        Upload video files with detailed descriptions and tags for easy searching.
        """)

# Image Data Collection
elif data_type == "🖼️ Image Data":
    st.header("🖼️ Image Data Collection")
    
    # Mandatory Auto-Location Detection
    st.subheader("📍 Location (Auto-Detected)")
    
    # Use the centralized location function
    location_data = get_auto_location()
        
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload images:")
        
        uploaded_images = st.file_uploader("Upload image files", type=['png', 'jpg', 'jpeg', 'gif', 'bmp'], accept_multiple_files=True)
        
        if uploaded_images:
            # Image metadata
            image_category = st.selectbox("Image Category:", ["Photos", "Screenshots", "Diagrams", "Charts", "Other"])
            description = st.text_area("Description:", placeholder="Describe the images...")
            tags = st.text_input("Tags (comma-separated):", placeholder="tag1, tag2, tag3")
            
            # Display images
            cols = st.columns(3)
            for i, uploaded_image in enumerate(uploaded_images):
                with cols[i % 3]:
                    st.image(uploaded_image, caption=uploaded_image.name, use_column_width=True)
            
            if st.button("Save Images"):
                # Validate location is set before saving
                if not validate_location_before_upload():
                    st.stop()  # Stop execution if location is not valid
                
                saved_files = []
                for uploaded_image in uploaded_images:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_extension = uploaded_image.name.split('.')[-1]
                    filename = f"image_{timestamp}_{uploaded_image.name}"
                    
                    # Create data directory if it doesn't exist
                    os.makedirs("data/image", exist_ok=True)
                    filepath = f"data/image/{filename}"
                    
                    # Get file data
                    file_data = uploaded_image.getbuffer()
                    file_bytes = bytes(file_data)  # Convert memoryview to bytes
                    
                    # Save to file system (for backward compatibility)
                    with open(filepath, 'wb') as f:
                        f.write(file_bytes)
                    
                    # Save to unified database (cloud or local)
                    additional_info = {
                        "category": image_category,
                        "description": description,
                        "tags": tags,
                        "original_name": uploaded_image.name,
                        "file_size": len(file_bytes)
                    }
                    
                    if CLOUD_DB_AVAILABLE:
                        data_id = supabase_manager.save_data("image", filename, file_bytes, additional_info, location_data)
                        saved_files.append((filename, data_id))
                    else:
                        st.error(f"❌ Failed to save {uploaded_image.name} to cloud storage.")
                
                if saved_files:
                    st.success(f"✅ {len(saved_files)} image(s) saved successfully!")
                    for filename, data_id in saved_files:
                        st.info(f"💾 {filename} - Supabase ID: {data_id}")
                    st.info(f"📍 Location: {location_data['city']}, {location_data['country']}")
    
    with col2:
        st.subheader("Instructions:")
        st.info("""
        🖼️ **Image Data Collection**
        
        • **Supported formats**: PNG, JPG, JPEG, GIF, BMP
        • **Multiple uploads**: Select multiple images at once
        • **Categories**: Photos, Screenshots, Diagrams
        
        Upload multiple images with descriptions and tags for better organization.
        """)

# View Collected Data
elif data_type == "📈 View Collected Data":
    st.header("🌿 Flora and Fauna Data Overview")
    
    # Show current database provider
    if CLOUD_DB_AVAILABLE:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.success("☁️ **Cloud Database Connected** (Supabase)")
        
        with col2:
            if st.button("🔄 Refresh Data"):
                st.rerun()
        
        with col3:
            show_metadata = st.checkbox("📊 Show Metadata", value=True)
    
    # Get database statistics
    if CLOUD_DB_AVAILABLE:
        db_stats = supabase_manager.get_statistics()
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Text Files", db_stats.get('text', 0))
        
        with col2:
            st.metric("🎵 Audio Files", db_stats.get('audio', 0))
        
        with col3:
            st.metric("🎥 Video Files", db_stats.get('video', 0))
        
        with col4:
            st.metric("🖼️ Image Files", db_stats.get('image', 0))
        
        st.markdown("---")
        
        # Data filtering
        st.subheader("🔍 Filter and View Data")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            filter_type = st.selectbox("Data Type:", ["All", "Text", "Audio", "Video", "Image"])
        
        with filter_col2:
            filter_days = st.selectbox("Time Range:", ["All Time", "Last 7 days", "Last 30 days", "Today"])
        
        with filter_col3:
            search_term = st.text_input("🔍 Search:", placeholder="Search in titles, descriptions...")
        
        # Get filtered data
        try:
            data_df = supabase_manager.get_all_data(
                data_type=filter_type.lower() if filter_type != "All" else None,
                days={"Today": 1, "Last 7 days": 7, "Last 30 days": 30}.get(filter_days),
                search_term=search_term if search_term else None
            )
            
            if data_df is not None and len(data_df) > 0:
                st.subheader(f"📊 Found {len(data_df)} records")
                
                # Display data in an interactive table
                for idx, row in data_df.iterrows():
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            # File info
                            data_type_icon = {"text": "📝", "audio": "🎵", "video": "🎥", "image": "🖼️"}.get(row['entry_type'], "📄")
                            st.write(f"{data_type_icon} **{row['title']}**")
                            if pd.notna(row.get('description')) and row['description']:
                                st.caption(f"📄 {row['description'][:100]}...")
                        
                        with col2:
                            # Metadata
                            if pd.notna(row.get('city')) and row['city']:
                                st.caption(f"📍 {row['city']}, {row.get('country', 'Unknown')}")
                            st.caption(f"📅 {row['timestamp'][:10] if pd.notna(row.get('timestamp')) else 'Unknown'}")
                        
                        with col3:
                            # Actions
                            if st.button("👁️ Preview", key=f"preview_{idx}"):
                                st.session_state[f"show_preview_{idx}"] = True
                        
                        # Show preview if requested
                        if st.session_state.get(f"show_preview_{idx}", False):
                            display_file_preview(row, idx)
                        
                        st.markdown("---")
            
            else:
                st.info("📭 No data found matching the current filters.")
                st.markdown("""
                **Tips:**
                - Try adjusting the filters above
                - Check if you have uploaded any data
                - Verify your database connection
                """)
        
        except Exception as e:
            st.error(f"❌ Error retrieving data: {str(e)}")
            st.info("Please check your database connection and try again.")
    
    else:
        st.error("❌ Cloud database not available. Please check your Supabase connection.")
        st.info("""
        **To connect to Supabase:**
        1. Ensure `supabase_db.py` exists in your project
        2. Check your `.streamlit/secrets.toml` file
        3. Verify your Supabase credentials
        """)
