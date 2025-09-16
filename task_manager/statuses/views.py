from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from .models import Status
from .forms import StatusForm


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'task_statuses/statuses.html'
    context_object_name = 'statuses'
    login_url = reverse_lazy('login')


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'task_statuses/create.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = 'Статус успешно создан'
    login_url = reverse_lazy('login')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'task_statuses/update.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = 'Статус успешно изменен'
    login_url = reverse_lazy('login')


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'task_statuses/delete.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = 'Статус успешно удален'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if status.task_set.exists():
            messages.error(request, 'Невозможно удалить статус, потому что он используется')
            return redirect('statuses:statuses')
        return super().post(request, *args, **kwargs)
