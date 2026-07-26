import pytest

from sudoku_logic import (
    SIZE,
    create_empty_board,
    deep_copy,
    fill_board,
    generate_puzzle,
    is_safe,
    remove_cells,
)


def test_create_empty_board_has_expected_size():
    board = create_empty_board()
    assert len(board) == SIZE
    assert all(len(row) == SIZE for row in board)
    assert all(cell == 0 for row in board for cell in row)


def test_deep_copy_returns_independent_board():
    board = create_empty_board()
    board[0][0] = 5
    copied = deep_copy(board)

    copied[0][0] = 1
    assert board[0][0] == 5


def test_is_safe_rejects_conflicts_in_row_column_and_box():
    board = create_empty_board()
    board[0][0] = 1
    board[0][1] = 2
    assert is_safe(board, 0, 2, 3) is True
    assert is_safe(board, 0, 0, 1) is False
    assert is_safe(board, 1, 0, 1) is False
    assert is_safe(board, 0, 2, 2) is False


def test_fill_board_solves_empty_board():
    board = create_empty_board()
    assert fill_board(board) is True
    assert all(1 <= cell <= SIZE for row in board for cell in row)


def test_remove_cells_reduces_clue_count():
    board = create_empty_board()
    fill_board(board)
    original_clues = sum(cell != 0 for row in board for cell in row)

    remove_cells(board, clues=35)
    remaining_clues = sum(cell != 0 for row in board for cell in row)

    assert remaining_clues <= original_clues


def test_generate_puzzle_returns_puzzle_and_solution():
    puzzle, solution = generate_puzzle(clues=35)

    assert len(puzzle) == SIZE
    assert len(solution) == SIZE
    assert all(len(row) == SIZE for row in puzzle)
    assert all(len(row) == SIZE for row in solution)
    assert puzzle != solution
