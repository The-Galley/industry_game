PYTHON_VERSION = 3.12
PROJECT_NAME = industry_game
TEST_PATH = ./tests/

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

clean_dev:
	rm -rf .venv/

develop: clean_dev  ##@Develop Create project venv
	python$(PYTHON_VERSION) -m venv .venv
	.venv/bin/pip install -U pip poetry
	.venv/bin/poetry config virtualenvs.create false
	.venv/bin/poetry install
	.venv/bin/pre-commit install

local:  ##@Develop Run db and rabbitmq containers
	docker compose -f docker-compose.dev.yaml up --force-recreate --renew-anon-volumes --build

local-down: ##@Develop Stop containers with delete volumes
	docker compose -f docker-compose.dev.yaml down -v

lint-ci: lint-py lint-js ##@Linting Run all linters in CI

lint-py: flake ruff bandit mypy  ##@Linting Run all python linters in CI

lint-js: ##@Linting Run JS linter in CI
	cd ./frontend && yarn lint --no-fix

flake: ##@Linting Run flake8
	.venv/bin/flake8 --max-line-length 88 --format=default $(PROJECT_PATH) 2>&1 | tee flake8.txt

ruff: ##@Linting Run ruff
	.venv/bin/ruff check $(PROJECT_PATH)

bandit: ##@Linting Run bandit
	.venv/bin/bandit -r -ll -iii $(PROJECT_PATH) -f json -o ./bandit.json

mypy: ##@Linting Run mypy
	.venv/bin/mypy --config-file ./pyproject.toml $(PROJECT_PATH)

db-upgrade-head: ##@Database Run db upgrade head
	.venv/bin/python -m $(PROJECT_NAME).db --pg-dsn=$(APP_PG_DSN) upgrade head

db-downgrade: ##@Database Run db downgrade to previous version
	.venv/bin/python -m $(PROJECT_NAME).db --pg-dsn=$(APP_PG_DSN) downgrade -1

db-revision: ##@Database Create new revision
	.venv/bin/python -m $(PROJECT_NAME).db --pg-dsn=$(APP_PG_DSN) revision --autogenerate -m "Initial migration"

docker-db-upgrade-head:
	docker compose exec rest python -m industry_game.db upgrade head
