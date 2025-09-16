from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from .models import Label
from .forms import LabelForm


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'task_labels/labels.html'
    context_object_name = 'labels'
    login_url = reverse_lazy('login')


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'task_labels/create.html'
    success_url = reverse_lazy('labels:labels')
    success_message = 'Метка успешно создана'
    login_url = reverse_lazy('login')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'task_labels/update.html'
    success_url = reverse_lazy('labels:labels')
    success_message = 'Метка успешно изменена'
    login_url = reverse_lazy('login')


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'task_labels/delete.html'
    success_url = reverse_lazy('labels:labels')
    success_message = 'Метка успешно удалена'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasklabel_set.exists():
            messages.error(request, 'Невозможно удалить метку, потому что она используется')
            return redirect('labels:labels')
        return super().post(request, *args, **kwargs)
