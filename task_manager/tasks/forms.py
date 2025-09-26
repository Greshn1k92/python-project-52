from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class UserSelectWidget(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            try:
                user = User.objects.get(pk=value)
                option['label'] = user.get_full_name() or user.username
            except User.DoesNotExist:
                pass
        return option

class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="----------",
        required=False,
        widget=UserSelectWidget(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убедитесь, что поле executor правильно настроено
        self.fields['executor'].label = "Исполнитель"
        # Настраиваем queryset для отображения полных имен
        self.fields['executor'].queryset = User.objects.all()
        
    def clean_executor(self):
        executor = self.cleaned_data.get('executor')
        return executor

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
