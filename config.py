# Configuration file for the Data Collection App

# Application settings
APP_TITLE = "Multi-Media Data Collection Application"
APP_ICON = "📊"

# Data storage settings
DATA_DIR = "data"
SUBDIRS = {
    "text": "data/text",
    "audio": "data/audio", 
    "video": "data/video",
    "images": "data/images"
}

# File upload settings
MAX_FILE_SIZE = 200  # MB

# Supported file types
SUPPORTED_FORMATS = {
    "text": ["txt", "csv"],
    "audio": ["mp3", "wav", "ogg", "m4a"],
    "video": ["mp4", "avi", "mov", "wmv"],
    "images": ["png", "jpg", "jpeg", "gif", "bmp"]
}

# Categories
CATEGORIES = {
    "text": ["General", "Research", "Survey", "Feedback", "Other"],
    "audio": ["Speech", "Music", "Nature Sounds", "Interview", "Other"],
    "video": ["Educational", "Documentation", "Interview", "Presentation", "Other"],
    "images": ["Photos", "Screenshots", "Diagrams", "Charts", "Other"]
}
