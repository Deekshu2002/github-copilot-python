"""Puzzle generation helpers for the Sudoku game."""

from __future__ import annotations

import copy
import random
from typing import List, Tuple

from sudoku_constants import EMPTY, SIZE
from sudoku_solver import count_solutions, solve_board

Board = List[List[int]]


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


def generate_puzzle(clues: int = 35) -> Tuple[Board, Board]:
    """Generate a new Sudoku puzzle and its solved board."""
    board = create_empty_board()
    solved = solve_board(board)
    if not solved:
        raise ValueError("Unable to generate a valid Sudoku board")
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution
