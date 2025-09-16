from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskCRUDTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            first_name='Other',
            last_name='User'
        )
        self.status = Status.objects.create(name='Новый')
        self.label = Label.objects.create(name='Важно')
        
    def test_task_list_view_requires_login(self):
        """Тест: список задач требует авторизации"""
        response = self.client.get(reverse('tasks:tasks'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/tasks/')
        
    def test_task_create_view_requires_login(self):
        """Тест: создание задачи требует авторизации"""
        response = self.client.get(reverse('tasks:create_task'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/tasks/create/')
        
    def test_task_create_success(self):
        """Тест: успешное создание задачи"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Тестовая задача',
            'description': 'Описание задачи',
            'status': self.status.id,
            'executor': self.other_user.id,
            'labels': [self.label.id]
        }
        response = self.client.post(reverse('tasks:create_task'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Тестовая задача').exists())
        
    def test_task_create_sets_author(self):
        """Тест: автор задачи устанавливается автоматически"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Тестовая задача',
            'description': 'Описание задачи',
            'status': self.status.id,
        }
        self.client.post(reverse('tasks:create_task'), data)
        task = Task.objects.get(name='Тестовая задача')
        self.assertEqual(task.author, self.user)
        
    def test_task_update_requires_login(self):
        """Тест: редактирование задачи требует авторизации"""
        task = Task.objects.create(
            name='Тестовая задача',
            description='Описание',
            status=self.status,
            author=self.user
        )
        response = self.client.get(reverse('tasks:update_task', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        
    def test_task_update_only_by_author(self):
        """Тест: редактировать задачу может только автор"""
        task = Task.objects.create(
            name='Тестовая задача',
            description='Описание',
            status=self.status,
            author=self.user
        )
        
        # Попытка редактирования другим пользователем
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('tasks:update_task', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:tasks'))
        
        # Редактирование автором
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tasks:update_task', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        
    def test_task_delete_requires_login(self):
        """Тест: удаление задачи требует авторизации"""
        task = Task.objects.create(
            name='Тестовая задача',
            description='Описание',
            status=self.status,
            author=self.user
        )
        response = self.client.get(reverse('tasks:delete_task', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        
    def test_task_delete_only_by_author(self):
        """Тест: удалять задачу может только автор"""
        task = Task.objects.create(
            name='Тестовая задача',
            description='Описание',
            status=self.status,
            author=self.user
        )
        
        # Попытка удаления другим пользователем
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('tasks:delete_task', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
        
        # Удаление автором
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('tasks:delete_task', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
        
    def test_task_detail_view_requires_login(self):
        """Тест: просмотр задачи требует авторизации"""
        task = Task.objects.create(
            name='Тестовая задача',
            description='Описание',
            status=self.status,
            author=self.user
        )
        response = self.client.get(reverse('tasks:task_detail', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        
    def test_task_detail_view_authenticated(self):
        """Тест: просмотр задачи авторизованным пользователем"""
        task = Task.objects.create(
            name='Тестовая задача',
            description='Описание',
            status=self.status,
            author=self.user
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tasks:task_detail', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая задача')
