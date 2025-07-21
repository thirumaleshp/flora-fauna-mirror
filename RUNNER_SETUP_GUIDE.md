# GitLab Runner Setup Guide for Flora & Fauna App

## 🚀 Quick Start: Enable Shared Runners (Easiest Option)

1. **Go to your project settings**:
   - Navigate to your GitLab project
   - Click **Settings** → **CI/CD**
   - Expand the **"Runners"** section

2. **Enable Shared Runners**:
   - Look for **"Shared runners"** 
   - Toggle **"Enable shared runners for this project"**
   - If this option is available, you're done! ✅

3. **Test your pipeline**:
   - Commit any small change to trigger the pipeline
   - Your `.gitlab-ci.yml` should now work with shared runners

---

## 🔧 Alternative: Create Project-Specific Runner

If shared runners aren't available, follow these steps:

### Step 1: Create Runner in GitLab UI
1. Go to **Settings** → **CI/CD** → **Runners**
2. Click **"New project runner"**
3. Fill out the form:
   - **Tags**: `docker`
   - **Runner description**: `Flora and Fauna App Runner`
   - **Maximum job timeout**: `3600`
   - **Run untagged jobs**: ✅ (check this)
4. Click **"Create runner"**

### Step 2: Install GitLab Runner (Choose your environment)

#### Option A: Docker (Recommended)
```bash
# Run GitLab Runner in Docker
docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:latest
```

#### Option B: Linux/Ubuntu
```bash
# Download and install
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt-get install gitlab-runner
```

#### Option C: Windows
- Download from: https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-windows-amd64.exe
- Rename to `gitlab-runner.exe` and place in your PATH

### Step 3: Register the Runner
After creating the runner in GitLab, you'll get a registration command like:

```bash
gitlab-runner register \
  --url https://gitlab.com \
  --token glrt-xxxxxxxxxxxxxxxxxxxx \
  --executor docker \
  --docker-image python:3.11-slim \
  --description "Flora and Fauna Runner" \
  --tag-list docker
```

### Step 4: Start the Runner
```bash
# If using system installation
sudo gitlab-runner start

# If using Docker
docker start gitlab-runner
```

---

## 🔍 Troubleshooting

### Check Runner Status
```bash
# System installation
sudo gitlab-runner status

# Docker
docker logs gitlab-runner
```

### Common Issues
1. **"No runner available"**: Enable shared runners or register a specific runner
2. **Permission denied**: Ensure Docker socket permissions or run as administrator
3. **Network issues**: Check firewall and GitLab connectivity

### Verify Your Pipeline
Your current `.gitlab-ci.yml` is configured for Docker runners with these tags:
- `docker` (for running in Docker containers)

---

## 🎯 Recommended Approach

1. **First**: Try enabling shared runners (easiest)
2. **If no shared runners**: Use Docker-based runner (most compatible)
3. **For production**: Consider dedicated runner for better control

## 📞 Need Help?
- GitLab Runner docs: https://docs.gitlab.com/runner/
- Docker installation: https://docs.docker.com/get-docker/
- GitLab CI/CD docs: https://docs.gitlab.com/ee/ci/

Your Flora & Fauna app is ready to deploy once a runner is available! 🌿
