# Sudoku Game

A polished Flask-based Sudoku experience with a responsive interface, hint support, game timing, a persistent Top 10 scoreboard, and a light/dark theme toggle. The project is organized around modular Python logic for generation, solving, validation, and Flask routes so it is easy to extend and test.

## Features

- Generate a valid Sudoku puzzle with a unique solution for each new game
- Support easy, medium, and hard difficulty levels
- Allow players to check the current board state and request hints
- Highlight conflicting values as the player types
- Track elapsed time and save completion times to a Top 10 scoreboard
- Persist scoreboard data in browser localStorage
- Toggle between light and dark mode
- Provide an accessible, responsive layout for desktop and mobile screens

## Folder structure

```text
.
├── starter/
│   ├── app.py                  # Flask entry point
│   ├── sudoku_blueprint.py    # Flask routes and session state
│   ├── sudoku_constants.py    # Shared Sudoku constants
│   ├── sudoku_generator.py    # Puzzle generation and difficulty logic
│   ├── sudoku_solver.py       # Solving and uniqueness checks
│   ├── sudoku_validator.py    # Board validation helpers
│   ├── static/                # CSS and JavaScript assets
│   ├── templates/             # HTML templates
│   ├── tests/                 # Automated pytest coverage
│   └── Screenshots/           # Feature screenshots used for documentation
```

## Environment setup

Requirements:
- Python 3.9+
- A modern web browser

Install dependencies from the project folder:

```bash
cd starter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-test.txt
```

## Installation command

```bash
cd starter && pip install -r requirements-test.txt
```

## Application run command

```bash
cd starter && python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Test command

From the repository root:

```bash
python -m pytest -q starter/tests
```

## How to use the game

- Difficulty: Use the difficulty selector to load an easy, medium, or hard puzzle.
- Check: Click Check Solution to verify the current board and see whether it is complete, incomplete, or incorrect.
- Hint: Click Hint to reveal one correct value in an empty editable cell and increase the hint counter.
- Timer: A timer starts when a new game begins and stops when the puzzle is solved.
- Scoreboard: When you solve the puzzle, you can enter your name to save your result to the Top 10 scoreboard. The scoreboard is stored in browser localStorage.
- Dark mode: Use the Dark mode toggle in the header to switch between light and dark themes.

## Scoreboard storage

The Top 10 fast-time leaderboard is saved in the browser via localStorage, so it remains available on the same device and browser even after a page refresh.

## Testing summary

The automated test suite covers puzzle generation, solver behavior, validator logic, unique-solution checks, difficulty handling, Flask routes, board checks, and hint requests. The tests are written to verify behavior and avoid brittle expectations around random board content.

## Screenshots

The Screenshots folder contains images that document features such as difficulty selection, the hint button, the timer, the scoreboard, responsive layout, dark mode, and validation feedback. These images are intended to help users understand the completed experience at a glance.
