"""Backward-compatible imports for the Sudoku modules."""

from __future__ import annotations

from sudoku_constants import EMPTY, SIZE
from sudoku_generator import create_empty_board, deep_copy, generate_puzzle, remove_cells
from sudoku_solver import (
    count_solutions,
    is_safe,
    is_valid_box,
    is_valid_column,
    is_valid_row,
    solve_board,
)
from sudoku_validator import find_incorrect_cells


def fill_board(board):
    """Backward-compatible wrapper for the old fill_board API."""
    return solve_board(board)


__all__ = [
    "EMPTY",
    "SIZE",
    "create_empty_board",
    "deep_copy",
    "fill_board",
    "find_incorrect_cells",
    "generate_puzzle",
    "is_safe",
    "is_valid_box",
    "is_valid_column",
    "is_valid_row",
    "remove_cells",
    "solve_board",
    "count_solutions",
]
