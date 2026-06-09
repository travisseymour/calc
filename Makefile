# Makefile
# --------
# Usage:
# make [COMMAND]
# E.g.:
# make build

.PHONY: build clean clean-pycache format install uninstall

SHELL := /usr/bin/env bash

install:
	@if [[ -n "$$VIRTUAL_ENV" ]]; then \
	    echo "Installing calc dependencies into virtual environment $$VIRTUAL_ENV"; \
	    pip install -U pip wheel; \
		pip install -e; \
	    pip install -e .[dev]; \
	else \
	    echo "Not in a virtual environment, install one first and then try again."; \
	fi

uninstall:
	@if [[ -n "$$VIRTUAL_ENV" ]]; then \
	    echo "Uninstalling calc dependencies from virtual environment $$VIRTUAL_ENV"; \
	    pip uninstall calc; \

	else \
	    echo "Not in a virtual environment, nothing to uninstall."; \
	fi

format:
	ruff check calc --fix
	ruff format calc

build:
	python -m build

clean:
	rm -rf build dist *.egg-info

clean-pycache:
	find . -type d -name "__pycache__" -exec rm -rf {} +
