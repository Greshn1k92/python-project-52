from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убедитесь, что поле executor правильно настроено
        self.fields['executor'].empty_label = None  # или "----------"
        self.fields['executor'].label = "Исполнитель"

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if hasattr(self, 'instance') and self.instance.pk:
            if Task.objects.filter(name=name).exclude(
                    pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    _("Task with this name already exists."))
        else:
            if Task.objects.filter(name=name).exists():
                raise forms.ValidationError(
                    _("Task with this name already exists."))

        return name
