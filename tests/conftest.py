import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

DATA = {
    "users": {
        "first": {
            "username": "test_user",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        },
        "second": {
            "username": "another_user",
            "password": "testpass123",
            "first_name": "Another",
            "last_name": "User"
        }
    },
    "statuses": {
        "first": {
            "name": "Новый"
        },
        "second": {
            "name": "В работе"
        }
    },
    "labels": {
        "first": {
            "name": "Важно"
        },
        "second": {
            "name": "Срочно"
        }
    },
    "tasks": {
        "first": {
            "name": "Первая задача",
            "description": "Описание первой задачи",
            "status": "Новый",
            "executor": "Test User"
        },
        "second": {
            "name": "Вторая задача",
            "description": "Описание второй задачи",
            "status": "В работе",
            "executor": "Another User"
        },
        "third": {
            "name": "Третья задача",
            "description": "Описание третьей задачи",
            "status": "Новый",
            "executor": "Test User"
        }
    }
}


@pytest.fixture
def login(page, context):
    def _login(username="test_user", password="testpass123"):
        page.goto("/login/")
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state()
    return _login
