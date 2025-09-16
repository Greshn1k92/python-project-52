from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        queryset = Task.objects.all()
        if self.request.GET.get('status'):
            queryset = queryset.filter(status_id=self.request.GET.get('status'))
        if self.request.GET.get('executor'):
            queryset = queryset.filter(executor_id=self.request.GET.get('executor'))
        if self.request.GET.get('label'):
            queryset = queryset.filter(labels__id=self.request.GET.get('label'))
        if self.request.GET.get('author'):
            queryset = queryset.filter(author_id=self.request.GET.get('author'))
        return queryset


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy('login')


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = 'Задача успешно создана'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = 'Задача успешно изменена'
    login_url = reverse_lazy('login')

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
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = 'Задача успешно удалена'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, 'Задачу может удалить только её автор')
            return redirect('tasks:tasks')
        return super().post(request, *args, **kwargs)
