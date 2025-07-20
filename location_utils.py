"""
Location utilities for the data collection app
"""

import requests

def get_location_from_ip():
    """Get approximate location from IP address"""
    try:
        # Using a free IP geolocation service
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get("city"),
                "region": data.get("regionName"),
                "country": data.get("country"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "timezone": data.get("timezone"),
                "source": "ip_geolocation"
            }
    except Exception as e:
        print(f"IP geolocation failed: {e}")
    
    return None

def reverse_geocode(latitude, longitude):
    """Get address from coordinates using free service"""
    try:
        url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={latitude}&longitude={longitude}&localityLanguage=en"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get("city"),
                "region": data.get("principalSubdivision"),
                "country": data.get("countryName"),
                "formatted_address": f"{data.get('city', '')}, {data.get('principalSubdivision', '')}, {data.get('countryName', '')}".strip(', '),
                "source": "reverse_geocoding"
            }
    except Exception as e:
        print(f"Reverse geocoding failed: {e}")
    
    return None

def validate_coordinates(lat_str, lon_str):
    """Validate and parse coordinate strings"""
    try:
        lat = float(lat_str)
        lon = float(lon_str)
        
        # Check if coordinates are within valid ranges
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return {"latitude": lat, "longitude": lon, "valid": True}
        else:
            return {"valid": False, "error": "Coordinates out of valid range"}
    except ValueError:
        return {"valid": False, "error": "Invalid coordinate format"}

def format_location_display(location_data):
    """Format location data for display"""
    if not location_data or location_data.get('status') == 'not_provided':
        return "Location not provided"
    
    parts = []
    
    if location_data.get('manual_location'):
        parts.append(f"📍 {location_data['manual_location']}")
    
    if location_data.get('city') and location_data.get('country'):
        parts.append(f"🏙️ {location_data['city']}, {location_data['country']}")
    elif location_data.get('city'):
        parts.append(f"🏙️ {location_data['city']}")
    elif location_data.get('country'):
        parts.append(f"🏳️ {location_data['country']}")
    
    if location_data.get('coordinates'):
        coords = location_data['coordinates']
        parts.append(f"🗺️ ({coords.get('latitude', 'N/A')}, {coords.get('longitude', 'N/A')})")
    
    return " | ".join(parts) if parts else "Location data incomplete"

def get_location_statistics(metadata_list):
    """Generate location statistics from metadata"""
    stats = {
        "total_entries": len(metadata_list),
        "entries_with_location": 0,
        "countries": {},
        "cities": {},
        "coordinate_entries": 0
    }
    
    for entry in metadata_list:
        location = entry.get('location', {})
        
        if location and location.get('status') != 'not_provided':
            stats["entries_with_location"] += 1
            
            if location.get('country'):
                country = location['country']
                stats["countries"][country] = stats["countries"].get(country, 0) + 1
            
            if location.get('city'):
                city = location['city']
                stats["cities"][city] = stats["cities"].get(city, 0) + 1
            
            if location.get('coordinates'):
                stats["coordinate_entries"] += 1
    
    # Calculate percentages
    if stats["total_entries"] > 0:
        stats["location_coverage_percent"] = (stats["entries_with_location"] / stats["total_entries"]) * 100
        stats["coordinate_coverage_percent"] = (stats["coordinate_entries"] / stats["total_entries"]) * 100
    else:
        stats["location_coverage_percent"] = 0
        stats["coordinate_coverage_percent"] = 0
    
    return stats

# Example usage and testing
if __name__ == "__main__":
    # Test IP geolocation
    print("Testing IP geolocation...")
    ip_location = get_location_from_ip()
    if ip_location:
        print(f"IP Location: {ip_location}")
    
    # Test coordinate validation
    print("\nTesting coordinate validation...")
    valid_coords = validate_coordinates("40.7128", "-74.0060")
    print(f"Valid coordinates: {valid_coords}")
    
    invalid_coords = validate_coordinates("invalid", "coords")
    print(f"Invalid coordinates: {invalid_coords}")
    
    # Test reverse geocoding (if valid coordinates)
    if valid_coords.get("valid"):
        print("\nTesting reverse geocoding...")
        address = reverse_geocode(valid_coords["latitude"], valid_coords["longitude"])
        if address:
            print(f"Reverse geocoded address: {address}")
