from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class LabelCRUDTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.status = Status.objects.create(name='Новый')

    def test_label_list_view_requires_login(self):
        """Тест: список меток требует авторизации"""
        response = self.client.get(reverse('labels:labels'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/labels/')

    def test_label_create_view_requires_login(self):
        """Тест: создание метки требует авторизации"""
        response = self.client.get(reverse('labels:create_label'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/labels/create/')

    def test_label_create_success(self):
        """Тест: успешное создание метки"""
        self.client.login(username='testuser', password='testpass123')
        data = {'name': 'Важно'}
        response = self.client.post(reverse('labels:create_label'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Важно').exists())

    def test_label_update_requires_login(self):
        """Тест: редактирование метки требует авторизации"""
        label = Label.objects.create(name='Тестовая метка')
        response = self.client.get(reverse('labels:update_label', args=[label.pk]))
        self.assertEqual(response.status_code, 302)

    def test_label_update_success(self):
        """Тест: успешное редактирование метки"""
        label = Label.objects.create(name='Тестовая метка')
        self.client.login(username='testuser', password='testpass123')
        data = {'name': 'Обновленная метка'}
        response = self.client.post(
            reverse('labels:update_label', args=[label.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        label.refresh_from_db()
        self.assertEqual(label.name, 'Обновленная метка')

    def test_label_delete_requires_login(self):
        """Тест: удаление метки требует авторизации"""
        label = Label.objects.create(name='Тестовая метка')
        response = self.client.get(reverse('labels:delete_label', args=[label.pk]))
        self.assertEqual(response.status_code, 302)

    def test_label_delete_success(self):
        """Тест: успешное удаление метки"""
        label = Label.objects.create(name='Тестовая метка')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('labels:delete_label', args=[label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())

    def test_label_delete_with_tasks(self):
        """Тест: нельзя удалить метку, связанную с задачами"""
        label = Label.objects.create(name='Тестовая метка')
        task = Task.objects.create(
            name='Тестовая задача',
            description='Описание',
            status=self.status,
            author=self.user
        )
        task.labels.add(label)

        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('labels:delete_label', args=[label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=label.pk).exists())

    def test_label_unique_name(self):
        """Тест: имена меток должны быть уникальными"""
        Label.objects.create(name='Существующая метка')
        self.client.login(username='testuser', password='testpass123')
        data = {'name': 'Существующая метка'}
        response = self.client.post(reverse('labels:create_label'), data)
        self.assertEqual(response.status_code, 200)  # Форма с ошибкой
        self.assertContains(response, 'уже существует')
