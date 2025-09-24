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
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from task_manager.users.views import login_view
import rollbar

def index(request):
    return render(request, 'index.html')

def test_rollbar(request):
    """Тестовая страница для проверки Rollbar"""
    try:
        # Генерируем тестовую ошибку
        raise Exception("Тестовая ошибка для Rollbar")
    except Exception as e:
        # Отправляем ошибку в Rollbar
        rollbar.report_exc_info()
        return render(request, 'test_rollbar.html', {'error': str(e)})

def test_rollbar_message(request):
    """Тестовая страница для отправки сообщения в Rollbar"""
    # Отправляем информационное сообщение
    rollbar.report_message("Тестовое сообщение из Django", "info")
    return render(request, 'test_rollbar.html', {
        'error': 'Информационное сообщение отправлено в Rollbar'
    })

urlpatterns = [
    path('', index, name='home'),
    path('test-rollbar/', test_rollbar, name='test_rollbar'),
    path('test-rollbar-message/', test_rollbar_message, name='test_rollbar_message'),
    path('users/', include('task_manager.users.urls', namespace='users')),
    path('tasks/', include('task_manager.tasks.urls', namespace='tasks')),
    path('statuses/', include('task_manager.statuses.urls', namespace='statuses')),
    path('labels/', include('task_manager.labels.urls', namespace='labels')),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
