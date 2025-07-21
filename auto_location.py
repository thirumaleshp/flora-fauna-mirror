def get_auto_location():
    """Automatically get location using IP geolocation and make it mandatory"""
    
    # Auto-fetch location on first load or if requested
    if 'mandatory_location' not in st.session_state:
        with st.spinner("🌐 Automatically detecting your location..."):
            try:
                import requests
                response = requests.get('http://ip-api.com/json/', timeout=5)
                if response.status_code == 200:
                    ip_data = response.json()
                    if ip_data.get('status') == 'success':
                        auto_location = {
                            "city": ip_data.get("city", "Unknown"),
                            "region": ip_data.get("regionName", "Unknown"), 
                            "country": ip_data.get("country", "Unknown"),
                            "latitude": ip_data.get("lat"),
                            "longitude": ip_data.get("lon"),
                            "detection_method": "ip_geolocation_auto",
                            "timestamp": datetime.datetime.now().isoformat()
                        }
                        st.session_state['mandatory_location'] = auto_location
                        st.success(f"✅ Location auto-detected: {auto_location['city']}, {auto_location['country']}")
                        st.success(f"📍 Coordinates: {auto_location['latitude']:.4f}, {auto_location['longitude']:.4f}")
                    else:
                        st.error("❌ Location detection failed")
                        st.session_state['mandatory_location'] = None
                else:
                    st.error("❌ Failed to connect to location service")
                    st.session_state['mandatory_location'] = None
            except Exception as e:
                st.error(f"❌ Location detection error: {str(e)}")
                st.session_state['mandatory_location'] = None
    
    # Show current location or require manual input
    if st.session_state.get('mandatory_location'):
        location = st.session_state['mandatory_location']
        
        # Display current location
        st.info(f"📍 **Auto-detected Location**: {location['city']}, {location['region']}, {location['country']}")
        st.write(f"🌐 **Coordinates**: {location['latitude']:.4f}, {location['longitude']:.4f}")
        
        # Option to refresh or override
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh Location"):
                del st.session_state['mandatory_location']
                st.rerun()
        
        with col2:
            override = st.checkbox("✏️ Override location")
        
        if override:
            st.write("**Manual Location Override:**")
            new_city = st.text_input("City:", value=location['city'])
            new_country = st.text_input("Country:", value=location['country']) 
            new_coords = st.text_input("Coordinates (lat, lng):", 
                                     value=f"{location['latitude']}, {location['longitude']}")
            
            if st.button("Update Location") and new_city and new_country and new_coords:
                try:
                    coord_parts = new_coords.split(',')
                    if len(coord_parts) == 2:
                        lat = float(coord_parts[0].strip())
                        lon = float(coord_parts[1].strip())
                        if -90 <= lat <= 90 and -180 <= lon <= 180:
                            st.session_state['mandatory_location'] = {
                                "city": new_city,
                                "region": location['region'],
                                "country": new_country,
                                "latitude": lat,
                                "longitude": lon,
                                "detection_method": "manual_override",
                                "timestamp": datetime.datetime.now().isoformat()
                            }
                            st.success("✅ Location updated!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid coordinate range")
                    else:
                        st.error("❌ Invalid coordinate format")
                except ValueError:
                    st.error("❌ Invalid coordinates. Use format: latitude, longitude")
        
        return st.session_state['mandatory_location']
    
    else:
        # Location detection failed - require manual input
        st.error("❌ **Automatic location detection failed. Manual input required:**")
        st.warning("⚠️ **Location is mandatory for all data uploads**")
        
        manual_city = st.text_input("🏙️ City (Required):", placeholder="Enter your city")
        manual_region = st.text_input("🗺️ Region/State:", placeholder="Enter your region/state")
        manual_country = st.text_input("🌍 Country (Required):", placeholder="Enter your country")
        manual_coords = st.text_input("📍 Coordinates (Required):", 
                                    placeholder="latitude, longitude (e.g., 40.7128, -74.0060)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌐 Try Auto-Detect Again"):
                if 'mandatory_location' in st.session_state:
                    del st.session_state['mandatory_location']
                st.rerun()
        
        with col2:
            help_link = st.button("❓ Get My Coordinates", help="Opens a new tab to help find your coordinates")
            if help_link:
                st.write("🔗 Visit: https://www.latlong.net/convert-address-to-lat-long.html")
        
        # Validate manual input
        if manual_city and manual_country and manual_coords:
            try:
                coord_parts = manual_coords.split(',')
                if len(coord_parts) == 2:
                    lat = float(coord_parts[0].strip())
                    lon = float(coord_parts[1].strip())
                    if -90 <= lat <= 90 and -180 <= lon <= 180:
                        location_data = {
                            "city": manual_city,
                            "region": manual_region or "Unknown",
                            "country": manual_country,
                            "latitude": lat,
                            "longitude": lon,
                            "detection_method": "manual_required",
                            "timestamp": datetime.datetime.now().isoformat()
                        }
                        st.success("✅ Manual location data validated!")
                        st.session_state['mandatory_location'] = location_data
                        st.rerun()
                    else:
                        st.error("❌ Coordinates must be between -90 to 90 (latitude) and -180 to 180 (longitude)")
                else:
                    st.error("❌ Invalid format. Use: latitude, longitude")
            except ValueError:
                st.error("❌ Invalid number format. Use: latitude, longitude")
        
        return None  # No valid location yet
