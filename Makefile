VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip

RM := rm -rf

.PHONY: venv venv-docs clean-venv clean-build clean-docs clean docs build

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
	$(RM) docs/build

clean: clean-venv clean-build clean-docs

docs:
	$(VENV)/bin/sphinx-build -b dirhtml "docs/source" "docs/build/html" -j auto

build:
	hatch build
