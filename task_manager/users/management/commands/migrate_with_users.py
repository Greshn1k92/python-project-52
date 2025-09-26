from django.core.management.base import BaseCommand
from django.core.management import call_command
from task_manager.users.models import User

class Command(BaseCommand):
    help = 'Runs migrations and creates test users'

    def handle(self, *args, **options):
        # Выполняем миграции
        call_command('migrate')
        
        # Создаем тестовых пользователей
        users_data = [
            {'username': 'test_user', 'password': 'testpass123', 'first_name': 'Test', 'last_name': 'User'},
            {'username': 'another_user', 'password': 'testpass123', 'first_name': 'Another', 'last_name': 'User'},
            {'username': 'third_user', 'password': 'testpass123', 'first_name': 'Third', 'last_name': 'User'},
        ]

        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(**user_data)
                self.stdout.write(self.style.SUCCESS(f"Successfully created user: {user_data['username']}"))
            else:
                self.stdout.write(self.style.WARNING(f"User '{user_data['username']}' already exists. Skipping."))
        
        self.stdout.write(self.style.SUCCESS('Migration and test users creation completed'))
