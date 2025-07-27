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

# AI Chatbot imports (Stage 2)
try:
    from chatbot import render_chatbot_interface
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False

# Main title
st.title("🌿 Flora and Fauna Data Collection")
st.markdown("*Document and preserve biodiversity through multi-media data collection*")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("🗂️ Data Collection Types")
data_type = st.sidebar.radio(
    "Select data type to collect:",
    ["🤖 AI Chatbot", "📝 Text Data", "🎵 Audio Data", "🎥 Video Data", "🖼️ Image Data", "📈 View Collected Data"],
    index=0  # Default to AI Chatbot
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
    """Get location automatically using IP geolocation or manual coordinates entry"""
    
    st.markdown("### 📍 Location Setting")
    
    # Location method selection
    location_method = st.radio(
        "Choose location method:",
        ["📱 Device Location (GPS/WiFi)", "🌐 IP-based Location", "📍 Enter coordinates manually"],
        horizontal=True
    )
    
    if location_method == "� Device Location (GPS/WiFi)":
        st.markdown("**📱 Device Location Detection**")
        st.info("🎯 This method uses your device's GPS/WiFi for the most accurate location.")
        
        # Check if we already have device location
        if ('auto_location' in st.session_state and 
            st.session_state['auto_location'].get('detection_method') == 'device_location'):
            location_data = st.session_state['auto_location']
        else:
            # HTML5 Geolocation API
            if st.button("📍 Get My Device Location", key="get_device_location", type="primary"):
                location_html = """
                <div style="padding: 20px; border: 2px solid #4CAF50; border-radius: 10px; background: #f8f9fa;">
                    <div id="location-status">🔄 Requesting location permission...</div>
                    <div id="location-result" style="margin-top: 10px;"></div>
                </div>
                
                <script>
                function getDeviceLocation() {
                    const statusDiv = document.getElementById('location-status');
                    const resultDiv = document.getElementById('location-result');
                    
                    if (navigator.geolocation) {
                        statusDiv.innerHTML = '🔄 Getting your location...';
                        
                        navigator.geolocation.getCurrentPosition(
                            function(position) {
                                const lat = position.coords.latitude;
                                const lon = position.coords.longitude;
                                const accuracy = position.coords.accuracy;
                                
                                statusDiv.innerHTML = '✅ Location found successfully!';
                                resultDiv.innerHTML = '<strong>📍 Coordinates:</strong> ' + lat.toFixed(6) + ', ' + lon.toFixed(6) + '<br><strong>🎯 Accuracy:</strong> ±' + Math.round(accuracy) + ' meters<br><em style="color: green;">Please copy these coordinates below and click "Use This Location".</em>';
                            },
                            function(error) {
                                let errorMsg = '❌ Location access failed: ';
                                switch(error.code) {
                                    case error.PERMISSION_DENIED:
                                        errorMsg += 'Permission denied. Please allow location access and try again.';
                                        break;
                                    case error.POSITION_UNAVAILABLE:
                                        errorMsg += 'Location information unavailable.';
                                        break;
                                    case error.TIMEOUT:
                                        errorMsg += 'Location request timed out. Please try again.';
                                        break;
                                    default:
                                        errorMsg += 'Unknown error occurred.';
                                        break;
                                }
                                statusDiv.innerHTML = errorMsg;
                            },
                            {
                                enableHighAccuracy: true,
                                timeout: 15000,
                                maximumAge: 300000
                            }
                        );
                    } else {
                        statusDiv.innerHTML = '❌ Geolocation is not supported by this browser.';
                    }
                }
                getDeviceLocation();
                </script>
                """
                st.components.v1.html(location_html, height=150)
            
            # Manual input for device coordinates
            st.markdown("**📍 Enter the coordinates from above (if detection worked):**")
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                device_lat = st.number_input("Device Latitude:", value=0.0, format="%.6f", key="device_lat")
            with col2:
                device_lon = st.number_input("Device Longitude:", value=0.0, format="%.6f", key="device_lon")
            with col3:
                if st.button("✅ Use This Location", key="use_device_coords"):
                    if device_lat != 0.0 and device_lon != 0.0:
                        # Get city/country from coordinates
                        try:
                            response = requests.get(
                                f'https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={device_lat}&longitude={device_lon}&localityLanguage=en',
                                timeout=5
                            )
                            if response.status_code == 200:
                                geo_data = response.json()
                                city = geo_data.get('city') or geo_data.get('locality') or 'Device Location'
                                country = geo_data.get('countryName') or 'GPS Coordinates'
                                region = geo_data.get('principalSubdivision') or 'Device GPS'
                            else:
                                city = "Device Location"
                                country = "GPS Coordinates"
                                region = "Device GPS"
                        except Exception:
                            city = "Device Location"
                            country = "GPS Coordinates"
                            region = "Device GPS"
                        
                        location_data = {
                            "city": city,
                            "region": region,
                            "country": country,
                            "latitude": float(device_lat),
                            "longitude": float(device_lon),
                            "detection_method": "device_location",
                            "timestamp": time.time(),
                            "service": "device_gps",
                            "accuracy": "high"
                        }
                        st.session_state['auto_location'] = location_data
                        st.success(f"✅ Device location set: {device_lat:.6f}, {device_lon:.6f}")
                        st.rerun()
                    else:
                        st.error("❌ Please enter valid coordinates from the GPS detection above.")
            
            return None
    
    elif location_method == "🌐 IP-based Location":
        st.markdown("**🌐 IP-based Location Detection**")
        st.warning("⚠️ Less accurate - may show server/proxy location instead of your actual location.")
        st.info("💡 For better accuracy, use Device Location instead.")
        
        # Continue with existing IP-based logic but simplified
        current_time = time.time()
        
        if ('auto_location' in st.session_state and 
            'timestamp' in st.session_state.get('auto_location', {}) and
            current_time - st.session_state['auto_location']['timestamp'] < 300 and
            st.session_state['auto_location'].get('detection_method') == 'ip_geolocation'):
            location_data = st.session_state['auto_location']
        else:
            with st.spinner("🌐 Detecting location from IP..."):
                location_data = None
                try:
                    response = requests.get('https://ipinfo.io/json', timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("loc"):
                            lat, lon = data.get("loc").split(",")
                            location_data = {
                                "city": data.get("city", "Unknown"),
                                "region": data.get("region", "Unknown"),
                                "country": data.get("country", "Unknown"),
                                "country_code": data.get("country", ""),
                                "latitude": float(lat),
                                "longitude": float(lon),
                                "timezone": data.get("timezone", "Unknown"),
                                "isp": data.get("org", "Unknown"),
                                "ip_address": data.get("ip", "Unknown"),
                                "detection_method": "ip_geolocation",
                                "timestamp": current_time,
                                "service": "ipinfo.io"
                            }
                            st.session_state['auto_location'] = location_data
                except Exception:
                    st.error("❌ IP location detection failed.")
                    return None
    
    elif location_method == "📍 Enter coordinates manually":
        st.markdown("**📍 Manual Coordinate Entry**")
        st.info("🎯 Enter your exact GPS coordinates for precise location data.")
        
        # Create two columns for latitude and longitude input
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌐 Latitude**")
            manual_lat = st.number_input(
                "Latitude (°N/S):", 
                min_value=-90.0,
                max_value=90.0,
                value=0.0, 
                format="%.6f",
                help="Enter latitude (-90 to 90). Positive for North, negative for South.",
                key="manual_lat_input"
            )
            st.caption("Range: -90.0 to +90.0")
            st.caption("Example: 40.712776 (New York)")
        
        with col2:
            st.markdown("**🌍 Longitude**")
            manual_lon = st.number_input(
                "Longitude (°E/W):", 
                min_value=-180.0,
                max_value=180.0,
                value=0.0, 
                format="%.6f",
                help="Enter longitude (-180 to 180). Positive for East, negative for West.",
                key="manual_lon_input"
            )
            st.caption("Range: -180.0 to +180.0")
            st.caption("Example: -74.006000 (New York)")
        
        # Coordinate validation and submission
        st.markdown("---")
        col_submit, col_help = st.columns([1, 2])
        
        with col_submit:
            coords_valid = (-90 <= manual_lat <= 90 and -180 <= manual_lon <= 180 and 
                          (manual_lat != 0.0 or manual_lon != 0.0))
            
            if st.button("📍 Set These Coordinates", 
                        disabled=not coords_valid,
                        type="primary" if coords_valid else "secondary"):
                if coords_valid:
                    # Try to get city/country from coordinates using reverse geocoding
                    with st.spinner("🔍 Looking up location details..."):
                        try:
                            response = requests.get(
                                f'https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={manual_lat}&longitude={manual_lon}&localityLanguage=en',
                                timeout=5
                            )
                            if response.status_code == 200:
                                geo_data = response.json()
                                city = geo_data.get('city') or geo_data.get('locality') or 'Unknown City'
                                country = geo_data.get('countryName') or 'Unknown Country'
                                region = geo_data.get('principalSubdivision') or 'Unknown Region'
                            else:
                                city = f"Lat: {manual_lat:.4f}"
                                country = f"Lon: {manual_lon:.4f}"
                                region = "Coordinates"
                        except Exception:
                            city = f"Lat: {manual_lat:.4f}"
                            country = f"Lon: {manual_lon:.4f}"
                            region = "Coordinates"
                        
                        location_data = {
                            "city": city,
                            "region": region,
                            "country": country,
                            "latitude": float(manual_lat),
                            "longitude": float(manual_lon),
                            "detection_method": "manual_coordinates",
                            "timestamp": time.time(),
                            "service": "manual"
                        }
                        st.session_state['auto_location'] = location_data
                        st.success(f"✅ Coordinates set: {manual_lat:.6f}, {manual_lon:.6f}")
                        st.rerun()
        
        with col_help:
            if not coords_valid:
                if manual_lat == 0.0 and manual_lon == 0.0:
                    st.warning("⚠️ Please enter your actual coordinates (not 0,0)")
                elif not (-90 <= manual_lat <= 90):
                    st.error("❌ Latitude must be between -90 and +90")
                elif not (-180 <= manual_lon <= 180):
                    st.error("❌ Longitude must be between -180 and +180")
            else:
                st.success("✅ Coordinates look valid!")
        
        # Help section
        with st.expander("ℹ️ How to find your coordinates"):
            st.markdown("""
            **Ways to get your GPS coordinates:**
            
            1. **Google Maps**: Right-click on your location → Click the coordinates that appear
            2. **Phone GPS**: Use apps like "GPS Coordinates" or "My Location"
            3. **Device Location**: Try the "Device Location" option above first
            4. **Online Tools**: Search "what are my coordinates" in your browser
            
            **Format:** Decimal degrees (e.g., 40.712776, -74.006000)
            """)
        
        # Return early if manual coordinates not yet set
        if ('auto_location' not in st.session_state or 
            st.session_state['auto_location'].get('detection_method') != 'manual_coordinates'):
            st.info("📍 Please enter and set your coordinates above")
            return None
    
    # Enhanced location status display with accuracy warnings
    if st.session_state.get('auto_location'):
        location_data = st.session_state['auto_location']
        
        # Show basic location info
        city = location_data.get('city', 'Unknown')
        country = location_data.get('country', 'Unknown')
        lat = location_data.get('latitude')
        lon = location_data.get('longitude')
        service = location_data.get('service', 'unknown')
        method = location_data.get('detection_method', 'unknown')
        
        if lat and lon:
            location_text = f"✅ Location detected: {city}, {country} ({lat:.4f}, {lon:.4f})"
        else:
            location_text = f"✅ Location detected: {city}, {country}"
        
        # Show different messages based on detection method
        if method == 'device_location':
            st.success(location_text)
            st.caption("🎯 Detected via Device GPS/WiFi • High accuracy")
        elif method == 'ip_geolocation':
            # Check for common server locations
            server_locations = ['The Dalles', 'Ashburn', 'Council Bluffs', 'Singapore', 'Frankfurt', 'Dublin']
            if city in server_locations:
                st.warning(f"⚠️ {location_text}")
                st.error("🚨 **This appears to be a server location, not your actual location!**")
                st.info("💡 Please use **Device Location** for accurate GPS coordinates.")
            else:
                st.success(location_text)
                st.caption(f"🌐 Detected via IP ({service}) • Moderate accuracy")
        else:
            st.success(location_text)
            st.caption("📍 Manual coordinates • User provided")
        
        return location_data
    else:
        st.warning("📍 Please set your location above")
        
        # Add quick action buttons when no location is set
        col1, col2 = st.columns(2)
        with col1:
            if st.button("� Try Device Location", key="retry_device"):
                st.info("👆 Select 'Device Location (GPS/WiFi)' above")
        with col2:
            if st.button("📍 Use Manual Entry", key="use_manual_entry"):
                st.info("👆 Select 'Enter coordinates manually' above")
        
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

# AI Chatbot - Stage 2
elif data_type == "🤖 AI Chatbot":
    if CHATBOT_AVAILABLE and CLOUD_DB_AVAILABLE:
        render_chatbot_interface()
    elif not CLOUD_DB_AVAILABLE:
        st.header("🤖 AI Chatbot - Database Required")
        st.error("❌ **Database Connection Required**")
        st.markdown("""
        The AI Chatbot requires a working database connection to answer questions about your flora and fauna data.
        
        **To use the chatbot:**
        1. ✅ Ensure Supabase is properly configured
        2. ✅ Check your `.streamlit/secrets.toml` file
        3. ✅ Verify database connectivity in the sidebar
        4. 🔄 Refresh the page once connected
        
        **What the chatbot can do:**
        - 🔍 Search through your collected data
        - 📊 Provide statistics and summaries
        - 🌍 Answer location-based queries
        - 📝 Find specific content by keywords
        """)
    elif not CHATBOT_AVAILABLE:
        st.header("🤖 AI Chatbot - Module Missing")
        st.error("❌ **Chatbot Module Not Available**")
        st.markdown("""
        The chatbot module could not be loaded.
        
        **To fix this:**
        1. ✅ Ensure `chatbot.py` exists in your project directory
        2. ✅ Check for any import errors in the chatbot module
        3. 🔄 Restart your Streamlit app
        """)
        
        # Show expected chatbot features
        st.markdown("---")
        st.markdown("### 🚀 **Stage 2 Features (Coming Soon)**")
        st.info("""
        **AI Chatbot Capabilities:**
        - 🤖 Natural language queries about your data
        - 🔍 Smart search across all collected content
        - 📊 Automated data analysis and insights
        - 🌍 Location-based data exploration
        - 📈 Statistics and trends visualization
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
            # Get all data first
            data_df = supabase_manager.get_all_data()
            
            # Apply client-side filtering if data exists
            if data_df is not None and len(data_df) > 0:
                
                # Filter by data type
                if filter_type != "All":
                    data_df = data_df[data_df['entry_type'] == filter_type.lower()]
                
                # Filter by time range
                if filter_days != "All Time":
                    try:
                        # Convert timestamp to datetime if it's a string
                        if 'timestamp' in data_df.columns:
                            data_df['timestamp_dt'] = pd.to_datetime(data_df['timestamp'])
                            cutoff_date = datetime.datetime.now() - datetime.timedelta(days={"Today": 1, "Last 7 days": 7, "Last 30 days": 30}.get(filter_days, 0))
                            data_df = data_df[data_df['timestamp_dt'] >= cutoff_date]
                    except Exception:
                        pass  # Skip time filtering if there's an issue with dates
                
                # Filter by search term
                if search_term:
                    search_columns = ['title', 'description', 'content']
                    mask = False
                    for col in search_columns:
                        if col in data_df.columns:
                            mask |= data_df[col].astype(str).str.contains(search_term, case=False, na=False)
                    data_df = data_df[mask]
            
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
