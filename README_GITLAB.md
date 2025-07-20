# 🌱 Flora & Fauna Data Collection Application

[![GitLab CI/CD](https://gitlab.com/yourusername/flora-fauna/badges/main/pipeline.svg)](https://gitlab.com/yourusername/flora-fauna/-/pipelines)
[![Docker Image](https://img.shields.io/badge/docker-registry.gitlab.com-blue)](https://gitlab.com/yourusername/flora-fauna/container_registry)

A comprehensive Streamlit application for collecting various types of data including text, audio, video, and images with automatic location tracking for research and internship projects.

## 🚀 Quick Deploy with GitLab

### Option 1: Streamlit Community Cloud (Recommended)
1. Push to GitLab: `./gitlab-deploy.sh` → Option 1
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitLab and deploy!

### Option 2: GitLab Container Registry
```bash
# Automatic build on push to main
git push origin main

# Use the built image
docker pull registry.gitlab.com/yourusername/flora-fauna:latest
docker run -p 8501:8501 registry.gitlab.com/yourusername/flora-fauna:latest
```

### Option 3: GitLab Pages (Documentation)
- Deployment guide automatically published at: `https://yourusername.gitlab.io/flora-fauna`

## ✨ Features

### 📍 **Automatic Location Tracking**
- **GPS Detection**: Precise location from device GPS
- **IP Geolocation**: Fallback location from IP address
- **Manual Entry**: Custom location input option
- **Address Lookup**: Automatic address resolution

### 📊 **Multi-Media Data Collection**
- **📝 Text**: Single entry, multi-line, CSV upload
- **🎵 Audio**: MP3, WAV, OGG, M4A support with metadata
- **🎥 Video**: MP4, AVI, MOV, WMV with tags and descriptions
- **🖼️ Images**: PNG, JPG, JPEG, GIF, BMP with batch upload

### 📈 **Analytics & Export**
- Real-time data visualization
- Location-based statistics
- CSV export with metadata
- Data filtering and search

### 📱 **Mobile-First Design**
- Responsive interface for all devices
- Touch-friendly controls
- Mobile camera integration
- Offline-ready data collection

## 🛠️ Development

### Local Setup
```bash
# Clone repository
git clone https://gitlab.com/yourusername/flora-fauna.git
cd flora-fauna

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

### GitLab CI/CD
The project includes automatic:
- ✅ Testing and validation
- 🐳 Docker image building
- 📄 Documentation deployment
- 🚀 Manual deployment jobs

## 📦 Deployment Options

| Platform | Method | URL Pattern | Notes |
|----------|--------|-------------|--------|
| **Streamlit Cloud** | GitLab Integration | `share.streamlit.io/user/repo` | Recommended |
| **GitLab Container Registry** | Auto Docker Build | `registry.gitlab.com/user/repo` | Enterprise ready |
| **GitLab Pages** | Auto Deployment | `user.gitlab.io/repo` | Documentation |
| **Heroku** | Manual CI/CD Job | `app-name.herokuapp.com` | Scalable |
| **Railway** | GitLab Connection | `app.railway.app` | Modern platform |

## 🔧 Configuration

### Environment Variables (GitLab CI/CD)
Set in **Settings > CI/CD > Variables**:
- `HEROKU_API_KEY`: For Heroku deployment
- `HEROKU_APP_NAME`: Your Heroku app name
- `RAILWAY_TOKEN`: For Railway deployment

### File Structure
```
flora-fauna/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .gitlab-ci.yml        # GitLab CI/CD pipeline
├── Dockerfile            # Container configuration
├── .streamlit/           # Streamlit configuration
├── data/                 # Data storage (auto-created)
└── .gitlab/              # GitLab templates
    ├── issue_templates/
    └── merge_request_templates/
```

## 📋 Usage

1. **Select Data Type**: Choose from text, audio, video, or images
2. **Capture Location**: Use automatic detection or manual entry
3. **Upload Content**: Add your data with metadata
4. **Review & Export**: View collected data and export as needed

### Location Detection
- **Desktop**: Browser-based geolocation
- **Mobile**: Native GPS integration
- **Fallback**: IP-based location detection
- **Manual**: Custom location entry

## 🔒 Privacy & Security

- **Local Storage**: All data stored locally by default
- **No Tracking**: Location data processed client-side
- **Secure Upload**: File validation and size limits
- **Privacy First**: No data sent to external services without consent

## 🤝 Contributing

1. Fork the repository on GitLab
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Merge Request

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Test on multiple devices and browsers
- Ensure mobile compatibility
- Include tests for new features
- Update documentation

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- **Issues**: [GitLab Issues](https://gitlab.com/yourusername/flora-fauna/-/issues)
- **Documentation**: [GitLab Pages](https://yourusername.gitlab.io/flora-fauna)
- **CI/CD**: [Pipeline Status](https://gitlab.com/yourusername/flora-fauna/-/pipelines)

## 🏆 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Location services powered by browser geolocation API
- Container registry hosted on GitLab
- Deployed with GitLab CI/CD

---

**Ready to deploy?** Run `./gitlab-deploy.sh` to get started! 🚀
