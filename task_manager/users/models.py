
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Можно добавить дополнительные поля или оставить пустым
    pass
    
    def __str__(self):
        return self.username
