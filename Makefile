DEFAULT_GOAL := help
COMPOSE_RUN_APP := run --rm web

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)## \(.*\)/\1;\3/p' \
	| column -t  -s ';'

build:  ## Build application
	docker-compose build

generate-migrations:  ## Generate new migrations
	docker-compose $(COMPOSE_RUN_APP) alembic revision --autogenerate -m '$(NAME)'

migrate:  ## Apply migrations
	docker-compose $(COMPOSE_RUN_APP) alembic upgrade head

generate-secret:  ## Generate and print secret key
	docker-compose $(COMPOSE_RUN_APP) python -c 'from cryptography.fernet import Fernet;print(Fernet.generate_key())'

start:  ## Start application
	docker-compose up -d

isort:  ## Apply isort to project
	docker-compose $(COMPOSE_RUN_APP) isort .

flake8:  ## Apply flake8 to project
	docker-compose $(COMPOSE_RUN_APP) flake8

mypy:  ## Apply mypy to project
	docker-compose $(COMPOSE_RUN_APP) mypy -m api

tests:  ## Run project's tests
	docker-compose $(COMPOSE_RUN_APP) /bin/bash -c "mypy tests && pytest"