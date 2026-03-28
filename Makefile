SHELL := /bin/bash

.PHONY: setup format lint test clean ci coverage

setup: clean
	( \
		python3 -m venv venv; \
		source venv/bin/activate; \
		python -m pip install pip --upgrade; \
		pip install -e .; \
		pip install -r requirements-dev.txt \
	)

format:
	black hookdns tests --target-version py39

lint:
	black --check hookdns tests --target-version py39
	flake8 hookdns tests

typing:
	mypy

test:
	pytest -v tests/

clean:
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf hookdns.egg-info
	rm -rf venv

ci:
	python -m pip install pip --upgrade
	pip install .
	pip install -r requirements-dev.txt
	pytest -v tests/

coverage:
	python -m pip install pip --upgrade
	pip install .
	pip install -r requirements-dev.txt
	coverage run -m pytest -v tests/
