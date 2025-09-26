
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Можно добавить дополнительные поля или оставить пустым
    pass
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        # Убедитесь, что этот метод возвращает полное имя
        return f"{self.first_name} {self.last_name}".strip()
