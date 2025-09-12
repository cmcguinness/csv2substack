.PHONY: help install-dev test

help:
	@echo "Common targets:"
	@echo "  make install-dev   # install dev dependencies"
	@echo "  make test          # run pytest"

install-dev:
	python -m pip install -U pip
	python -m pip install -r requirements-dev.txt

test:
	python -m pytest -q

