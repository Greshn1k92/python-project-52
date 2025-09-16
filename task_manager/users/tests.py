from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class UserCRUDTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_user_registration(self):
        """Test user registration (Create)"""
        url = reverse('create_user')
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_list_view(self):
        """Test user list view is accessible without authentication"""
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_user_update(self):
        """Test user update (Update)"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('update_user', kwargs={'pk': self.user.pk})
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': 'testuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_user_update_unauthorized(self):
        """Test user cannot update another user"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        url = reverse('update_user', kwargs={'pk': other_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect due to unauthorized access

    def test_user_delete(self):
        """Test user deletion (Delete)"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('delete_user', kwargs={'pk': self.user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_user_delete_unauthorized(self):
        """Test user cannot delete another user"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        url = reverse('delete_user', kwargs={'pk': other_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect due to unauthorized access

    def test_login_redirect(self):
        """Test login redirects to home page"""
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_registration_redirect_to_login(self):
        """Test registration redirects to login page"""
        url = reverse('create_user')
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser2',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_update_redirect_to_users_list(self):
        """Test update redirects to users list"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('update_user', kwargs={'pk': self.user.pk})
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': 'testuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users'))