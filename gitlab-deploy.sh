#!/bin/bash

# GitLab Deployment Helper Script
echo "🦊 GitLab Deployment Helper for Flora & Fauna Data Collection App"
echo "================================================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a Git repository. Initializing..."
    git init
    echo "✅ Git repository initialized"
fi

# Check if GitLab remote exists
if ! git remote get-url origin &> /dev/null; then
    echo ""
    echo "🔗 GitLab Remote Setup"
    echo "====================="
    read -p "Enter your GitLab repository URL (e.g., https://gitlab.com/username/flora-fauna): " gitlab_url
    
    if [ ! -z "$gitlab_url" ]; then
        git remote add origin "$gitlab_url"
        echo "✅ GitLab remote added: $gitlab_url"
    else
        echo "⚠️  No remote URL provided. You can add it later with:"
        echo "   git remote add origin https://gitlab.com/username/flora-fauna"
    fi
fi

# Check current status
echo ""
echo "📊 Repository Status"
echo "==================="
echo "📍 Current branch: $(git branch --show-current 2>/dev/null || echo 'No branch')"
echo "🔗 Remote URL: $(git remote get-url origin 2>/dev/null || echo 'No remote set')"
echo "📝 Uncommitted changes: $(git status --porcelain | wc -l)"

# GitLab CI/CD setup check
echo ""
echo "🔧 GitLab CI/CD Configuration"
echo "============================="

if [ -f ".gitlab-ci.yml" ]; then
    echo "✅ .gitlab-ci.yml found"
else
    echo "❌ .gitlab-ci.yml not found"
fi

if [ -d ".gitlab" ]; then
    echo "✅ .gitlab directory found (templates available)"
else
    echo "⚠️  .gitlab directory not found"
fi

# Deployment readiness check
echo ""
echo "🚀 Deployment Readiness Check"
echo "============================="

checks=(
    "requirements.txt:Requirements file"
    "app.py:Main application file"
    "Dockerfile:Docker configuration"
    ".streamlit/config.toml:Streamlit configuration"
    "Procfile:Heroku configuration"
)

for check in "${checks[@]}"; do
    file=$(echo $check | cut -d: -f1)
    desc=$(echo $check | cut -d: -f2)
    
    if [ -f "$file" ]; then
        echo "✅ $desc"
    else
        echo "❌ $desc ($file missing)"
    fi
done

# Offer deployment options
echo ""
echo "🌐 GitLab Deployment Options"
echo "============================"
echo "1. 📄 Commit and push to GitLab (triggers CI/CD)"
echo "2. 🐳 Set up GitLab Container Registry"
echo "3. 📊 Configure Streamlit Cloud with GitLab"
echo "4. 🚀 Manual deployment setup"
echo "5. 📋 Show deployment URLs"
echo ""

read -p "Select option (1-5): " option

case $option in
    1)
        echo ""
        echo "📤 Committing and Pushing to GitLab"
        echo "==================================="
        
        # Add all files
        git add .
        
        # Commit with timestamp
        commit_msg="Deploy Flora & Fauna Data Collection App - $(date '+%Y-%m-%d %H:%M:%S')"
        git commit -m "$commit_msg"
        
        # Push to main branch
        echo "🚀 Pushing to GitLab..."
        git push -u origin main
        
        if [ $? -eq 0 ]; then
            echo "✅ Successfully pushed to GitLab!"
            echo "🔍 Check your GitLab repository for CI/CD pipeline status"
            echo "📊 Pipeline URL: $(git remote get-url origin | sed 's/\.git$//')/-/pipelines"
        else
            echo "❌ Push failed. Check your GitLab credentials and repository permissions."
        fi
        ;;
    
    2)
        echo ""
        echo "🐳 GitLab Container Registry Setup"
        echo "=================================="
        echo "📋 Steps to enable Container Registry:"
        echo "1. Go to your GitLab project"
        echo "2. Navigate to Settings > General > Visibility"
        echo "3. Enable Container Registry"
        echo "4. Push code to trigger automatic Docker build"
        echo ""
        echo "🔗 Your registry URL will be:"
        gitlab_url=$(git remote get-url origin 2>/dev/null)
        if [ ! -z "$gitlab_url" ]; then
            registry_url=$(echo "$gitlab_url" | sed 's|https://gitlab.com/|registry.gitlab.com/|' | sed 's/\.git$//')
            echo "   $registry_url"
        else
            echo "   registry.gitlab.com/username/flora-fauna"
        fi
        ;;
    
    3)
        echo ""
        echo "📊 Streamlit Cloud + GitLab Setup"
        echo "================================="
        echo "📋 Steps:"
        echo "1. Go to https://share.streamlit.io"
        echo "2. Sign in and click 'New app'"
        echo "3. Connect to GitLab"
        echo "4. Select your repository"
        echo "5. Set main file path: app.py"
        echo "6. Deploy!"
        echo ""
        echo "🔗 Your app will be available at:"
        echo "   https://share.streamlit.io/username/flora-fauna/main/app.py"
        ;;
    
    4)
        echo ""
        echo "🚀 Manual Deployment Options"
        echo "============================"
        echo "🐳 Docker:"
        echo "   docker build -t flora-fauna ."
        echo "   docker run -p 8501:8501 flora-fauna"
        echo ""
        echo "🌐 Local network:"
        echo "   streamlit run app.py --server.address 0.0.0.0"
        echo ""
        echo "☁️  Heroku:"
        echo "   heroku create your-app-name"
        echo "   git push heroku main"
        echo ""
        echo "🚂 Railway:"
        echo "   Connect GitLab repository at railway.app"
        ;;
    
    5)
        echo ""
        echo "📋 Deployment URLs"
        echo "=================="
        gitlab_url=$(git remote get-url origin 2>/dev/null)
        if [ ! -z "$gitlab_url" ]; then
            project_path=$(echo "$gitlab_url" | sed 's|https://gitlab.com/||' | sed 's/\.git$//')
            username=$(echo "$project_path" | cut -d/ -f1)
            repo_name=$(echo "$project_path" | cut -d/ -f2)
            
            echo "🦊 GitLab Project: $gitlab_url"
            echo "🐳 Container Registry: registry.gitlab.com/$project_path"
            echo "📄 GitLab Pages: https://$username.gitlab.io/$repo_name"
            echo "📊 Streamlit Cloud: https://share.streamlit.io/$project_path/main/app.py"
            echo "🔍 CI/CD Pipelines: $gitlab_url/-/pipelines"
        else
            echo "⚠️  No GitLab remote configured"
        fi
        ;;
    
    *)
        echo "❌ Invalid option"
        ;;
esac

echo ""
echo "📖 For detailed instructions, see:"
echo "   • GITLAB_DEPLOYMENT.md"
echo "   • .gitlab-ci.yml (CI/CD configuration)"
echo "   • deployment.html (visual guide)"
