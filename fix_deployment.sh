#!/bin/bash

# Deployment fix script for Flora & Fauna Data Collection App
echo "🌱 Flora & Fauna - Fixing GitLab CI/CD Pipeline"
echo "=============================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Please run this from your project root."
    exit 1
fi

# Check git status
echo "📋 Current git status:"
git status --short

# Add the fixed files
echo "📦 Adding updated GitLab CI configuration..."
git add .gitlab-ci.yml

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit."
else
    echo "💾 Committing GitLab CI fixes..."
    git commit -m "Fix GitLab CI pipeline configuration

- Fixed deployment_info job script formatting
- Removed special characters that caused parsing errors
- Simplified script commands for better compatibility
- Updated Flora & Fauna branding throughout pipeline"

    echo "🚀 Ready to push! Run: git push origin main"
fi

echo ""
echo "✅ GitLab CI configuration has been fixed!"
echo "📋 Changes made:"
echo "   • Fixed script formatting in deployment_info job"
echo "   • Removed problematic special characters"
echo "   • Simplified echo commands"
echo "   • Maintained all deployment functionality"
echo ""
echo "🔗 Next steps:"
echo "   1. Push changes: git push origin main"
echo "   2. Check GitLab pipeline status"
echo "   3. Deploy using your preferred method"
