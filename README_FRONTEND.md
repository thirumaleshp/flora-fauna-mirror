# 🌿 Flora & Fauna Frontend Homepage

A modern, responsive frontend homepage for the Flora & Fauna Data Collection project. Built with HTML, Tailwind CSS, and modern JavaScript with Supabase integration.

## ✨ Features

### 🎨 Modern Design
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Tailwind CSS**: Modern utility-first CSS framework for beautiful styling
- **Clean UI/UX**: Intuitive navigation and user-friendly interface
- **Smooth Animations**: Fade-in effects, hover animations, and smooth scrolling
- **Dark/Light Elements**: Professional color scheme with nature-inspired themes

### 🌐 Hero Section
- Eye-catching gradient background with call-to-action buttons
- Real-time statistics display (total records, species count, locations)
- Animated counters that count up when the page loads
- Direct integration buttons to explore data and access Streamlit app

### 📊 Dynamic Data Display
- **Real-time Data**: Fetches and displays data from Supabase database
- **Multiple Media Types**: Supports images, videos, audio files, and text entries
- **Smart Filtering**: Filter by entry type (all, images, text, audio, video)
- **Search Functionality**: Search across titles, content, and locations
- **Responsive Grid**: Adaptive grid layout that works on all screen sizes

### 🔌 Supabase Integration
- **Modern JavaScript**: Uses async/await and ES6+ features
- **Automatic Connection**: Attempts to connect using saved credentials
- **Configuration Modal**: Easy setup interface for Supabase credentials
- **Error Handling**: Graceful error handling with user-friendly messages
- **Real-time Status**: Connection status indicator in the navigation

### 📱 Mobile-First Design
- Responsive navigation with mobile hamburger menu
- Touch-friendly buttons and interactions
- Optimized for all screen sizes
- Fast loading and smooth performance

## 🚀 Quick Start

### 1. File Structure
```
frontend/
├── index.html          # Main homepage
├── app.js             # JavaScript application logic
├── config.js          # Configuration file
└── README_FRONTEND.md # This file
```

### 2. Setup Instructions

#### Option A: Simple Setup (Recommended)
1. Open `index.html` in your web browser
2. When prompted, enter your Supabase credentials:
   - **Supabase URL**: `https://your-project-ref.supabase.co`
   - **Anon Key**: Your project's anon/public key
3. Click "Connect" and start exploring your data!

#### Option B: Configuration File Setup
1. Edit `config.js` and update the `SUPABASE_CONFIG` object:
```javascript
const SUPABASE_CONFIG = {
    url: 'https://your-actual-project.supabase.co',
    anonKey: 'your-actual-anon-key-here',
    tableName: 'data_entries'
};
```
2. Open `index.html` in your browser

### 3. Supabase Requirements

Your Supabase project needs:

#### Database Table
```sql
CREATE TABLE data_entries (
    id BIGSERIAL PRIMARY KEY,
    entry_type TEXT NOT NULL,
    title TEXT,
    content TEXT,
    file_path TEXT,
    file_url TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    location_lat NUMERIC,
    location_lng NUMERIC,
    location_name TEXT,
    metadata JSONB
);
```

#### Storage Buckets
Create these storage buckets in your Supabase project:
- `images` (for image files)
- `videos` (for video files)
- `audios` (for audio files)
- `texts` (for text files)

#### RLS Policies (Optional)
If using Row Level Security, ensure your policies allow:
- `SELECT` operations for anonymous users
- Appropriate access for your use case

## 🔧 Streamlit Integration

This frontend is designed to work seamlessly with the existing Streamlit backend:

### Shared Configuration
Ensure your `.streamlit/secrets.toml` has the same credentials:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
```

### Data Compatibility
The frontend automatically displays data created through:
- The Streamlit app's text data collection
- Image uploads via Streamlit
- Audio and video data collection
- Location-tagged entries

### Navigation Integration
The "Open Streamlit App" button can be configured to:
- Open the Streamlit app in a new tab
- Redirect to your deployed Streamlit application
- Launch a local Streamlit instance

## 🎯 Usage Guide

### For End Users
1. **Browse Data**: Use the filter buttons to explore different types of flora and fauna data
2. **Search**: Use the search bar to find specific entries by name, content, or location
3. **View Details**: Click "Details" on any card to see full information
4. **Access Files**: Click "View" to open the original uploaded files
5. **Navigate**: Use the smooth-scrolling navigation to explore different sections

### For Developers
1. **Customize Styling**: Modify Tailwind classes in `index.html`
2. **Add Features**: Extend the `FloraFaunaApp` class in `app.js`
3. **Configure Integration**: Update connection settings in `config.js`
4. **Deploy**: Host the files on any static web server

## 🛠 Technical Details

### JavaScript Features
- **ES6+ Syntax**: Modern JavaScript with classes, async/await, and arrow functions
- **Modular Design**: Clean, organized code structure
- **Error Handling**: Comprehensive error handling with user feedback
- **Local Storage**: Automatic credential saving for convenience
- **Performance Optimized**: Efficient data loading and rendering

### CSS Framework
- **Tailwind CSS**: Utility-first CSS framework
- **Custom Animations**: Smooth transitions and hover effects
- **Responsive Grid**: Adaptive layouts for all screen sizes
- **Component Styling**: Reusable component patterns

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Progressive enhancement for older browsers

## 🌍 Deployment Options

### Static Hosting
Deploy to any static hosting service:
- **Netlify**: Drag and drop the files
- **Vercel**: Connect your GitHub repository
- **GitHub Pages**: Host directly from your repository
- **Local Server**: Use `python -m http.server` or similar

### CDN Integration
All external dependencies are loaded via CDN:
- Tailwind CSS
- Supabase JavaScript Client
- Font Awesome icons
- Google Fonts

### Custom Domain
Point your custom domain to the hosting service for a professional URL.

## 🔒 Security Considerations

### Credentials
- Anon keys are safe to expose in frontend code
- Service keys should never be used in frontend applications
- Consider implementing Row Level Security for sensitive data

### Data Protection
- All communication with Supabase is encrypted (HTTPS)
- Client-side validation prevents malformed requests
- Error messages don't expose sensitive information

## 🤝 Contributing

### Adding Features
1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

### Reporting Issues
- Use the GitHub issue tracker
- Provide detailed reproduction steps
- Include browser and device information

## 📄 License

This project is part of the Flora & Fauna Data Collection system. Please refer to the main project license.

## 🔗 Related Files

- **Backend**: `app.py` (Streamlit application)
- **Database**: `supabase_db.py` (Database integration)
- **Configuration**: `.streamlit/secrets.toml` (Shared credentials)

---

**Built with ❤️ for nature conservation and biodiversity preservation**