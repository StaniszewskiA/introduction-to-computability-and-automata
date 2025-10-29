PYTHON = python
VENV_ACTIVATE = venv\Scripts\Activate.ps1
PIP = pip
PYTEST = python -m pytest

setup:
	$(PYTHON) -m venv venv
	powershell -Command "& { . $(VENV_ACTIVATE); $(PIP) install pytest pytest-cov }"

install:
	powershell -Command "& { . $(VENV_ACTIVATE); $(PIP) install pytest pytest-cov }"

test:
	powershell -Command "& { . $(VENV_ACTIVATE); $(PYTEST) tests/regular/regular_expression.py tests/regular/fsa.py -v }"

test-regular-grammar:
	powershell -Command "& { . $(VENV_ACTIVATE); $(PYTEST) tests/regular/regular_grammar.py -v }"

test-regex:
	powershell -Command "& { . $(VENV_ACTIVATE); $(PYTEST) tests/regular/regular_expression.py -v }"

test-fsa:
	powershell -Command "& { . $(VENV_ACTIVATE); $(PYTEST) tests/regular/fsa.py -v }"

coverage:
	powershell -Command "& { . $(VENV_ACTIVATE); $(PYTEST) tests/regular/regular_expression.py tests/regular/fsa.py --cov=src --cov-report=html --cov-report=term }"

clean:
	powershell -Command "Remove-Item -Path .pytest_cache -Recurse -Force -ErrorAction SilentlyContinue"
	powershell -Command "Remove-Item -Path htmlcov -Recurse -Force -ErrorAction SilentlyContinue"
	powershell -Command "Remove-Item -Path .coverage -Force -ErrorAction SilentlyContinue"
	powershell -Command "Get-ChildItem -Path . -Recurse -Name '__pycache__' | Remove-Item -Recurse -Force"

.PHONY: help setup install test test-regular test-fsa test-verbose coverage clean lint
