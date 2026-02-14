VENV := .venv
PYTHON := $(VENV)/bin/python3
POETRY := $(VENV)/bin/poetry
PIP := $(VENV)/bin/pip

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
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirement.txt

run:
	@$(PYTHON) a_maze_ing.py

debug:
	$(PYTHON) -m pdb a_maze_ing.py

test:
	$(PYTHON) -m pytest -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
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

.PHONY: help install run test clean debug lint lint-strict