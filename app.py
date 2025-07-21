import streamlit as st

# Configure page - MUST be first Streamlit command
st.set_page_config(
    page_title="Flora and Fauna Data Collection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Standard imports
import os
import datetime
import pandas as pd
import json
import streamlit.components.v1 as components

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
                except Exception as e:
                    st.error(f"❌ Could not display image: {e}")
                    st.markdown(f"🔗 [View file directly]({row['file_url']})")
            
            elif data_type == 'audio':
                try:
                    st.audio(row['file_url'])
                    st.markdown(f"🔗 [Download audio]({row['file_url']})")
                except Exception as e:
                    st.error(f"❌ Could not play audio: {e}")
                    st.markdown(f"🔗 [Download file directly]({row['file_url']})")
            
            elif data_type == 'video':
                try:
                    st.video(row['file_url'])
                    st.markdown(f"🔗 [Download video]({row['file_url']})")
                except Exception as e:
                    st.error(f"❌ Could not play video: {e}")
                    st.markdown(f"🔗 [Download file directly]({row['file_url']})")
            
            elif data_type == 'text':
                try:
                    # First, try to show content from database
                    if pd.notna(row.get('content')) and row['content'].strip():
                        st.text_area("� Text Content:", row['content'], height=200, key=f"text_content_{idx}")
                    
                    # Show additional text info if available
                    if pd.notna(row.get('description')) and row['description'] != row.get('content'):
                        st.text_area("📄 Description:", row['description'], height=100, key=f"text_desc_{idx}")
                    
                    # If there's a cloud file URL, show it and allow download
                    if row['file_url']:
                        st.markdown(f"🔗 [Download text file]({row['file_url']})")
                        
                        # Try to fetch and display cloud text file content
                        try:
                            import requests
                            response = requests.get(row['file_url'])
                            if response.status_code == 200:
                                cloud_content = response.text
                                if cloud_content.strip() and cloud_content != row.get('content', ''):
                                    st.text_area("☁️ Cloud File Content:", cloud_content, height=150, key=f"cloud_text_{idx}")
                        except Exception as e:
                            st.info("💡 Click the link above to view the cloud-stored text file")
                    
                except Exception as e:
                    st.error(f"❌ Could not display text: {e}")
            
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
    if 'auto_location' not in st.session_state:
        with st.spinner("🌐 Automatically detecting your location..."):
            try:
                import requests
                response = requests.get('http://ip-api.com/json/', timeout=5)
                if response.status_code == 200:
                    ip_data = response.json()
                    if ip_data.get('status') == 'success':
                        location_data = {
                            "city": ip_data.get("city", "Unknown"),
                            "region": ip_data.get("regionName", "Unknown"), 
                            "country": ip_data.get("country", "Unknown"),
                            "coordinates": {
                                "latitude": ip_data.get("lat"),
                                "longitude": ip_data.get("lon")
                            },
                            "detection_method": "ip_geolocation_auto"
                        }
                        st.session_state['auto_location'] = location_data
                        st.success(f"✅ Location detected: {location_data['city']}, {location_data['country']}")
                    else:
                        st.error("❌ Location detection failed")
                        st.session_state['auto_location'] = None
                else:
                    st.error("❌ Failed to connect to location service")
                    st.session_state['auto_location'] = None
            except Exception as e:
                st.error(f"❌ Location detection error: {str(e)}")
                st.session_state['auto_location'] = None
    
    # Display current location
    if st.session_state.get('auto_location'):
        location_data = st.session_state['auto_location']
        st.info(f"📍 **Current Location**: {location_data['city']}, {location_data['country']} ({location_data['coordinates']['latitude']:.4f}, {location_data['coordinates']['longitude']:.4f})")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Location"):
                del st.session_state['auto_location']
                st.rerun()
        with col2:
            override = st.checkbox("✏️ Edit location")
        
        if override:
            new_city = st.text_input("City:", value=location_data['city'])
            new_country = st.text_input("Country:", value=location_data['country'])
            new_coords = st.text_input("Coordinates:", value=f"{location_data['coordinates']['latitude']}, {location_data['coordinates']['longitude']}")
            if st.button("Update") and new_city and new_country and new_coords:
                try:
                    lat, lon = map(float, new_coords.split(','))
                    st.session_state['auto_location'].update({
                        "city": new_city, "country": new_country, 
                        "coordinates": {"latitude": lat, "longitude": lon},
                        "detection_method": "manual_override"
                    })
                    st.success("✅ Location updated!")
                    st.rerun()
                except ValueError:
                    st.error("❌ Invalid coordinates format. Use: latitude, longitude")
        
        return location_data
    else:
        st.error("❌ Location detection failed. Location is required for uploads.")
        return None

def get_location_component():
    """Create a location input component with automatic detection"""
    st.subheader("📍 Location Information")
    
    # Initialize session state for location
    if 'location_data' not in st.session_state:
        st.session_state.location_data = {"status": "not_detected"}
    
    # Auto-detect location button
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🌍 Detect My Location", type="primary", help="Automatically detect your current location"):
            # HTML and JavaScript for geolocation
            location_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    .location-container {
                        padding: 20px;
                        border-radius: 10px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        text-align: center;
                        margin: 10px 0;
                    }
                    .location-info {
                        background: rgba(255,255,255,0.1);
                        padding: 15px;
                        border-radius: 8px;
                        margin: 10px 0;
                    }
                    .loading {
                        animation: pulse 2s infinite;
                    }
                    @keyframes pulse {
                        0% { opacity: 1; }
                        50% { opacity: 0.5; }
                        100% { opacity: 1; }
                    }
                    .success { color: #4CAF50; }
                    .error { color: #f44336; }
                </style>
            </head>
            <body>
                <div class="location-container">
                    <h3>📍 Automatic Location Detection</h3>
                    <div id="status" class="loading">🔍 Detecting your location...</div>
                    <div id="location-info" class="location-info" style="display:none;">
                        <div id="coordinates"></div>
                        <div id="address"></div>
                    </div>
                </div>

                <script>
                function getLocation() {
                    const statusEl = document.getElementById('status');
                    const locationInfoEl = document.getElementById('location-info');
                    const coordinatesEl = document.getElementById('coordinates');
                    const addressEl = document.getElementById('address');

                    if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition(
                            function(position) {
                                const lat = position.coords.latitude;
                                const lon = position.coords.longitude;
                                const accuracy = position.coords.accuracy;
                                
                                statusEl.innerHTML = '✅ Location detected successfully!';
                                statusEl.className = 'success';
                                
                                coordinatesEl.innerHTML = `
                                    <strong>📍 Coordinates:</strong><br>
                                    Latitude: ${lat.toFixed(6)}<br>
                                    Longitude: ${lon.toFixed(6)}<br>
                                    Accuracy: ±${Math.round(accuracy)}m
                                `;
                                
                                locationInfoEl.style.display = 'block';
                                
                                // Store coordinates in a way Streamlit can access
                                window.detectedLocation = {
                                    latitude: lat,
                                    longitude: lon,
                                    accuracy: accuracy,
                                    timestamp: new Date().toISOString()
                                };
                                
                                // Try to get address using reverse geocoding
                                fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${lat}&longitude=${lon}&localityLanguage=en`)
                                    .then(response => response.json())
                                    .then(data => {
                                        const city = data.city || data.locality || 'Unknown';
                                        const region = data.principalSubdivision || data.region || '';
                                        const country = data.countryName || 'Unknown';
                                        
                                        const fullAddress = `${city}, ${region}, ${country}`.replace(/, ,/g, ',').replace(/^,|,$/g, '');
                                        
                                        addressEl.innerHTML = `
                                            <strong>🏠 Address:</strong><br>
                                            ${fullAddress}<br>
                                            <small>City: ${city} | Country: ${country}</small>
                                        `;
                                        
                                        // Update stored location with address info
                                        window.detectedLocation.city = city;
                                        window.detectedLocation.region = region;
                                        window.detectedLocation.country = country;
                                        window.detectedLocation.full_address = fullAddress;
                                    })
                                    .catch(error => {
                                        addressEl.innerHTML = `
                                            <strong>🏠 Address:</strong><br>
                                            <span style="color: #ffeb3b;">Address lookup failed, but coordinates are available</span>
                                        `;
                                    });
                            },
                            function(error) {
                                let errorMessage = '';
                                switch(error.code) {
                                    case error.PERMISSION_DENIED:
                                        errorMessage = '❌ Location access denied by user. Please enable location permissions.';
                                        break;
                                    case error.POSITION_UNAVAILABLE:
                                        errorMessage = '❌ Location information unavailable.';
                                        break;
                                    case error.TIMEOUT:
                                        errorMessage = '❌ Location request timed out.';
                                        break;
                                    default:
                                        errorMessage = '❌ An unknown error occurred while retrieving location.';
                                        break;
                                }
                                statusEl.innerHTML = errorMessage;
                                statusEl.className = 'error';
                            },
                            {
                                enableHighAccuracy: true,
                                timeout: 10000,
                                maximumAge: 0
                            }
                        );
                    } else {
                        statusEl.innerHTML = '❌ Geolocation is not supported by this browser.';
                        statusEl.className = 'error';
                    }
                }

                // Auto-run on load
                getLocation();
                </script>
            </body>
            </html>
            """
            
            st.components.v1.html(location_html, height=300)
            
            # Instructions for the user
            st.info("""
            **How automatic location detection works:**
            1. 🔒 Your browser will ask for location permission
            2. 📍 Allow access to detect your current location
            3. ✅ Location data will be automatically captured
            4. 🏠 Address will be looked up from coordinates
            
            **Note:** Location data stays on your device and is only used for this data collection.
            """)
    
    with col2:
        # IP-based location as backup
        st.write("**🌐 Backup Option:**")
        if st.button("Use IP Location", help="Get approximate location from IP"):
            try:
                # Simple IP geolocation
                import requests
                response = requests.get('http://ip-api.com/json/', timeout=5)
                if response.status_code == 200:
                    ip_data = response.json()
                    st.success("✅ IP location detected!")
                    ip_location = {
                        "city": ip_data.get("city"),
                        "region": ip_data.get("regionName"),
                        "country": ip_data.get("country"),
                        "latitude": ip_data.get("lat"),
                        "longitude": ip_data.get("lon"),
                        "detection_method": "ip_geolocation"
                    }
                    st.json(ip_location)
                    st.session_state['backup_location'] = ip_location
                else:
                    st.error("Failed to get IP location")
            except Exception as e:
                st.error(f"IP location failed: {str(e)}")
        
        # Manual override option
        st.write("**✏️ Manual Override:**")
        manual_location = st.text_input("Custom location:", placeholder="Override detected location", key="manual_loc")
        manual_coordinates = st.text_input("Custom coordinates:", placeholder="lat, lng", key="manual_coords")
    
    # Create location data object
    location_data = {"detection_method": "automatic"}
    
    # Add manual overrides if provided
    if manual_location:
        location_data["manual_override"] = manual_location
        location_data["detection_method"] = "manual_override"
    
    if manual_coordinates:
        try:
            coord_parts = manual_coordinates.split(',')
            if len(coord_parts) == 2:
                lat = float(coord_parts[0].strip())
                lon = float(coord_parts[1].strip())
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    location_data["coordinates"] = {"latitude": lat, "longitude": lon}
                    location_data["detection_method"] = "manual_coordinates"
                else:
                    st.error("Coordinates must be within valid ranges: -90 to 90 for latitude, -180 to 180 for longitude")
        except ValueError:
            st.warning("Invalid coordinate format. Use: latitude, longitude (e.g., 40.7128, -74.0060)")
    
    # Use backup IP location if available and no manual override
    if 'backup_location' in st.session_state and not manual_location and not manual_coordinates:
        backup = st.session_state['backup_location']
        location_data.update(backup)
    
    # Store timestamp
    location_data["timestamp"] = datetime.datetime.now().isoformat()
    
    # Display current location data status
    has_location_data = (
        location_data.get("detection_method") != "automatic" or 
        manual_location or 
        manual_coordinates or 
        'backup_location' in st.session_state
    )
    
    if has_location_data:
        st.success("✅ Location data ready for upload!")
        with st.expander("📋 View location data to be saved"):
            st.json(location_data)
    else:
        st.info("""
        🌍 **Location Options Available:**
        • **Automatic Detection**: Click 'Detect My Location' for precise GPS location
        • **IP Location**: Use 'Use IP Location' for approximate location
        • **Manual Entry**: Enter location details manually
        """)
        
        st.warning("⚠️ **For automatic location detection:**\n"
                  "• Allow location permissions when prompted\n"
                  "• Make sure location services are enabled\n"
                  "• Use HTTPS (secure connection) for best results")
    
    return location_data

# Text Data Collection
if data_type == "📝 Text Data":
    st.header("📝 Text Data Collection")
    
    # Mandatory Auto-Location Detection
    st.subheader("📍 Location (Auto-Detected)")
    
    # Auto-fetch location on first load
    if 'auto_location' not in st.session_state:
        with st.spinner("🌐 Automatically detecting your location..."):
            try:
                import requests
                response = requests.get('http://ip-api.com/json/', timeout=5)
                if response.status_code == 200:
                    ip_data = response.json()
                    if ip_data.get('status') == 'success':
                        location_data = {
                            "city": ip_data.get("city", "Unknown"),
                            "region": ip_data.get("regionName", "Unknown"), 
                            "country": ip_data.get("country", "Unknown"),
                            "latitude": ip_data.get("lat"),
                            "longitude": ip_data.get("lon"),
                            "detection_method": "ip_geolocation_auto"
                        }
                        st.session_state['auto_location'] = location_data
                        st.success(f"✅ Location detected: {location_data['city']}, {location_data['country']}")
                    else:
                        st.error("❌ Location detection failed")
                        st.session_state['auto_location'] = None
                else:
                    st.error("❌ Failed to connect to location service")
                    st.session_state['auto_location'] = None
            except Exception as e:
                st.error(f"❌ Location detection error: {str(e)}")
                st.session_state['auto_location'] = None
    
    # Display current location
    if st.session_state.get('auto_location'):
        location_data = st.session_state['auto_location']
        st.info(f"📍 **Current Location**: {location_data['city']}, {location_data['country']} ({location_data['latitude']:.4f}, {location_data['longitude']:.4f})")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Location"):
                del st.session_state['auto_location']
                st.rerun()
        with col2:
            override = st.checkbox("✏️ Edit location")
        
        if override:
            new_city = st.text_input("City:", value=location_data['city'])
            new_country = st.text_input("Country:", value=location_data['country'])
            new_coords = st.text_input("Coordinates:", value=f"{location_data['latitude']}, {location_data['longitude']}")
            if st.button("Update") and new_city and new_country and new_coords:
                try:
                    lat, lon = map(float, new_coords.split(','))
                    st.session_state['auto_location'].update({
                        "city": new_city, "country": new_country, 
                        "latitude": lat, "longitude": lon,
                        "detection_method": "manual_override"
                    })
                    st.success("✅ Location updated!")
                    st.rerun()
                except:
                    st.error("❌ Invalid coordinates format")
    else:
        st.error("❌ **Location is required for data upload**")
        st.warning("Please provide location manually:")
        manual_city = st.text_input("City (Required):")
        manual_country = st.text_input("Country (Required):")
        manual_coords = st.text_input("Coordinates (lat, lng):")
        
        if st.button("🌐 Try Auto-Detect Again"):
            if 'auto_location' in st.session_state:
                del st.session_state['auto_location']
            st.rerun()
        
        if manual_city and manual_country and manual_coords:
            try:
                lat, lon = map(float, manual_coords.split(','))
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    location_data = {
                        "city": manual_city, "country": manual_country,
                        "latitude": lat, "longitude": lon,
                        "detection_method": "manual_required"
                    }
                    st.session_state['auto_location'] = location_data
                    st.success("✅ Manual location set!")
                    st.rerun()
                else:
                    st.error("❌ Invalid coordinate range")
            except:
                st.error("❌ Invalid coordinate format")
        
        location_data = None  # No valid location
    
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
                # Check if location is available
                if not location_data:
                    st.error("❌ Location is required! Please set your location above before saving.")
                else:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"text_{timestamp}.txt"
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
                # Check if location is available
                if not location_data:
                    st.error("❌ Location is required! Please set your location above before saving.")
                else:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"multitext_{timestamp}.txt"
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
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"csv_{timestamp}.csv"
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
    
    # Auto-fetch location on first load
    if 'auto_location' not in st.session_state:
        with st.spinner("🌐 Automatically detecting your location..."):
            try:
                import requests
                response = requests.get('http://ip-api.com/json/', timeout=5)
                if response.status_code == 200:
                    ip_data = response.json()
                    if ip_data.get('status') == 'success':
                        location_data = {
                            "city": ip_data.get("city", "Unknown"),
                            "region": ip_data.get("regionName", "Unknown"), 
                            "country": ip_data.get("country", "Unknown"),
                            "latitude": ip_data.get("lat"),
                            "longitude": ip_data.get("lon"),
                            "detection_method": "ip_geolocation_auto"
                        }
                        st.session_state['auto_location'] = location_data
                        st.success(f"✅ Location detected: {location_data['city']}, {location_data['country']}")
                    else:
                        st.error("❌ Location detection failed")
                        st.session_state['auto_location'] = None
                else:
                    st.error("❌ Failed to connect to location service")
                    st.session_state['auto_location'] = None
            except Exception as e:
                st.error(f"❌ Location detection error: {str(e)}")
                st.session_state['auto_location'] = None
    
    # Display current location
    if st.session_state.get('auto_location'):
        location_data = st.session_state['auto_location']
        st.info(f"📍 **Current Location**: {location_data['city']}, {location_data['country']} ({location_data['latitude']:.4f}, {location_data['longitude']:.4f})")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Location", key="audio_refresh_location"):
                del st.session_state['auto_location']
                st.rerun()
        with col2:
            override_audio = st.checkbox("✏️ Edit location", key="audio_edit_location")
        
        if override_audio:
            new_city = st.text_input("City:", value=location_data['city'], key="audio_city")
            new_country = st.text_input("Country:", value=location_data['country'], key="audio_country")
            new_coords = st.text_input("Coordinates:", value=f"{location_data['latitude']}, {location_data['longitude']}", key="audio_coords")
            if st.button("Update Location", key="audio_update_location") and new_city and new_country and new_coords:
                try:
                    lat, lon = map(float, new_coords.split(','))
                    st.session_state['auto_location'].update({
                        "city": new_city, "country": new_country, 
                        "latitude": lat, "longitude": lon,
                        "detection_method": "manual_override"
                    })
                    st.success("✅ Location updated!")
                    st.rerun()
                except ValueError:
                    st.error("❌ Invalid coordinates format. Use: latitude, longitude")
    else:
        st.error("❌ Location detection failed. Location is required for uploads.")
        
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
                # Use the location from session state
                location_data = st.session_state.get('auto_location')
                if not location_data:
                    st.error("❌ Location is required! Please ensure location is detected above.")
                else:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_extension = uploaded_audio.name.split('.')[-1]
                    filename = f"audio_{timestamp}.{file_extension}"
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
                        st.success(f"🎵 Audio saved successfully as {filename}")
                        st.info(f"💾 Stored in: Supabase (ID: {data_id})")
                        st.info(f"📍 Location: {location_data.get('city', 'Unknown')}, {location_data.get('country', 'Unknown')}")
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
    
    # Auto-fetch location on first load
    if 'auto_location' not in st.session_state:
        with st.spinner("🌐 Automatically detecting your location..."):
            try:
                import requests
                response = requests.get('http://ip-api.com/json/', timeout=5)
                if response.status_code == 200:
                    ip_data = response.json()
                    if ip_data.get('status') == 'success':
                        location_data = {
                            "city": ip_data.get("city", "Unknown"),
                            "region": ip_data.get("regionName", "Unknown"), 
                            "country": ip_data.get("country", "Unknown"),
                            "latitude": ip_data.get("lat"),
                            "longitude": ip_data.get("lon"),
                            "detection_method": "ip_geolocation_auto"
                        }
                        st.session_state['auto_location'] = location_data
                        st.success(f"✅ Location detected: {location_data['city']}, {location_data['country']}")
                    else:
                        st.error("❌ Location detection failed")
                        st.session_state['auto_location'] = None
                else:
                    st.error("❌ Failed to connect to location service")
                    st.session_state['auto_location'] = None
            except Exception as e:
                st.error(f"❌ Location detection error: {str(e)}")
                st.session_state['auto_location'] = None
    
    # Display current location
    if st.session_state.get('auto_location'):
        location_data = st.session_state['auto_location']
        st.info(f"📍 **Current Location**: {location_data['city']}, {location_data['country']} ({location_data['latitude']:.4f}, {location_data['longitude']:.4f})")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Location", key="video_refresh_location"):
                del st.session_state['auto_location']
                st.rerun()
        with col2:
            override_video = st.checkbox("✏️ Edit location", key="video_edit_location")
        
        if override_video:
            new_city = st.text_input("City:", value=location_data['city'], key="video_city")
            new_country = st.text_input("Country:", value=location_data['country'], key="video_country")
            new_coords = st.text_input("Coordinates:", value=f"{location_data['latitude']}, {location_data['longitude']}", key="video_coords")
            if st.button("Update Location", key="video_update_location") and new_city and new_country and new_coords:
                try:
                    lat, lon = map(float, new_coords.split(','))
                    st.session_state['auto_location'].update({
                        "city": new_city, "country": new_country, 
                        "latitude": lat, "longitude": lon,
                        "detection_method": "manual_override"
                    })
                    st.success("✅ Location updated!")
                    st.rerun()
                except ValueError:
                    st.error("❌ Invalid coordinates format. Use: latitude, longitude")
    else:
        st.error("❌ Location detection failed. Location is required for uploads.")
        
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
                # Use the location from session state
                location_data = st.session_state.get('auto_location')
                if not location_data:
                    st.error("❌ Location is required! Please ensure location is detected above.")
                else:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_extension = uploaded_video.name.split('.')[-1]
                    filename = f"video_{timestamp}.{file_extension}"
                    
                    # Get file data
                    file_data = uploaded_video.getbuffer()
                    file_bytes = bytes(file_data)  # Convert memoryview to bytes
                    
                    # Save to cloud storage
                    additional_info = {
                        "category": video_category,
                        "duration": duration,
                        "resolution": resolution,
                        "description": description,
                        "tags": [tag.strip() for tag in tags.split(',') if tag.strip()],
                        "original_name": uploaded_video.name,
                        "file_size": len(file_bytes)
                    }
                    
                    if CLOUD_DB_AVAILABLE:
                        data_id = supabase_manager.save_data("video", filename, file_bytes, additional_info, location_data)
                        st.success(f"🎥 Video saved successfully as {filename}")
                        st.info(f"💾 Stored in: Supabase (ID: {data_id})")
                        st.info(f"📍 Location: {location_data.get('city', 'Unknown')}, {location_data.get('country', 'Unknown')}")
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
    
    # Auto-fetch location on first load
    if 'auto_location' not in st.session_state:
        with st.spinner("🌐 Automatically detecting your location..."):
            try:
                import requests
                response = requests.get('http://ip-api.com/json/', timeout=5)
                if response.status_code == 200:
                    ip_data = response.json()
                    if ip_data.get('status') == 'success':
                        location_data = {
                            "city": ip_data.get("city", "Unknown"),
                            "region": ip_data.get("regionName", "Unknown"), 
                            "country": ip_data.get("country", "Unknown"),
                            "latitude": ip_data.get("lat"),
                            "longitude": ip_data.get("lon"),
                            "detection_method": "ip_geolocation_auto"
                        }
                        st.session_state['auto_location'] = location_data
                        st.success(f"✅ Location detected: {location_data['city']}, {location_data['country']}")
                    else:
                        st.error("❌ Location detection failed")
                        st.session_state['auto_location'] = None
                else:
                    st.error("❌ Failed to connect to location service")
                    st.session_state['auto_location'] = None
            except Exception as e:
                st.error(f"❌ Location detection error: {str(e)}")
                st.session_state['auto_location'] = None
    
    # Display current location
    if st.session_state.get('auto_location'):
        location_data = st.session_state['auto_location']
        st.info(f"📍 **Current Location**: {location_data['city']}, {location_data['country']} ({location_data['latitude']:.4f}, {location_data['longitude']:.4f})")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Location", key="image_refresh_location"):
                del st.session_state['auto_location']
                st.rerun()
        with col2:
            override_image = st.checkbox("✏️ Edit location", key="image_edit_location")
        
        if override_image:
            new_city = st.text_input("City:", value=location_data['city'], key="image_city")
            new_country = st.text_input("Country:", value=location_data['country'], key="image_country")
            new_coords = st.text_input("Coordinates:", value=f"{location_data['latitude']}, {location_data['longitude']}", key="image_coords")
            if st.button("Update Location", key="image_update_location") and new_city and new_country and new_coords:
                try:
                    lat, lon = map(float, new_coords.split(','))
                    st.session_state['auto_location'].update({
                        "city": new_city, "country": new_country, 
                        "latitude": lat, "longitude": lon,
                        "detection_method": "manual_override"
                    })
                    st.success("✅ Location updated!")
                    st.rerun()
                except ValueError:
                    st.error("❌ Invalid coordinates format. Use: latitude, longitude")
    else:
        st.error("❌ Location detection failed. Location is required for uploads.")
        
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
                # Use the location from session state
                location_data = st.session_state.get('auto_location')
                if not location_data:
                    st.error("❌ Location is required! Please ensure location is detected above.")
                else:
                    saved_files = []
                    for uploaded_image in uploaded_images:
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        file_extension = uploaded_image.name.split('.')[-1]
                        filename = f"image_{timestamp}_{uploaded_image.name}"
                        
                        # Get file data
                        file_data = uploaded_image.getbuffer()
                        file_bytes = bytes(file_data)  # Convert memoryview to bytes
                        
                        # Save to cloud storage
                        additional_info = {
                            "category": image_category,
                            "description": description,
                            "tags": [tag.strip() for tag in tags.split(',') if tag.strip()],
                            "original_name": uploaded_image.name,
                            "file_size": len(file_bytes)
                        }
                        
                        if CLOUD_DB_AVAILABLE:
                            data_id = supabase_manager.save_data("image", filename, file_bytes, additional_info, location_data)
                            saved_files.append((filename, data_id))
                        else:
                            st.error("❌ Failed to save to cloud storage. Please check your Supabase connection.")
                            break
                    
                    if CLOUD_DB_AVAILABLE:
                        st.success(f"🖼️ Successfully saved {len(saved_files)} images!")
                        st.info(f"💾 Stored in: Supabase")
                        st.info(f"📍 Location: {location_data.get('city', 'Unknown')}, {location_data.get('country', 'Unknown')}")
                        for filename, data_id in saved_files:
                            st.write(f"• {filename} (ID: {data_id})")
                        for filename, _ in saved_files:
                            st.write(f"• {filename}")
    
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
            st.success(f"🌐 **Current Database**: Supabase")
        
        with col2:
            st.metric("📊 Provider", "SUPABASE")
        
        with col3:
            st.metric("🔗 Status", "Connected")
    
    # Get database statistics
    if CLOUD_DB_AVAILABLE:
        db_stats = supabase_manager.get_statistics()
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Records", db_stats['total_records'])
        with col2:
            text_count = db_stats['type_counts'].get('text', 0)
            st.metric("📝 Text Records", text_count)
        with col3:
            audio_count = db_stats['type_counts'].get('audio', 0)
            st.metric("🎵 Audio Records", audio_count)
        with col4:
            other_count = sum(v for k, v in db_stats['type_counts'].items() if k not in ['text', 'audio'])
            st.metric("🎥🖼️ Other Records", other_count)
        
        # Load and display data
        if db_stats['total_records'] > 0:
            df = supabase_manager.get_all_data()
            
            st.markdown("---")
            st.subheader("🗄️ Database Records")
            
            # Filter options
            if not df.empty:
                # Use correct column name (entry_type instead of data_type)
                data_types = ['All'] + list(df['entry_type'].unique())
                selected_type = st.selectbox("Filter by data type:", data_types)
                
                if selected_type != 'All':
                    filtered_df = df[df['entry_type'] == selected_type]
                else:
                    filtered_df = df
                
                # Enhanced data display with preview
                if not filtered_df.empty:
                    st.info(f"📋 Showing {len(filtered_df)} records")
                    
                    # Display each record with preview capability
                    for idx, row in filtered_df.iterrows():
                        with st.container():
                            st.markdown("---")
                            
                            col1, col2, col3 = st.columns([2, 1, 1])
                            
                            with col1:
                                st.subheader(f"{row['entry_type'].title()}: {row['title']}")
                                if pd.notna(row.get('content')):
                                    st.write(f"📝 {row['content']}")
                                # Extract metadata for additional info
                                metadata = row.get('metadata', {})
                                if isinstance(metadata, dict):
                                    if metadata.get('category'):
                                        st.write(f"🏷️ Category: {metadata['category']}")
                                    if metadata.get('description'):
                                        st.write(f"📄 Description: {metadata['description']}")
                                    if metadata.get('tags'):
                                        st.write(f"🔖 Tags: {metadata['tags']}")
                            
                            with col2:
                                if pd.notna(row.get('timestamp')):
                                    try:
                                        timestamp = pd.to_datetime(row['timestamp'])
                                        st.write(f"📅 {timestamp.strftime('%Y-%m-%d %H:%M')}")
                                    except:
                                        st.write(f"📅 {row['timestamp']}")
                                if pd.notna(row.get('location_name')):
                                    st.write(f"📍 {row['location_name']}")
                                # Extract file size from metadata
                                metadata = row.get('metadata', {})
                                if isinstance(metadata, dict) and metadata.get('file_size'):
                                    try:
                                        size_mb = float(metadata['file_size']) / (1024 * 1024)
                                        if size_mb < 1:
                                            size_kb = float(metadata['file_size']) / 1024
                                            st.write(f"📦 Size: {size_kb:.1f} KB")
                                        else:
                                            st.write(f"📦 Size: {size_mb:.1f} MB")
                                    except:
                                        st.write(f"📦 Size: {metadata['file_size']}")
                            
                            with col3:
                                # Preview/View button
                                if st.button(f"👁️ View", key=f"view_{idx}"):
                                    st.session_state[f"show_preview_{idx}"] = True
                                
                                # Storage info
                                if pd.notna(row.get('file_url')) and isinstance(row['file_url'], str) and row['file_url'].startswith('http'):
                                    st.success("☁️ Cloud Stored")
                                else:
                                    st.info("💾 Local File")
                            
                            # Show preview if requested
                            if st.session_state.get(f"show_preview_{idx}", False):
                                display_file_preview(row, idx)
                    
                    st.markdown("---")
                    # Download options
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        csv_data = filtered_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Filtered CSV",
                            data=csv_data,
                            file_name=f"filtered_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        all_csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download All Data CSV",
                            data=all_csv,
                            file_name=f"all_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col3:
                        # Provider-specific info
                        st.write(f"**Supabase**")
                        st.write("Cloud Storage: ✅")
                        st.write("Real-time sync: ✅")
                else:
                    st.info("No data found for the selected filter.")
            else:
                st.info("No data structure available to display.")
        else:
            st.info("🗄️ No data in database yet. Start collecting data to see it here!")
    
    else:
        st.error("❌ Cloud database not available. Please check your Supabase connection.")

# Footer
st.markdown("---")
if CLOUD_DB_AVAILABLE:
    st.markdown(f"""
    <div style="text-align: center; color: #666;">
        <p>🌿 Flora and Fauna Data Collection | Built with Streamlit</p>
        <p>💾 Database: Supabase (Cloud) | 🌐 Real-time sync enabled</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🌿 Flora and Fauna Data Collection | Built with Streamlit</p>
        <p>⚠️ Cloud database not available</p>
    </div>
    """, unsafe_allow_html=True)
