VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip

RM := rm -rf

.PHONY: venv venv-docs clean-venv clean-build clean-docs clean api docs build test

venv:
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
		$(PIP) install -U pip wheel setuptools; \
	fi
	$(PIP) install -U -e .

venv-docs:
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
		$(PIP) install -U pip wheel setuptools; \
	fi
	$(PIP) install -U -e ".[docs]"

clean-venv:
	$(RM) $(VENV)

clean-build:
	$(RM) *.egg-info build dist

clean-docs:
	$(RM) docs/build docs/source/api/methods docs/source/api/iban docs/source/api/countries.rst

clean: clean-venv clean-build clean-docs

api:
	$(PYTHON) -m compiler.docs.compiler

docs: api
	$(VENV)/bin/sphinx-build -b dirhtml "docs/source" "docs/build/html" -j auto

build:
	hatch build

test:
	$(PYTHON) -m pytest --cov=smartfaker --cov-report=term-missing
