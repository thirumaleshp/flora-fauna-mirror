#!/usr/bin/env python3
"""
Deployment Check Script for Flora and Fauna Chatbot
Run this script to verify all dependencies and components are working correctly.
"""

import sys
import importlib

def check_dependency(module_name):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} - Available")
        return True
    except ImportError as e:
        print(f"✗ {module_name} - Missing: {e}")
        return False

def main():
    print("Flora and Fauna Chatbot - Deployment Check")
    print("=" * 50)
    
    # Check required dependencies
    dependencies = [
        'streamlit',
        'pandas',
        'supabase',
        'requests'
    ]
    
    missing_deps = []
    for dep in dependencies:
        if not check_dependency(dep):
            missing_deps.append(dep)
    
    print("\n" + "=" * 50)
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("\nTo install missing dependencies, run:")
        print(f"pip install {' '.join(missing_deps)}")
        return False
    else:
        print("✅ All dependencies are available!")
    
    # Check if chatbot can be imported
    print("\nChecking chatbot module...")
    try:
        from chatbot import FloraFaunaChatbot
        print("✓ FloraFaunaChatbot - Can be imported")
        
        # Try to create instance
        chatbot = FloraFaunaChatbot()
        print("✓ FloraFaunaChatbot - Instance created successfully")
        
        # Check if main method exists
        if hasattr(chatbot, 'process_query_with_media'):
            print("✓ process_query_with_media method - Available")
        else:
            print("✗ process_query_with_media method - Missing")
            
    except Exception as e:
        print(f"✗ FloraFaunaChatbot - Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Deployment check completed successfully!")
    print("Your chatbot should work correctly now.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
