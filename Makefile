COMPOSE_RUN_APP := run --rm web

build:
	docker-compose build

generate_migrations:
	docker-compose $(COMPOSE_RUN_APP) alembic revision --autogenerate -m '$(NAME)'

migrate:
	docker-compose $(COMPOSE_RUN_APP) alembic upgrade head

start:
	docker-compose up -d

isort:
	docker-compose $(COMPOSE_RUN_APP) isort .

flake8:
	docker-compose $(COMPOSE_RUN_APP) flake8

mypy:
	docker-compose $(COMPOSE_RUN_APP) mypy -m api

tests:
	docker-compose $(COMPOSE_RUN_APP) /bin/bash -c "mypy tests && pytest"