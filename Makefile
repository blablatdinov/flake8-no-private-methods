SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run ruff check flake8_no_private_methods tests
	poetry run mypy flake8_no_private_methods tests
	./lint-venv/bin/flake8 flake8_no_private_methods tests
	if poetry run command -v doc8 > /dev/null 2>&1; then poetry run doc8 -q docs; fi

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check

.PHONY: test
test: lint package unit
