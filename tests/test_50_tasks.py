# tests/test_50_tasks.py
import re
from urllib.parse import urljoin
from .conftest import login, DATA


class TestTask:
    def test_create_show(self, page, context, base_url):
        login(page, context)

        page.goto("/tasks/")
        page.click('text="Создать задачу"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/tasks/create/")

        page.fill('input[name="name"]', DATA["tasks"]["first"]["name"])
        page.fill('textarea[name="description"]', DATA["tasks"]["first"]["description"])
        page.select_option('select[name="status"]', label=DATA["tasks"]["first"]["status"])
        # ИСПРАВЛЕННАЯ СТРОКА - используем #id_executor вместо text=
        page.select_option('#id_executor', label=DATA["tasks"]["first"]["executor"])
        
        page.click('button[type="submit"]')
        page.wait_for_load_state()

        # Проверяем, что мы вернулись на страницу списка задач
        assert page.url == urljoin(base_url, "/tasks/")
        
        # Проверяем, что задача появилась в списке
        assert page.locator('text="' + DATA["tasks"]["first"]["name"] + '"').is_visible()

    def test_create_task(self, page, context, base_url):
        login(page, context)

        page.goto("/tasks/create/")
        
        page.fill('input[name="name"]', DATA["tasks"]["second"]["name"])
        page.fill('textarea[name="description"]', DATA["tasks"]["second"]["description"])
        page.select_option('select[name="status"]', label=DATA["tasks"]["second"]["status"])
        page.select_option('#id_executor', label=DATA["tasks"]["second"]["executor"])
        
        page.click('button[type="submit"]')
        page.wait_for_load_state()

        # Проверяем, что мы вернулись на страницу списка задач
        assert page.url == urljoin(base_url, "/tasks/")
        
        # Проверяем, что задача появилась в списке
        assert page.locator('text="' + DATA["tasks"]["second"]["name"] + '"').is_visible()

    def test_update_task(self, page, context, base_url):
        login(page, context)

        page.goto("/tasks/")
        
        # Находим первую задачу и кликаем "Изменить"
        task_row = page.locator('tr').filter(has_text=DATA["tasks"]["first"]["name"]).first
        task_row.locator('a[href*="/update/"]').click()
        page.wait_for_load_state()

        # Изменяем название задачи
        new_name = "Обновленная задача"
        page.fill('input[name="name"]', new_name)
        page.click('button[type="submit"]')
        page.wait_for_load_state()

        # Проверяем, что мы вернулись на страницу списка задач
        assert page.url == urljoin(base_url, "/tasks/")
        
        # Проверяем, что задача обновилась
        assert page.locator('text="' + new_name + '"').is_visible()

    def test_delete_task(self, page, context, base_url):
        login(page, context)

        page.goto("/tasks/")
        
        # Находим задачу и кликаем "Удалить"
        task_row = page.locator('tr').filter(has_text=DATA["tasks"]["second"]["name"]).first
        task_row.locator('a[href*="/delete/"]').click()
        page.wait_for_load_state()

        # Подтверждаем удаление
        page.click('button[type="submit"]')
        page.wait_for_load_state()

        # Проверяем, что мы вернулись на страницу списка задач
        assert page.url == urljoin(base_url, "/tasks/")
        
        # Проверяем, что задача удалена
        assert not page.locator('text="' + DATA["tasks"]["second"]["name"] + '"').is_visible()
