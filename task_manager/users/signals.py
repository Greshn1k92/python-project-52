from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_migrate)
def create_test_users(sender, **kwargs):
    """Создает тестовых пользователей после миграций"""
    if sender.name == 'users':  # Только для приложения users
        users_data = [
            {'username': 'test_user', 'password': 'testpass123', 'first_name': 'Test', 'last_name': 'User'},
            {'username': 'another_user', 'password': 'testpass123', 'first_name': 'Another', 'last_name': 'User'},
            {'username': 'third_user', 'password': 'testpass123', 'first_name': 'Third', 'last_name': 'User'},
        ]

        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(**user_data)
                print(f"Successfully created user: {user_data['username']}")
            else:
                print(f"User '{user_data['username']}' already exists. Skipping.")
        
        print('Test users creation completed')
