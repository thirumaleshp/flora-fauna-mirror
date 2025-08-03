
# 🌿 Flora & Fauna Chatbot

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red.svg)](https://streamlit.io/)
[![GitLab](https://img.shields.io/badge/GitLab-Repository-orange.svg)](https://code.swecha.org/DAYAKAR123/flora)

> A bilingual (English/Telugu) AI-powered chatbot for flora and fauna data collection, query, and biodiversity information sharing.

**🌐 Live Demo:** [flora-fauna.streamlit.app](https://flora-fauna.streamlit.app/)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [Project Structure](#project-structure)
- [Development](#development)
- [Deployment](#deployment)
- [License](#license)
- [Support](#support)

## 🌟 Overview

The Flora & Fauna Chatbot is an innovative bilingual application designed to bridge the gap between traditional botanical and zoological knowledge and modern digital accessibility. Built with Streamlit and powered by Supabase, this chatbot enables users to:

- **Query biodiversity data** in both English and Telugu
- **Contribute species information** with multimedia support
- **Explore local flora and fauna** with location-based search
- **Access cultural knowledge** about traditional uses and significance
- **Preserve biodiversity data** for research and education

## ✨ Features

### 🗣️ Bilingual Support
- **English & Telugu Interface**: Native language support for wider accessibility
- **Smart Query Processing**: Understands mixed-language queries
- **Cultural Context**: Local names and traditional knowledge integration

### 📊 Data Management
- **Species Database**: Comprehensive flora and fauna information
- **Media Support**: Images, videos, and audio recordings
- **Location Tracking**: GPS coordinates and habitat descriptions
- **Data Validation**: Quality assurance and expert verification

### 🎯 User Experience
- **Interactive Chat Interface**: Natural conversation flow
- **Visual Media Display**: Rich multimedia content presentation
- **Search & Filter**: Advanced query capabilities
- **Mobile Responsive**: Works on all devices

### 🔬 Research Features
- **Data Export**: CSV and JSON format support
- **Analytics Dashboard**: Usage and contribution statistics
- **API Access**: Programmatic data access
- **Collaboration Tools**: Multi-user contribution system

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Modern web browser

### 1-Minute Setup

```bash
# Clone the repository
git clone https://code.swecha.org/DAYAKAR123/flora.git
cd flora

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

🎉 **That's it!** Open your browser to `http://localhost:8501` and start exploring!

## 📦 Installation

### Method 1: Using Poetry (Recommended)

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Clone and setup
git clone https://code.swecha.org/DAYAKAR123/flora.git
cd flora
poetry install
poetry run streamlit run app.py
```

### Method 2: Using pip

```bash
git clone https://code.swecha.org/DAYAKAR123/flora.git
cd flora
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Method 3: Using Docker

```bash
docker-compose up --build
```

## ⚙️ Configuration

### Database Setup

1. **Create Supabase Account**: Visit [supabase.com](https://supabase.com/) and create a new project

2. **Database Schema**: Import the schema from `COMPLETE_SETUP.sql`

3. **Environment Variables**: Copy and configure secrets
   ```bash
   cp secrets.template.toml .streamlit/secrets.toml
   # Edit .streamlit/secrets.toml with your credentials
   ```

### Detailed Setup Guides
- 📖 [Complete Setup Guide](CREATE_OWN_SUPABASE.md)
- ☁️ [Cloud Database Setup](CLOUD_DATABASE_SETUP.md)
- 🚀 [Deployment Guide](DEPLOYMENT.md)

## 💡 Usage

### Basic Queries

```
🔍 User: "Show me plants native to Telangana"
🤖 Bot: [Displays native plant species with images and descriptions]

🔍 User: "తెలంగాణలో పండే పువ్వులు చూపించు" (Show flowers that bloom in Telangana)
🤖 Bot: [Shows flowering plants with Telugu names and details]
```

### Data Contribution

1. **Navigate to Data Collection** section in the app
2. **Fill species information** form
3. **Upload media files** (images, videos, audio)
4. **Add location details** and habitat information
5. **Submit** for review and validation

### Advanced Features

- **Keyword Search**: Use specific terms like "medicinal plants", "endangered species"
- **Location Filtering**: Search by state, district, or GPS coordinates
- **Media Filtering**: Find species with images, videos, or audio recordings
- **Seasonal Information**: Query by flowering seasons or migration patterns

## 🤝 Contributing

We welcome contributions from researchers, students, botanists, zoologists, and nature enthusiasts!

### Priority Contributions
1. **🌱 Species Data**: Flora and fauna information (HIGHEST PRIORITY)
2. **📸 Media Content**: Images, videos, audio recordings
3. **🌍 Location Data**: GPS coordinates and habitat descriptions
4. **💻 Code Improvements**: Bug fixes and new features

### Quick Contribute
- **Data**: Use the web interface to add species information
- **Code**: Check [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- **Issues**: Report bugs or suggest features in GitLab Issues
- **Documentation**: Help improve guides and tutorials

**📋 [Read Full Contributing Guide](CONTRIBUTING.md)**

## 📁 Project Structure

```
flora-fauna-chatbot/
├── app.py                  # Main Streamlit application
├── chatbot.py             # Core chatbot logic
├── supabase_db.py         # Database operations
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Poetry configuration
├── .streamlit/            # Streamlit configuration
│   ├── config.toml        # App configuration
│   └── secrets.toml       # Database credentials (not in git)
├── .vscode/               # VS Code settings
├── .gitlab/               # GitLab templates
├── data/                  # Sample data and exports
├── tests/                 # Test files
├── docs/                  # Documentation
└── README.md              # This file
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone and setup
git clone https://code.swecha.org/DAYAKAR123/flora.git
cd flora

# Install with development dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest tests/

# Code formatting
poetry run black .
poetry run isort .
```

### Development Tools

- **Testing**: `pytest` with coverage reporting
- **Formatting**: `black` for code formatting
- **Linting**: `flake8` for code quality
- **Type Checking**: `mypy` for type hints
- **Pre-commit**: Automated code quality checks

### VS Code Setup

The project includes VS Code configuration with:
- Python extension recommendations
- Debugging configurations
- Task definitions
- Settings for formatting and linting

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Fork the repository on GitLab
2. Connect your GitLab account to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy directly from your fork
4. Configure secrets in the Streamlit Cloud dashboard

### Other Deployment Options

- **Heroku**: Use `Procfile` and `requirements.txt`
- **Docker**: Use `docker-compose.yml`
- **DigitalOcean**: App Platform deployment
- **AWS/GCP**: Container or serverless deployment

**📖 [Detailed Deployment Guide](DEPLOYMENT.md)**

## 📊 Statistics

- **🌿 Species Count**: 500+ flora species documented
- **🦋 Fauna Records**: 300+ animal species cataloged
- **📸 Media Files**: 1000+ images and videos
- **🌍 Locations**: Coverage across 5+ Indian states
- **👥 Contributors**: 15+ active data contributors

## 🤖 Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.8+ with pandas for data processing
- **Database**: Supabase (PostgreSQL) with real-time capabilities
- **Storage**: Supabase Storage for media files
- **Deployment**: Streamlit Cloud, Docker support
- **Development**: Poetry, pytest, black, VS Code integration

## 📜 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

**Key points:**
- ✅ Free to use, modify, and distribute
- ✅ Commercial use allowed
- ✅ Open source community development
- ⚠️ Must share modifications if deployed publicly
- ⚠️ Network use requires source availability

See [LICENSE/LICENSE.md](LICENSE/LICENSE.md) for full license text.

## 🆘 Support

### Getting Help

- **📖 Documentation**: Check our comprehensive guides
- **🐛 Issues**: Report bugs on [GitLab Issues](https://code.swecha.org/DAYAKAR123/flora/-/issues)
- **💬 Discussions**: Join community discussions
- **📧 Email**: Contact maintainers directly

### Maintainers

- **Thirumalesh Pinninti** - Project Lead & Development
- **DAYAKAR123** - Repository Owner & Data Curation

### Quick Links

- 🌐 [Live Application](https://flora-fauna.streamlit.app/)
- 📚 [Documentation](docs/)
- 🐛 [Report Issues](https://code.swecha.org/DAYAKAR123/flora/-/issues)
- 🤝 [Contributing Guide](CONTRIBUTING.md)
- 📝 [Changelog](CHANGELOG.md)

---

## 🌟 Acknowledgments

This project is built with contributions from botanists, zoologists, researchers, and nature enthusiasts. Special thanks to:

- **Swecha Community** for hosting and supporting open-source development
- **Local Researchers** who provided species data and expertise
- **Contributors** who added media content and location information
- **Streamlit Team** for the amazing web framework
- **Supabase Team** for the powerful backend infrastructure

---

**Made with ❤️ for biodiversity conservation and education**

*Help us preserve and share the rich flora and fauna knowledge of India! 🇮🇳*
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







