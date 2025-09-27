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
        page.fill(
            'textarea[name="description"]',
            DATA["tasks"]["first"]["description"])
        page.select_option(
            'select[name="status"]', label=DATA["tasks"]["first"]["status"])
        page.select_option(
            '#id_executor', label=DATA["tasks"]["first"]["executor"])
        page.click('button[type="submit"]')
        page.wait_for_load_state()
        assert page.url == urljoin(base_url, "/tasks/")
        assert page.locator(
            'text="' + DATA["tasks"]["first"]["name"] + '"').is_visible()

    def test_update_show(self, page, context, base_url):
        login(page, context)
        page.goto("/tasks/")
        page.click('text="Изменить"')
        page.wait_for_load_state()
        page.fill('input[name="name"]', DATA["tasks"]["second"]["name"])
        page.fill(
            'textarea[name="description"]',
            DATA["tasks"]["second"]["description"])
        page.select_option(
            'select[name="status"]', label=DATA["tasks"]["second"]["status"])
        page.select_option(
            '#id_executor', label=DATA["tasks"]["second"]["executor"])
        page.click('button[type="submit"]')
        page.wait_for_load_state()
        assert page.url == urljoin(base_url, "/tasks/")
        assert page.locator(
            'text="' + DATA["tasks"]["second"]["name"] + '"').is_visible()

    def test_delete_show(self, page, context, base_url):
        login(page, context)
        page.goto("/tasks/")
        page.click('text="Удалить"')
        page.wait_for_load_state()
        page.click('button[type="submit"]')
        page.wait_for_load_state()
        assert page.url == urljoin(base_url, "/tasks/")

    def test_index_filter(self, page, context, base_url):
        login(page, context)
        page.goto("/tasks/")
        page.check('text="Только свои задачи"')
        page.select_option(
            'select[name="executor"]',
            label=DATA["tasks"]["first"]["executor"])
        page.click('button[type="submit"]')
        page.wait_for_load_state()
        assert page.url == urljoin(base_url, "/tasks/")
        assert page.locator(
            'text="' + DATA["tasks"]["first"]["name"] + '"').is_visible()
