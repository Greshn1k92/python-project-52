# Task Manager

[![hexlet-check](https://github.com/Greshn1k92/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Greshn1k92/python-project-52/actions/workflows/hexlet-check.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Greshn1k92_python-project-52&metric=coverage)](https://sonarcloud.io/dashboard?id=Greshn1k92_python-project-52)

Django-based task management system with user authentication, task creation, status management, and label system.

## Features

- 👤 User registration and authentication
- 📝 Task creation, editing, and deletion
- 🏷️ Status and label management
- 🔍 Task filtering and search
- 📱 Responsive Bootstrap UI
- 🧪 Comprehensive test coverage

## Live Demo

🌐 **Live Application**: https://python-project-52-6zp9.onrender.com

## Deployment on Render

### Prerequisites
- GitHub repository with the code
- Render account

### Steps to Deploy

1. **Connect Repository**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `task-manager` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn task_manager.wsgi:application`

3. **Environment Variables**
   Set these in Render dashboard:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   ROLLBAR_ACCESS_TOKEN=your-rollbar-token (optional)
   ```

4. **Database**
   - Render will automatically provide a PostgreSQL database
   - The `DATABASE_URL` environment variable will be set automatically

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### Files for Deployment

- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification
- `Procfile` - Process configuration for Render
- `build.sh` - Build script for deployment
- `static/` - Static files directory

## Local Development

### Setup
```bash
# Clone repository
git clone <repository-url>
cd python-project-52

# Install dependencies
uv sync

# Run migrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser

# Run development server
uv run python manage.py runserver
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=task_manager
```

