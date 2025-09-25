# tests/conftest.py
import pytest
from playwright.sync_api import Page


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
            "name": "В работе"
        },
        "second": {
            "name": "Завершено"
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
            "name": "Тестовая задача",
            "description": "Описание тестовой задачи",
            "status": "В работе",
            "executor": "Test User",
            "labels": {
                "first": "Важно",
                "third": "Срочно"
            }
        },
        "second": {
            "name": "Вторая задача",
            "description": "Описание второй задачи", 
            "status": "Завершено",
            "executor": "Another User",
            "labels": {
                "first": "Важно",
                "second": "Срочно"
            }
        },
        "third": {
            "name": "Третья задача",
            "description": "Описание третьей задачи",
            "status": "В работе",
            "executor": "Test User"
        }
    }
}


def login(page: Page, context):
    """Функция для входа в систему"""
    page.goto("/login/")
    page.fill('input[name="username"]', DATA["users"]["first"]["username"])
    page.fill('input[name="password"]', DATA["users"]["first"]["password"])
    page.click('button[type="submit"]')
    page.wait_for_load_state()


@pytest.fixture
def context():
    """Фикстура для контекста тестов"""
    return {}
