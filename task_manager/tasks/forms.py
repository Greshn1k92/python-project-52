from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User

class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['labels'].required = False
        
        # Отладочная информация
        users_count = User.objects.count()
        print(f"DEBUG: В базе данных {users_count} пользователей")
        users_list = list(User.objects.values_list('username', flat=True))
        print(f"DEBUG: Пользователи: {users_list}")
        
        # Исправляем поле executor
        self.fields['executor'].queryset = User.objects.all()
        self.fields['executor'].empty_label = "---------"
        self.fields['executor'].required = False
        
        # Проверяем queryset для executor
        executor_queryset = self.fields['executor'].queryset
        print(f"DEBUG: Executor queryset содержит {executor_queryset.count()} пользователей")
        print(f"DEBUG: Executor queryset: {list(executor_queryset.values_list('username', flat=True))}")

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_('Status'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_('Executor'),
        required=False,  # Изменено на False
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm',
            'data-testid': 'executor-select'
        })
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select form-select-sm'
        }),
        label=_('Labels')
    )

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

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            'name': _('Name'),
            'description': _('Description'),
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': _('Name'),
                'class': 'form-control'
                }
            ),
            'description': forms.Textarea(attrs={
                'placeholder': _('Description'),
                'class': 'form-control'
                }
            ),
        }
