import django_filters
from django import forms
from task_manager.users.models import User
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from .forms import UserSelectWidget


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        empty_label="Все статусы",
        label="Статус",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        empty_label="Все исполнители",
        label="Исполнитель",
        required=False,
        widget=UserSelectWidget(attrs={'class': 'form-select form-select-sm'})
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(),
        label="Метка",
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select form-select-sm'})
    )
    author = django_filters.BooleanFilter(
        method='filter_author',
        label="Только свои задачи",
        required=False
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'author']

    def filter_author(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset
