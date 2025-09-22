from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.users.forms import UserRegistrationForm, UserLoginForm


class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'

    def form_valid(self, form):
        # Сохраняем пользователя, но НЕ входим в систему
        user = form.save()
        # Добавляем сообщение об успехе
        messages.success(self.request, self.success_message)
        # Не делаем автоматический вход - просто перенаправляем
        return redirect(self.success_url)


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:users')
    success_message = 'Пользователь успешно изменен'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users:users')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:users')
    success_message = 'Пользователь успешно удален'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users:users')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user.authored_tasks.exists() or user.assigned_tasks.exists():
            messages.error(request, 'Невозможно удалить пользователя, потому что он связан с задачами')
            return redirect('users:users')
        return super().post(request, *args, **kwargs)


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = 'Вы залогинены'
    next_page = reverse_lazy('home')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')
