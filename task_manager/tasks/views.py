from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task_template/delete.html'
    success_url = reverse_lazy('tasks:tasks')
    login_url = reverse_lazy('login')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Задачу может удалить только ее автор')
        return redirect('tasks:tasks')

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.get_object()
        return context
