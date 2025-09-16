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
from task_manager.users.forms import UserLoginForm

def index(request):
    return render(request, 'index.html')

urlpatterns = [
    path('', index, name='home'),
    path('users/', include('task_manager.users.urls', namespace='users')),
    path('tasks/', include('task_manager.tasks.urls', namespace='tasks')),
    path('statuses/', include('task_manager.statuses.urls', namespace='statuses')),
    path('labels/', include('task_manager.labels.urls', namespace='labels')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', form_class=UserLoginForm, next_page='/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
