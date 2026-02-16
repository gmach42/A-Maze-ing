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
	@echo
	@echo "Available keybinds while running the programm:"
	@echo
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║           A-MAZE-ING - KEYBINDS HELP                 ║"
	@echo "╠══════════════════════════════════════════════════════╣"
	@echo "║  ESC   │ Exit application                            ║"
	@echo "║  a     │ Change Maze generation algorithm            ║"
	@echo "║  c     │ Cycle maze wall colors                      ║"
	@echo "║  d     │ Display/Hide solution path                  ║"
	@echo "║  s     │ Cycle solution path colors                  ║"
	@echo "║  g     │ Toggle 42 animation                         ║"
	@echo "║  r     │ Regenerate new maze                         ║"
	@echo "║  h     │ Show this help message                      ║"
	@echo "╚══════════════════════════════════════════════════════╝"

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	@$(PYTHON) a_maze_ing.py

debug:
	$(PYTHON) -m pdb a_maze_ing.py

test:
	$(PYTHON) -m pytest -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

clean-all: clean
	rm -rf $(VENV)

lint:
	python3 -m flake8 .
	python3 -m mypy . \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs \

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict

.PHONY: help install run test clean debug lint lint-strict
