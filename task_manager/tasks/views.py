from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import redirect
from django.contrib import messages
from django_filters.views import FilterView
from .models import Task
from .forms import TaskForm
from .filters import TaskFilter


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'task_template/tasks.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    login_url = reverse_lazy('login')
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from task_manager.users.models import User
        context['users'] = User.objects.all()  # ← Передать в контекст
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_template/detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy('login')


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_template/create.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = 'Задача успешно создана'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from task_manager.users.models import User
        
        # Отладочная информация
        users_count = User.objects.count()
        print(f"DEBUG VIEW: В базе данных {users_count} пользователей")
        users_list = list(User.objects.values_list('username', flat=True))
        print(f"DEBUG VIEW: Пользователи: {users_list}")
        
        context['users'] = User.objects.all()
        print(f"DEBUG VIEW: Передаем в контекст {len(context['users'])} пользователей")
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_template/update.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = 'Задача успешно изменена'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from task_manager.users.models import User
        context['users'] = User.objects.all()  # ← Передать в контекст
        return context

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, 'Задачу может изменить только её автор')
            return redirect('tasks:tasks')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, 'Задачу может изменить только её автор')
            return redirect('tasks:tasks')
        return super().post(request, *args, **kwargs)


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'task_template/delete.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = 'Задача успешно удалена'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, 'Задачу может удалить только её автор')
            return redirect('tasks:tasks')
        return super().post(request, *args, **kwargs)
