#!/usr/bin/env python3
import yaml
import sys

def test_gitlab_ci():
    try:
        with open('.gitlab-ci.yml', 'r') as f:
            config = yaml.safe_load(f)
        
        print("✅ GitLab CI YAML is valid!")
        
        # Check required sections
        required_sections = ['stages', 'test_app', 'deployment_info']
        for section in required_sections:
            if section in config:
                print(f"✅ {section} section found")
            else:
                print(f"❌ {section} section missing")
                
        # Check deployment_info specifically
        if 'deployment_info' in config:
            job = config['deployment_info']
            if 'script' in job and isinstance(job['script'], list):
                print(f"✅ deployment_info has {len(job['script'])} script commands")
            else:
                print("❌ deployment_info script is not properly formatted")
                
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_gitlab_ci()
    sys.exit(0 if success else 1)
