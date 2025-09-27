from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, render
from task_manager.users.forms import (
    UserRegistrationForm, UserLoginForm, UserUpdateForm)


class UserListView(ListView):
    model = User
    template_name = 'base_template/users.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'base_template/create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'

    def form_valid(self, form):
        # Сохраняем пользователя, но НЕ входим в систему
        form.save()
        # Добавляем сообщение об успехе
        messages.success(self.request, self.success_message)
        # Не делаем автоматический вход - просто перенаправляем
        return redirect(self.success_url)


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'base_template/update.html'
    success_url = reverse_lazy('users:users')
    success_message = 'Пользователь успешно изменен'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            messages.error(
                request, 'У вас нет прав для изменения другого пользователя.'
            )
            return redirect('users:users')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'base_template/delete.html'
    success_url = reverse_lazy('users:users')
    success_message = 'Пользователь успешно удален'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            messages.error(
                request, 'У вас нет прав для изменения другого пользователя.'
            )
            return redirect('users:users')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user.authored_tasks.exists() or user.assigned_tasks.exists():
            messages.error(
                request,
                'Невозможно удалить пользователя, '
            'потому что он связан с задачами'
            )
            return redirect('users:users')
        return super().post(request, *args, **kwargs)


def login_view(request):
    """Функциональный view для входа с сообщением об успехе"""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Вы залогинены')
                return redirect('home')
            else:
                messages.error(request, 'Неверные учетные данные')
    else:
        form = UserLoginForm()

    return render(request, 'base_template/login.html', {'form': form})


def logout_view(request):
    """Функциональный view для выхода с сообщением"""
    logout(request)
    messages.success(request, 'Вы разлогинены')
    return redirect('home')
