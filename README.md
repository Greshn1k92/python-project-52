# Task Manager

[![hexlet-check](https://github.com/Greshn1k92/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Greshn1k92/python-project-52/actions/workflows/hexlet-check.yml)

Django-based task management system.

## Live Demo

🌐 **Live Application**: https://python-project-52-6zp9.onrender.com

> **Note**: This project is part of the Hexlet Python course curriculum.

## Features

- User authentication and authorization
- Task management (create, read, update, delete)
- Status management for tasks
- Label management for task categorization
- Task filtering by status, executor, labels, and author
- Error monitoring with Rollbar
- Internationalization support (i18n)
- Responsive design

## Tech Stack

- Python 3.12+
- Django 5.2
- PostgreSQL
- Bootstrap 5
- Rollbar (Error Monitoring)
- django-filter (Task Filtering)

## Setup and Installation

1. Clone the repository
2. Install dependencies: `make install`
3. Apply migrations: `make migrate`
4. Set up environment variables (see Environment Variables section)
5. Start the application: `make run`

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=webserver,127.0.0.1,localhost,*.onrender.com,*

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Rollbar (optional)
ROLLBAR_ACCESS_TOKEN=your-rollbar-access-token-here
```

## Rollbar Setup

1. Create a free account at [Rollbar](https://rollbar.com/)
2. Create a new project and get your access token
3. Set the `ROLLBAR_ACCESS_TOKEN` environment variable
4. Test error reporting by visiting `/test-rollbar/` endpoint

## Development

- Run tests: `make test`
- Check code style: `make lint`
- Run development server: `make run`

## Deployment

- Build command: `make build`
- Start command: `make render-start`
