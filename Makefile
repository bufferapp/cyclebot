.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo -e "Usage: \tmake [TARGET]\n"
	@echo -e "Targets:"
	@echo -e "  deps                Installs and checks for dependencies (Pipenv)"
	@echo -e "  init                Initialize the Python enviroment, make sure to run this before using make run"
	@echo -e "  requirements.txt    Generates the requirements.txt file"
	@echo -e "  run                 Execute the app locally"
	@echo -e "  deploy              Deploy the app to AWS lambda/API gateway"

.PHONY: deps
deps:
	@pip install pipenv

.PHONY: init
init: deps
	@pipenv install

requirements.txt: deps
	@pipenv lock -r > requirements.txt

.PHONY: run
run:
	@pipenv run ./cyclebot.py

.PHONY: deploy
deploy: deps requirements.txt
	@pipenv run slam deploy
