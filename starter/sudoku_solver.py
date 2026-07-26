"""Sudoku solving utilities."""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from sudoku_constants import EMPTY, SIZE


Board = List[List[int]]


def is_safe(board: Board, row: int, col: int, num: int) -> bool:
    """Return True when placing num at (row, col) would not violate Sudoku rules."""
    if board[row][col] != EMPTY:
        return False

    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def is_valid_row(board: Sequence[Sequence[int]], row: int) -> bool:
    """Return True when the row contains no duplicate values other than zero."""
    values = [value for value in board[row] if value != EMPTY]
    return len(values) == len(set(values))


def is_valid_column(board: Sequence[Sequence[int]], col: int) -> bool:
    """Return True when the column contains no duplicate values other than zero."""
    values = [board[row][col] for row in range(SIZE) if board[row][col] != EMPTY]
    return len(values) == len(set(values))


def is_valid_box(board: Sequence[Sequence[int]], row: int, col: int) -> bool:
    """Return True when the 3x3 box contains no duplicate values other than zero."""
    start_row = row - row % 3
    start_col = col - col % 3
    values = []
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] != EMPTY:
                values.append(board[i][j])
    return len(values) == len(set(values))


def _find_empty_cell(board: Board) -> Optional[Tuple[int, int]]:
    """Return the next empty cell location, if one exists."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return row, col
    return None


def solve_board(board: Board) -> bool:
    """Solve a Sudoku board in place using backtracking."""
    empty_cell = _find_empty_cell(board)
    if empty_cell is None:
        return True

    row, col = empty_cell
    for candidate in range(1, SIZE + 1):
        if is_safe(board, row, col, candidate):
            board[row][col] = candidate
            if solve_board(board):
                return True
            board[row][col] = EMPTY
    return False


def count_solutions(board: Board, limit: int = 2) -> int:
    """Count possible solutions up to a provided limit."""
    if not all(is_valid_row(board, row) for row in range(SIZE)):
        return 0
    if not all(is_valid_column(board, col) for col in range(SIZE)):
        return 0
    if not all(is_valid_box(board, row, col) for row in range(SIZE) for col in range(SIZE) if board[row][col] != EMPTY):
        return 0

    board_copy = [row[:] for row in board]
    solutions = 0

    def backtrack(current_board: Board) -> None:
        nonlocal solutions
        if solutions >= limit:
            return
        empty_cell = _find_empty_cell(current_board)
        if empty_cell is None:
            solutions += 1
            return

        row, col = empty_cell
        for candidate in range(1, SIZE + 1):
            if is_safe(current_board, row, col, candidate):
                current_board[row][col] = candidate
                backtrack(current_board)
                current_board[row][col] = EMPTY
                if solutions >= limit:
                    return

    backtrack(board_copy)
    return solutions
