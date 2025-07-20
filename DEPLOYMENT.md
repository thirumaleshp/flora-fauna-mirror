# Deployment Guide for Flora & Fauna Data Collection App

## 🚀 Deployment Options

### 1. Streamlit Community Cloud (Recommended - Free)

**Steps:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository
5. Set main file path: `app.py`
6. Deploy!

**Preparation:**
```bash
# Create GitHub repository
git init
git add .
git commit -m "Initial commit: Flora & Fauna Data Collection App"
git branch -M main
git remote add origin https://github.com/yourusername/flora-fauna-data-collection.git
git push -u origin main
```

### 2. Heroku (Free Tier Available)

**Required Files Created:**
- `Procfile`
- `setup.sh`
- `runtime.txt` (optional)

**Steps:**
1. Install Heroku CLI
2. Create Heroku app: `heroku create your-app-name`
3. Push to Heroku: `git push heroku main`

### 3. Railway (Modern Alternative)

**Steps:**
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Deploy automatically

### 4. Render (Free Static Sites)

**Steps:**
1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run app.py --server.port $PORT`

### 5. Local Network Deployment

**Run on local network:**
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## 📝 Pre-Deployment Checklist

- [x] requirements.txt is complete
- [x] .streamlit/config.toml configured
- [x] Environment variables set (if any)
- [x] File upload limits configured
- [x] HTTPS considerations for geolocation
- [x] Static files properly referenced

## 🔧 Environment Variables (if needed)

For production deployment, consider these environment variables:
- `STREAMLIT_SERVER_PORT`: Port number
- `STREAMLIT_SERVER_ADDRESS`: Server address
- `MAX_UPLOAD_SIZE`: File upload limit

## 🌐 Domain & SSL

For custom domains:
- Use your hosting provider's domain settings
- Enable HTTPS for geolocation features
- Configure DNS properly

## 📱 Mobile Considerations

- Responsive design already implemented
- Touch-friendly interface
- Geolocation works on mobile browsers
- File upload optimized for mobile

## 🔐 Security Notes

- Location data processed client-side
- No sensitive data stored permanently
- File uploads validated
- CORS properly configured

## 📊 Monitoring & Analytics

Consider adding:
- Usage analytics
- Error tracking
- Performance monitoring
- User feedback system
