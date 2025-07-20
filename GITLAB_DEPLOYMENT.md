# GitLab Deployment Guide for Flora & Fauna Data Collection App

## 🦊 GitLab-Specific Deployment Options

### 1. GitLab Container Registry + Docker

**Automatic Docker Build:**
- Push to `main` branch triggers automatic Docker image build
- Images stored in GitLab Container Registry
- Access at: `registry.gitlab.com/yourusername/flora-fauna-data-collection`

**Manual Docker Deployment:**
```bash
# Pull the built image
docker pull registry.gitlab.com/yourusername/flora-fauna-data-collection:latest

# Run the container
docker run -p 8501:8501 registry.gitlab.com/yourusername/flora-fauna-data-collection:latest
```

### 2. GitLab Pages (Documentation)

**Automatic Deployment:**
- Deployment guide automatically published to GitLab Pages
- Available at: `https://yourusername.gitlab.io/flora-fauna-data-collection`

### 3. GitLab CI/CD Variables Setup

**Required Variables (Settings > CI/CD > Variables):**

For Heroku deployment:
- `HEROKU_API_KEY`: Your Heroku API key
- `HEROKU_APP_NAME`: Your Heroku app name

For Railway deployment:
- `RAILWAY_TOKEN`: Your Railway CLI token
- `RAILWAY_DOMAIN`: Your Railway app domain

### 4. Streamlit Community Cloud with GitLab

**Steps:**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect GitLab account
3. Select your repository
4. Set main file: `app.py`
5. Deploy!

### 5. Manual Deployment Jobs

The CI/CD pipeline includes manual deployment jobs:
- **Heroku**: Manual job in GitLab CI/CD
- **Railway**: Manual job in GitLab CI/CD

## 🔧 GitLab Repository Setup

### Initial Repository Setup:
```bash
# Initialize git repository
git init
git remote add origin https://gitlab.com/yourusername/flora-fauna-data-collection.git

# Add all files
git add .
git commit -m "Initial commit: Flora & Fauna Data Collection App"

# Push to GitLab
git push -u origin main
```

### Branch Protection:
- Enable merge request approvals
- Require CI/CD pipeline to pass
- Enable automatic merge when pipeline succeeds

## 📋 CI/CD Pipeline Features

### Automatic Testing:
- ✅ Python syntax validation
- ✅ Dependency checks
- ✅ Import verification
- ✅ File structure validation

### Automatic Building:
- 🐳 Docker image creation
- 📦 Container registry storage
- 🏷️ Version tagging

### Deployment Options:
- 📄 GitLab Pages (documentation)
- 🚀 Manual Heroku deployment
- 🚂 Manual Railway deployment
- 📊 Deployment information artifacts

## 🌐 Production Deployment URLs

After setup, your app will be available at:
- **Docker**: `http://localhost:8501` (local)
- **Heroku**: `https://your-app-name.herokuapp.com`
- **Railway**: `https://your-domain.railway.app`
- **Streamlit Cloud**: `https://share.streamlit.io/yourusername/flora-fauna-data-collection`

## 🔐 Security Configuration

### GitLab Security Features:
- Container scanning enabled
- Dependency scanning for Python packages
- Secret detection in commits
- SAST (Static Application Security Testing)

### Environment Variables:
All sensitive data stored as GitLab CI/CD variables, not in code.

## 📊 Monitoring & Analytics

### GitLab Built-in Features:
- Pipeline success/failure tracking
- Deployment frequency metrics
- Container registry usage
- Pages views analytics

## 🆘 Troubleshooting

### Common Issues:

**1. Pipeline Fails:**
- Check GitLab CI/CD logs
- Verify Python version compatibility
- Ensure all dependencies in requirements.txt

**2. Docker Build Fails:**
- Check Dockerfile syntax
- Verify base image availability
- Review resource limits

**3. Deployment Fails:**
- Verify environment variables
- Check target platform requirements
- Review deployment logs

### Getting Help:
- GitLab Issues: Use repository issue tracker
- GitLab Documentation: [docs.gitlab.com](https://docs.gitlab.com)
- Community: GitLab Community Forum
