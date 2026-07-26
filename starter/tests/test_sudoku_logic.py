import pytest

from sudoku_logic import (
    SIZE,
    create_empty_board,
    deep_copy,
    fill_board,
    generate_puzzle,
    is_safe,
    is_valid_box,
    is_valid_column,
    is_valid_row,
    remove_cells,
    solve_board,
    count_solutions,
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


def test_is_valid_row_detects_duplicates():
    board = create_empty_board()
    board[0] = [1, 2, 3, 4, 5, 6, 7, 8, 1]
    assert is_valid_row(board, 0) is False
    assert is_valid_row(create_empty_board(), 0) is True


def test_is_valid_column_detects_duplicates():
    board = create_empty_board()
    board[0][0] = 1
    board[1][0] = 1
    assert is_valid_column(board, 0) is False
    assert is_valid_column(create_empty_board(), 0) is True


def test_is_valid_box_detects_duplicates():
    board = create_empty_board()
    board[0][0] = 1
    board[0][1] = 1
    assert is_valid_box(board, 0, 0) is False
    assert is_valid_box(create_empty_board(), 0, 0) is True


def test_solve_board_solves_a_known_puzzle():
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    assert solve_board(board) is True
    assert count_solutions(board, limit=2) == 1
    assert all(cell != 0 for row in board for cell in row)


def test_count_solutions_stops_early_for_multiple_solutions():
    board = create_empty_board()
    assert count_solutions(board, limit=2) == 2


def test_generated_puzzles_have_exactly_one_solution():
    for _ in range(5):
        puzzle, _ = generate_puzzle(clues=35)
        assert count_solutions(puzzle, limit=2) == 1
