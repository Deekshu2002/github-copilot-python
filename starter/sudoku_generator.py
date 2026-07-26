"""Puzzle generation helpers for the Sudoku game."""

from __future__ import annotations

import copy
import random
from typing import List, Tuple

from sudoku_constants import EMPTY, SIZE
from sudoku_solver import count_solutions, solve_board

Board = List[List[int]]

DIFFICULTY_CLUES = {
    "easy": 40,
    "medium": 32,
    "hard": 24,
}


def create_empty_board() -> Board:
    """Create a blank Sudoku board filled with empty cells."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def deep_copy(board: Board) -> Board:
    """Return a deep copy of the board."""
    return copy.deepcopy(board)


def remove_cells(board: Board, clues: int) -> None:
    """Remove cells one at a time while preserving a unique solution."""
    attempts = SIZE * SIZE - clues
    remaining_cells = SIZE * SIZE
    while attempts > 0 and remaining_cells > clues:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] == EMPTY:
            continue

        original_value = board[row][col]
        board[row][col] = EMPTY
        remaining_cells -= 1

        if count_solutions(board, limit=2) != 1:
            board[row][col] = original_value
            remaining_cells += 1
            attempts -= 1
            continue

        attempts -= 1


def get_clues_for_difficulty(difficulty: str) -> int:
    """Return the clue count for a supported difficulty label."""
    normalized = (difficulty or "easy").strip().lower()
    return DIFFICULTY_CLUES.get(normalized, DIFFICULTY_CLUES["easy"])


def generate_puzzle(clues: int = 35, difficulty: str = "easy") -> Tuple[Board, Board]:
    """Generate a new Sudoku puzzle and its solved board."""
    board = create_empty_board()
    solved = solve_board(board)
    if not solved:
        raise ValueError("Unable to generate a valid Sudoku board")
    solution = deep_copy(board)

    clue_count = clues if clues != 35 else get_clues_for_difficulty(difficulty)
    remove_cells(board, clue_count)
    puzzle = deep_copy(board)
    return puzzle, solution
