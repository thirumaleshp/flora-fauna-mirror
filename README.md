
# Flora and Fauna

## [flora-fauna.streamlit.app](https://flora-fauna.streamlit.app/)



```
cd existing_repo
git remote add origin https://code.swecha.org/DAYAKAR123/flora.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://code.swecha.org/DAYAKAR123/flora/-/settings/integrations)


# 🌿 Flora and Fauna Data Collection App

A comprehensive Streamlit application for documenting and preserving biodiversity through multi-media data collection. Capture flora and fauna observations with text descriptions, audio recordings, video documentation, and photographs - all with automatic location tracking for scientific research and conservation efforts.

## Features

### 📍 Location Tracking
- Manual location entry
- Coordinate input (latitude, longitude)
- Country and city specification
- Location statistics and analytics
- Location data validation

### 📝 Text Data Collection
- Single text entry with categories
- Multi-line text input for longer content
- CSV file upload for bulk data import
- Automatic timestamping and categorization
- Location capture for each entry

### 🎵 Audio Data Collection
- Upload audio files (MP3, WAV, OGG, M4A)
- Audio preview functionality
- Metadata collection (duration, category, description)
- Support for various audio categories
- Location information for each recording

### 🎥 Video Data Collection
- Upload video files (MP4, AVI, MOV, WMV)
- Video preview functionality
- Detailed metadata (duration, resolution, tags)
- Category-based organization
- Location tracking for video content

### 🖼️ Image Data Collection
- Multiple image upload support
- Image preview gallery
- Tagging and categorization system
- Support for various image formats (PNG, JPG, JPEG, GIF, BMP)
- Location data for image capture

### 📈 Data Management
- View all collected data in a unified dashboard
- Filter data by type
- Export data to CSV
- Summary statistics
- Metadata tracking with timestamps
- Location-based analytics and statistics

## Installation

1. Clone or download the project files
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Use the sidebar to select the type of data you want to collect:
   - **📝 Text Data**: Enter text manually or upload CSV files
   - **🎵 Audio Data**: Upload audio recordings
   - **🎥 Video Data**: Upload video files
   - **🖼️ Image Data**: Upload single or multiple images
   - **📈 View Collected Data**: Review and export collected data

4. For each data type, provide location information:
   - Enter location manually (e.g., "New York, NY")
   - Input coordinates (latitude, longitude)
   - Specify country and city
   - View location statistics in the data overview

## Data Storage

All collected data is stored locally in the `data/` directory:
- `data/text/` - Text files and CSV uploads
- `data/audio/` - Audio recordings
- `data/video/` - Video files
- `data/images/` - Image files
- `data/metadata.json` - Metadata for all collected files

## File Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── location_utils.py     # Location processing utilities
├── data_utils.py         # Data processing utilities
├── analytics.py          # Analytics dashboard
├── config.py             # Configuration settings
└── data/                 # Data storage directory (created automatically)
    ├── text/
    ├── audio/
    ├── video/
    ├── images/
    └── metadata.json
```

## Features in Detail

### Metadata Tracking
Each uploaded file includes comprehensive metadata:
- Timestamp of upload
- Data type and category
- Original filename
- Location information (manual entry, coordinates, country/city)
- Additional attributes (duration, resolution, tags, etc.)
- Custom descriptions and notes

### Location Features
- **Manual Entry**: Type your current location
- **Coordinates**: Enter GPS coordinates
- **Country/City**: Specify geographic details
- **Statistics**: View location-based analytics
- **Validation**: Coordinate format checking
- **Export**: Location data included in CSV exports

### User Interface
- Clean, intuitive interface with clear navigation
- Responsive design that works on different screen sizes
- Real-time preview of uploaded content
- Progress indicators and success messages
- Organized layout with helpful instructions

### Data Export
- Export metadata to CSV format
- Filter data before export
- Download collected data summaries
- Comprehensive data overview dashboard

## Customization

You can easily customize the application by:
- Adding new data categories in the selectbox options
- Modifying the metadata fields collected
- Changing the file storage structure
- Adding new data types or input methods

## Requirements

- Python 3.7+
- Streamlit 1.28.1+
- Pandas 2.1.1+
- Matplotlib 3.7.1+
- Requests 2.31.0+
- Standard Python libraries (os, datetime, pathlib, json)







