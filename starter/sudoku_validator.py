"""Validation helpers for Sudoku boards."""

from __future__ import annotations

from typing import List, Sequence, Tuple

from sudoku_constants import SIZE

Board = List[List[int]]


def find_incorrect_cells(board: Sequence[Sequence[int]], solution: Sequence[Sequence[int]]) -> List[List[int]]:
    """Return a list of coordinates that differ from the solved board."""
    incorrect: List[List[int]] = []
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return incorrect
