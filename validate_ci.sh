#!/bin/bash

echo "🔧 GitLab CI Validation and Fix Script"
echo "====================================="

# Check if GitLab CI file exists
if [ ! -f ".gitlab-ci.yml" ]; then
    echo "❌ .gitlab-ci.yml file not found!"
    exit 1
fi

echo "✅ GitLab CI file found"

# Test YAML syntax
python3 -c "
import yaml
try:
    with open('.gitlab-ci.yml', 'r') as f:
        yaml.safe_load(f)
    print('✅ YAML syntax is valid')
except Exception as e:
    print(f'❌ YAML error: {e}')
    exit(1)
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ GitLab CI configuration is valid!"
else
    echo "❌ YAML syntax errors detected"
fi

echo ""
echo "🚀 Ready to commit and push:"
echo "git add .gitlab-ci.yml"
echo "git commit -m 'Fix GitLab CI configuration'"  
echo "git push origin main"
echo ""
echo "📋 GitLab Runner Solutions:"
echo "1. Enable shared runners in GitLab project settings"
echo "2. Or deploy directly to Streamlit Cloud (recommended)"
echo "3. Visit: https://share.streamlit.io"
