import streamlit as st
import os
import datetime
import pandas as pd
from pathlib import Path
import json
import requests
import streamlit.components.v1 as components

# Configure page
st.set_page_config(
    page_title="Data Collection App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create directories for storing collected data
def create_directories():
    directories = ['data/text', 'data/audio', 'data/video', 'data/images']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

create_directories()

# Main title
st.title("📊 Multi-Media Data Collection Application")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("🗂️ Data Collection Types")
data_type = st.sidebar.radio(
    "Select data type to collect:",
    ["📝 Text Data", "🎵 Audio Data", "🎥 Video Data", "🖼️ Image Data", "📈 View Collected Data"]
)

# Function to save metadata with location
def save_metadata(data_type, filename, additional_info=None, location_data=None):
    metadata = {
        "timestamp": datetime.datetime.now().isoformat(),
        "data_type": data_type,
        "filename": filename,
        "location": location_data,
        "additional_info": additional_info or {}
    }
    
    metadata_file = "data/metadata.json"
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            all_metadata = json.load(f)
    else:
        all_metadata = []
    
    all_metadata.append(metadata)
    
    with open(metadata_file, 'w') as f:
        json.dump(all_metadata, f, indent=2)

# Location Component
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
    
    # Location component
    location_data = get_location_component()
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
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"text_{timestamp}.txt"
                filepath = f"data/text/{filename}"
                
                with open(filepath, 'w') as f:
                    f.write(f"Category: {category}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Content: {text_input}\n")
                
                save_metadata("text", filename, {"category": category, "method": "single_entry"}, location_data)
                st.success(f"Text saved successfully as {filename}")
        
        elif input_method == "Multi-line Text":
            text_area = st.text_area("Enter multi-line text:", height=200, placeholder="Enter your multi-line text here...")
            category = st.selectbox("Category:", ["General", "Research", "Survey", "Feedback", "Other"])
            
            if st.button("Save Multi-line Text") and text_area:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"multitext_{timestamp}.txt"
                filepath = f"data/text/{filename}"
                
                with open(filepath, 'w') as f:
                    f.write(f"Category: {category}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Content:\n{text_area}\n")
                
                save_metadata("text", filename, {"category": category, "method": "multi_line"}, location_data)
                st.success(f"Multi-line text saved successfully as {filename}")
        
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
                    
                    save_metadata("text", filename, {"method": "csv_upload", "rows": len(df), "columns": list(df.columns)}, location_data)
                    st.success(f"CSV data saved successfully as {filename}")
    
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
    
    # Location component
    location_data = get_location_component()
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
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_extension = uploaded_audio.name.split('.')[-1]
                filename = f"audio_{timestamp}.{file_extension}"
                filepath = f"data/audio/{filename}"
                
                with open(filepath, 'wb') as f:
                    f.write(uploaded_audio.getbuffer())
                
                save_metadata("audio", filename, {
                    "category": audio_category,
                    "duration": duration,
                    "description": description,
                    "original_name": uploaded_audio.name
                }, location_data)
                st.success(f"Audio saved successfully as {filename}")
        
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
    
    # Location component
    location_data = get_location_component()
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
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_extension = uploaded_video.name.split('.')[-1]
                filename = f"video_{timestamp}.{file_extension}"
                filepath = f"data/video/{filename}"
                
                with open(filepath, 'wb') as f:
                    f.write(uploaded_video.getbuffer())
                
                save_metadata("video", filename, {
                    "category": video_category,
                    "duration": duration,
                    "resolution": resolution,
                    "description": description,
                    "tags": [tag.strip() for tag in tags.split(',') if tag.strip()],
                    "original_name": uploaded_video.name
                }, location_data)
                st.success(f"Video saved successfully as {filename}")
    
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
    
    # Location component
    location_data = get_location_component()
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
                saved_files = []
                for uploaded_image in uploaded_images:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_extension = uploaded_image.name.split('.')[-1]
                    filename = f"image_{timestamp}_{uploaded_image.name}"
                    filepath = f"data/images/{filename}"
                    
                    with open(filepath, 'wb') as f:
                        f.write(uploaded_image.getbuffer())
                    
                    save_metadata("image", filename, {
                        "category": image_category,
                        "description": description,
                        "tags": [tag.strip() for tag in tags.split(',') if tag.strip()],
                        "original_name": uploaded_image.name
                    }, location_data)
                    saved_files.append(filename)
                
                st.success(f"Successfully saved {len(saved_files)} images!")
                for filename in saved_files:
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
    st.header("📈 Collected Data Overview")
    
    # Load metadata
    metadata_file = "data/metadata.json"
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            all_metadata = json.load(f)
        
        if all_metadata:
            # Convert to DataFrame for better display
            df = pd.DataFrame(all_metadata)
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                text_count = len([m for m in all_metadata if m['data_type'] == 'text'])
                st.metric("📝 Text Files", text_count)
            
            with col2:
                audio_count = len([m for m in all_metadata if m['data_type'] == 'audio'])
                st.metric("🎵 Audio Files", audio_count)
            
            with col3:
                video_count = len([m for m in all_metadata if m['data_type'] == 'video'])
                st.metric("🎥 Video Files", video_count)
            
            with col4:
                image_count = len([m for m in all_metadata if m['data_type'] == 'image'])
                st.metric("🖼️ Image Files", image_count)
            
            st.markdown("---")
            
            # Location Statistics
            st.subheader("🌍 Location Statistics")
            
            # Extract location data
            locations = []
            countries = []
            cities = []
            
            for metadata in all_metadata:
                location = metadata.get('location', {})
                if isinstance(location, dict) and location.get('status') != 'not_provided':
                    if location.get('manual_location'):
                        locations.append(location['manual_location'])
                    if location.get('country'):
                        countries.append(location['country'])
                    if location.get('city'):
                        cities.append(location['city'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if countries:
                    country_counts = pd.Series(countries).value_counts()
                    st.write("**Top Countries:**")
                    for country, count in country_counts.head(5).items():
                        st.write(f"🏳️ {country}: {count}")
                else:
                    st.write("**Countries:** No data")
            
            with col2:
                if cities:
                    city_counts = pd.Series(cities).value_counts()
                    st.write("**Top Cities:**")
                    for city, count in city_counts.head(5).items():
                        st.write(f"🏙️ {city}: {count}")
                else:
                    st.write("**Cities:** No data")
            
            with col3:
                total_with_location = len([m for m in all_metadata if m.get('location', {}).get('status') != 'not_provided'])
                location_percentage = (total_with_location / len(all_metadata)) * 100 if all_metadata else 0
                st.metric("📍 Data with Location", f"{total_with_location}/{len(all_metadata)}", f"{location_percentage:.1f}%")
            
            st.markdown("---")
            
            # Detailed view
            st.subheader("📋 Detailed Data Records")
            
            # Filter options
            data_type_filter = st.selectbox("Filter by data type:", ["All", "text", "audio", "video", "image"])
            
            if data_type_filter != "All":
                filtered_df = df[df['data_type'] == data_type_filter]
            else:
                filtered_df = df
            
            # Display the data
            if not filtered_df.empty:
                # Expand the dataframe to show location information better
                display_df = filtered_df.copy()
                
                # Extract location info for better display
                location_info = []
                for idx, row in display_df.iterrows():
                    location = row.get('location', {})
                    if isinstance(location, dict):
                        loc_str = ""
                        if location.get('manual_location'):
                            loc_str += f"📍 {location['manual_location']}"
                        if location.get('city') or location.get('country'):
                            city = location.get('city', '')
                            country = location.get('country', '')
                            loc_str += f" 🏙️ {city}, {country}".strip(', ')
                        if location.get('coordinates'):
                            coords = location['coordinates']
                            loc_str += f" 🗺️ ({coords.get('latitude', '')}, {coords.get('longitude', '')})"
                        location_info.append(loc_str if loc_str else "Not provided")
                    else:
                        location_info.append("Not provided")
                
                display_df['location_summary'] = location_info
                
                st.dataframe(display_df, use_container_width=True)
                
                # Download option
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"collected_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No data found for the selected filter.")
        else:
            st.info("No data has been collected yet.")
    else:
        st.info("No data has been collected yet. Start by collecting some data using the other tabs!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>📊 Multi-Media Data Collection Application | Built with Streamlit</p>
    <p>Collected data is stored locally in the 'data' directory</p>
</div>
""", unsafe_allow_html=True)
