COMPOSE_RUN_APP := run --rm web
.DEFAULT_GOAL := help

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build:  ## Build application
	docker-compose build

generate-migrations:  ## Generate new migrations
	docker-compose $(COMPOSE_RUN_APP) alembic revision --autogenerate -m '$(NAME)'

migrate:  ## Apply migrations
	docker-compose $(COMPOSE_RUN_APP) alembic upgrade head

generate-secret:  ## Generate and print secret key
	docker-compose $(COMPOSE_RUN_APP) python -c 'from utils import generate_secret;print(generate_secret())'

start:  ## Start application
	docker-compose up -d

isort:  ## Run isort
	docker-compose $(COMPOSE_RUN_APP) isort .

flake8:  ## Run flake8
	docker-compose $(COMPOSE_RUN_APP) flake8

mypy:  ## Run mypy
	docker-compose $(COMPOSE_RUN_APP) mypy .

tests:  ## Run tests
	docker-compose $(COMPOSE_RUN_APP) tests

all_lint:  ## Run all linters
	docker-compose $(COMPOSE_RUN_APP) /bin/sh -c "isort . && flake8 && mypy ."
