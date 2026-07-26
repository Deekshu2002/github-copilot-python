"""Validation helpers for Sudoku boards."""

from __future__ import annotations

from typing import List, Sequence

from sudoku_constants import EMPTY, SIZE

Board = List[List[int]]


def find_incorrect_cells(board: Sequence[Sequence[int]], solution: Sequence[Sequence[int]]) -> List[List[int]]:
    """Return a list of coordinates that differ from the solved board."""
    incorrect: List[List[int]] = []
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return incorrect


def evaluate_board_state(board: Sequence[Sequence[int]], solution: Sequence[Sequence[int]]) -> str:
    """Return whether the submitted board is incomplete, incorrect, or complete."""
    if any(cell == EMPTY for row in board for cell in row):
        return "incomplete"

    if find_incorrect_cells(board, solution):
        return "incorrect"

    return "complete"
