#!/bin/bash
# Quick setup script for new Supabase project

echo "🚀 Setting up Flora & Fauna Data Collection for Team Use"
echo "========================================================="

echo ""
echo "📋 Steps you need to complete:"
echo ""
echo "1. ✅ Create new Supabase project at https://supabase.com"
echo "2. ✅ Copy Project URL and anon key from Settings → API"
echo "3. ✅ Update .streamlit/secrets.toml with your new credentials"
echo "4. ✅ Run 'streamlit run app.py' and use 'Setup Supabase Storage'"
echo "5. ✅ Share credentials with your team using TEAM_SETUP_GUIDE.md"

echo ""
echo "🔧 Template for your .streamlit/secrets.toml:"
echo "=============================================="
echo ""
cat << 'EOF'
[supabase]
url = "https://YOUR_NEW_PROJECT.supabase.co"
key = "YOUR_NEW_ANON_KEY_HERE"
EOF

echo ""
echo "💡 Benefits of your own project:"
echo "- ✅ Full admin control (can disable RLS)"
echo "- ✅ Team cloud storage access"
echo "- ✅ No permission restrictions"
echo "- ✅ Unlimited file uploads"
echo ""
echo "🎯 Once setup, your team can collaborate with shared cloud storage!"
