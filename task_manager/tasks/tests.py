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


class TaskFilterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )
        self.status1 = Status.objects.create(name='Новый')
        self.status2 = Status.objects.create(name='В работе')
        self.label1 = Label.objects.create(name='Важно')
        self.label2 = Label.objects.create(name='Срочно')

        # Создаем тестовые задачи
        self.task1 = Task.objects.create(
            name='Задача 1',
            description='Описание 1',
            status=self.status1,
            author=self.user1,
            executor=self.user2
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Задача 2',
            description='Описание 2',
            status=self.status2,
            author=self.user2,
            executor=self.user1
        )
        self.task2.labels.add(self.label2)

        self.task3 = Task.objects.create(
            name='Задача 3',
            description='Описание 3',
            status=self.status1,
            author=self.user1
        )
        self.task3.labels.add(self.label1, self.label2)

    def test_filter_by_status(self):
        """Тест: фильтрация по статусу"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('tasks:tasks'), {'status': self.status1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertContains(response, 'Задача 3')
        self.assertNotContains(response, 'Задача 2')

    def test_filter_by_executor(self):
        """Тест: фильтрация по исполнителю"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('tasks:tasks'), {'executor': self.user2.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')
        self.assertNotContains(response, 'Задача 3')

    def test_filter_by_label(self):
        """Тест: фильтрация по метке"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('tasks:tasks'), {'labels': self.label1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')
        self.assertContains(response, 'Задача 3')

    def test_filter_by_author(self):
        """Тест: фильтрация по автору (только мои задачи)"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('tasks:tasks'), {'author': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')
        self.assertContains(response, 'Задача 3')

    def test_filter_combination(self):
        """Тест: комбинированная фильтрация"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('tasks:tasks'), {
            'status': self.status1.id,
            'labels': self.label1.id,
            'author': 'true'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')
        self.assertContains(response, 'Задача 3')

    def test_filter_form_display(self):
        """Тест: отображение формы фильтров"""
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('tasks:tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Фильтры')
        self.assertContains(response, 'Статус')
        self.assertContains(response, 'Исполнитель')
        self.assertContains(response, 'Метка')
        self.assertContains(response, 'Только мои задачи')
