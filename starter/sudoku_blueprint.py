"""Flask blueprint for the Sudoku app routes."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from flask import Blueprint, jsonify, render_template, request

from sudoku_constants import EMPTY, SIZE
from sudoku_generator import generate_puzzle
from sudoku_validator import evaluate_board_state, find_incorrect_cells

bp = Blueprint("sudoku", __name__)


CURRENT: Dict[str, Any] = {
    "puzzle": None,
    "solution": None,
    "hints_used": 0,
}


@bp.route("/")
def index() -> str:
    """Render the main Sudoku page."""
    return render_template("index.html")


@bp.route("/new")
def new_game():
    """Generate and return a new puzzle for the current session."""
    clues = request.args.get("clues", default=35, type=int)
    difficulty = request.args.get("difficulty", default="easy")
    puzzle, solution = generate_puzzle(clues=clues, difficulty=difficulty)
    CURRENT["puzzle"] = puzzle
    CURRENT["solution"] = solution
    CURRENT["hints_used"] = 0
    return jsonify({"puzzle": puzzle, "difficulty": difficulty, "hints_used": 0})


@bp.route("/hint", methods=["POST"])
def apply_hint():
    """Fill one empty editable cell with the correct value."""
    data = request.json or {}
    board = data.get("board")
    solution = CURRENT.get("solution")
    puzzle = CURRENT.get("puzzle")

    if solution is None or puzzle is None:
        return jsonify({"error": "No game in progress"}), 400

    if not isinstance(board, list) or len(board) != SIZE:
        return jsonify({"error": "Invalid board"}), 400

    if evaluate_board_state(board, solution) == "complete":
        return jsonify({"board": board, "position": None, "hints_used": CURRENT.get("hints_used", 0)})

    updated_board = [row[:] for row in board]
    chosen_position: Optional[List[int]] = None
    for row in range(SIZE):
        for col in range(SIZE):
            if updated_board[row][col] == EMPTY and puzzle[row][col] == EMPTY:
                updated_board[row][col] = solution[row][col]
                chosen_position = [row, col]
                CURRENT["hints_used"] = CURRENT.get("hints_used", 0) + 1
                break
        if chosen_position is not None:
            break

    return jsonify({
        "board": updated_board,
        "position": chosen_position,
        "hints_used": CURRENT.get("hints_used", 0),
    })


@bp.route("/check", methods=["POST"])
def check_solution():
    """Validate the submitted board against the current solution."""
    data = request.json
    board = data.get("board")
    solution = CURRENT.get("solution")
    if solution is None:
        return jsonify({"error": "No game in progress"}), 400

    incorrect = find_incorrect_cells(board, solution)
    status = evaluate_board_state(board, solution)
    return jsonify({"incorrect": incorrect, "status": status})
