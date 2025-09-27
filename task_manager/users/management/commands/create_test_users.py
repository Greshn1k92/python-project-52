from django.core.management.base import BaseCommand
from task_manager.users.models import User


class Command(BaseCommand):
    help = 'Create test users for Playwright tests'

    def handle(self, *args, **options):
        # Create test users if they don't exist
        users_data = [
            {
                'username': 'test_user',
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
                'password': 'test_password'
            },
            {
                'username': 'another_user',
                'first_name': 'Another',
                'last_name': 'User',
                'email': 'another@example.com',
                'password': 'test_password'
            },
            {
                'username': 'third_user',
                'first_name': 'Third',
                'last_name': 'User',
                'email': 'third@example.com',
                'password': 'test_password'
            }
        ]

        for user_data in users_data:
            username = user_data['username']
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created user: {username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User {username} already exists')
                )

        self.stdout.write(
            self.style.SUCCESS('Test users creation completed')
        )
