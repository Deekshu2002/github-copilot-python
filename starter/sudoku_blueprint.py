"""Flask blueprint for the Sudoku app routes."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from flask import Blueprint, jsonify, render_template, request

from sudoku_constants import SIZE
from sudoku_generator import generate_puzzle
from sudoku_validator import find_incorrect_cells

bp = Blueprint("sudoku", __name__)


CURRENT: Dict[str, Optional[List[List[int]]]] = {
    "puzzle": None,
    "solution": None,
}


@bp.route("/")
def index() -> str:
    """Render the main Sudoku page."""
    return render_template("index.html")


@bp.route("/new")
def new_game():
    """Generate and return a new puzzle for the current session."""
    clues = int(request.args.get("clues", 35))
    puzzle, solution = generate_puzzle(clues)
    CURRENT["puzzle"] = puzzle
    CURRENT["solution"] = solution
    return jsonify({"puzzle": puzzle})


@bp.route("/check", methods=["POST"])
def check_solution():
    """Validate the submitted board against the current solution."""
    data = request.json
    board = data.get("board")
    solution = CURRENT.get("solution")
    if solution is None:
        return jsonify({"error": "No game in progress"}), 400

    incorrect = find_incorrect_cells(board, solution)
    return jsonify({"incorrect": incorrect})
