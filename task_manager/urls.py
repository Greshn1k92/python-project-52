"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.conf import settings
import os

def index(request):
    # Сначала пробуем найти файл в STATIC_ROOT (продакшен)
    if settings.STATIC_ROOT:
        html_file_path = os.path.join(settings.STATIC_ROOT, 'index.html')
        if os.path.exists(html_file_path):
            with open(html_file_path, 'r', encoding='utf-8') as f:
                return HttpResponse(f.read(), content_type='text/html')
    
    # Затем пробуем в корне проекта (разработка)
    html_file_path = os.path.join(settings.BASE_DIR, 'index.html')
    if os.path.exists(html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/html')
    
    # Если файл не найден, возвращаем простой текст
    return HttpResponse('Hello! Welcome to the main page!')

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
]
