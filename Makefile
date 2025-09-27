install:
	uv sync

dev-install:
	uv sync --group dev

makemigrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate
	uv run python manage.py create_test_users

setup:
	uv run python manage.py migrate
	uv run python manage.py create_test_users

collectstatic:
	uv run python manage.py collectstatic --noinput

run:
	uv run python manage.py runserver

render-start:
	uv run gunicorn task_manager.wsgi:application

build:
	./build.sh

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

test:
	uv run pytest

coverage:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest
	uv run coverage report --show-missing --skip-covered

ci-install:
	uv sync --group dev

ci-migrate:
	uv run python manage.py makemigrations --noinput && \
	uv run python manage.py migrate --noinput && \
	uv run python manage.py create_test_users

ci-test:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest
	uv run coverage xml
	uv run coverage report --show-missing --skip-covered