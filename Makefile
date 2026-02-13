.PHONY: help install run test clean debug lint lint-strict

VENV := .venv
PYTHON := $(VENV)/bin/python3
POETRY := $(VENV)/bin/poetry

help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make run         - Run the application"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean temporary files"
	@echo "  make debug       - Run the application in debug mode"
	@echo "  make lint        - Run linters and type checkers"
	@echo "  make lint-strict - Run linters and type checkers in strict mode"
	@echo "  make keybind     - Show available keybinds while running the program"

keybind:
	@echo "Available keybinds while running the programm:"
	@echo "  - 'h' to show this help message"
	@echo "  - 'd' to show/hide the solution path"
	@echo "  - 'r' to regenerate the maze"
	@echo "  - 's' to change the color of the solution path"
	@echo "  - 'c' to change the color of the maze"
	@echo "  - 'g' to change the color of the 42 symbol"
	@echo "  - 'ESC' to quit the application"

install:
	python3 -m venv .venv
	$(POETRY) install

run: $(VENV)/bin/activate
	$(PYTHON) a_maze_ing.py

$(VENV)/bin/activate: pyproject.toml
	python3 -m venv $(VENV)
	$(POETRY) install

debug:
	$(PYTHON) -m pdb a_maze_ing.py

test:
	$(PYTHON) -m pytest -v

clean:
	rm -rf __pycache__
	rm -rf poetry.lock
	rm -rf $(VENV)

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs \

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict
