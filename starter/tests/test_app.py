import pytest

from app import app
from sudoku_blueprint import CURRENT
from sudoku_generator import count_solutions, create_empty_board, generate_puzzle, get_clues_for_difficulty
from sudoku_solver import is_safe, solve_board
from sudoku_validator import evaluate_board_state, find_incorrect_cells


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_game_state():
    CURRENT["puzzle"] = None
    CURRENT["solution"] = None
    CURRENT["hints_used"] = 0
    yield
    CURRENT["puzzle"] = None
    CURRENT["solution"] = None
    CURRENT["hints_used"] = 0


def test_home_page_loads_successfully(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data


@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
def test_difficulty_endpoints_generate_uniquely_solved_puzzles(client, difficulty):
    response = client.get(f'/new?difficulty={difficulty}')

    assert response.status_code == 200
    data = response.get_json()
    assert data["difficulty"] == difficulty
    assert count_solutions(data["puzzle"], limit=2) == 1


def test_unknown_difficulty_defaults_to_easy(client):
    response = client.get('/new?difficulty=unknown')

    assert response.status_code == 200
    data = response.get_json()
    assert data["difficulty"] == "unknown"
    assert count_solutions(data["puzzle"], limit=2) == 1


def test_new_game_resets_hint_count(client):
    response = client.get('/new?difficulty=medium')

    assert response.status_code == 200
    data = response.get_json()
    assert data["hints_used"] == 0
    assert CURRENT["hints_used"] == 0


def test_generate_puzzle_returns_a_unique_solution_with_expected_shape():
    puzzle, solution = generate_puzzle(clues=40, difficulty="easy")

    assert len(puzzle) == 9
    assert len(solution) == 9
    clue_count = sum(cell != 0 for row in puzzle for cell in row)
    assert 24 <= clue_count < 81
    assert count_solutions(puzzle, limit=2) == 1
    assert count_solutions(solution, limit=2) == 1
    assert puzzle != solution


def test_is_safe_detects_conflicts_in_rows_columns_and_boxes():
    board = create_empty_board()
    board[0][0] = 1

    assert is_safe(board, 0, 1, 1) is False
    assert is_safe(board, 1, 0, 1) is False
    assert is_safe(board, 2, 2, 1) is False
    assert is_safe(board, 0, 1, 2) is True


def test_solve_board_solves_a_partially_filled_board():
    solved_board = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ]
    puzzle = [row[:] for row in solved_board]
    puzzle[0][0] = 0

    assert solve_board(puzzle) is True
    assert puzzle == solved_board


def test_count_solutions_returns_zero_for_invalid_board():
    invalid_board = create_empty_board()
    invalid_board[0][0] = 1
    invalid_board[0][1] = 1

    assert count_solutions(invalid_board, limit=2) == 0


def test_find_incorrect_cells_reports_board_differences():
    solution = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ]
    board = [row[:] for row in solution]
    board[0][0] = 2

    assert find_incorrect_cells(board, solution) == [[0, 0]]


def test_get_clues_for_difficulty_uses_expected_values():
    assert get_clues_for_difficulty("easy") == 40
    assert get_clues_for_difficulty("medium") == 32
    assert get_clues_for_difficulty("hard") == 24
    assert get_clues_for_difficulty("unknown") == 40


def test_check_endpoint_reports_incomplete_board(client):
    response = client.get('/new?difficulty=easy')
    puzzle = response.get_json()['puzzle']
    incomplete_board = [row[:] for row in puzzle]
    incomplete_board[0][0] = 0

    response = client.post('/check', json={'board': incomplete_board})
    assert response.status_code == 200
    assert response.get_json()['status'] == 'incomplete'


def test_check_endpoint_reports_incorrect_board(client):
    solution = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ]
    CURRENT['solution'] = solution
    CURRENT['puzzle'] = solution
    incorrect_board = [row[:] for row in solution]
    incorrect_board[0][0] = 2

    response = client.post('/check', json={'board': incorrect_board})
    assert response.status_code == 200
    assert response.get_json()['status'] == 'incorrect'


def test_check_endpoint_reports_complete_board(client):
    _, solution = generate_puzzle(clues=40)
    CURRENT["solution"] = solution
    CURRENT["puzzle"] = solution

    response = client.post('/check', json={'board': solution})
    assert response.status_code == 200
    assert response.get_json()['status'] == 'complete'


def test_hint_endpoint_fills_one_empty_editable_cell(client):
    response = client.get('/new?difficulty=easy')
    puzzle = response.get_json()['puzzle']
    board = [row[:] for row in puzzle]

    response = client.post('/hint', json={'board': board})
    data = response.get_json()

    assert response.status_code == 200
    assert data['hints_used'] == 1
    assert data['position'] is not None
    row, col = data['position']
    assert puzzle[row][col] == 0
    assert data['board'][row][col] == CURRENT['solution'][row][col]


def test_hint_endpoint_is_noop_for_complete_board(client):
    _, solution = generate_puzzle(clues=40)
    CURRENT['solution'] = solution
    CURRENT['puzzle'] = solution
    CURRENT['hints_used'] = 0

    response = client.post('/hint', json={'board': solution})
    data = response.get_json()

    assert response.status_code == 200
    assert data['hints_used'] == 0
    assert data['position'] is None
    assert data['board'] == solution


def test_check_endpoint_returns_error_when_no_game_in_progress(client):
    CURRENT['solution'] = None
    CURRENT['puzzle'] = None

    response = client.post('/check', json={'board': create_empty_board()})

    assert response.status_code == 400
    assert response.get_json()['error'] == 'No game in progress'


def test_hint_endpoint_returns_error_when_no_game_in_progress(client):
    CURRENT['solution'] = None
    CURRENT['puzzle'] = None

    response = client.post('/hint', json={'board': create_empty_board()})

    assert response.status_code == 400
    assert response.get_json()['error'] == 'No game in progress'


def test_evaluate_board_state_helper():
    solution = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ]
    incomplete_board = [row[:] for row in solution]
    incomplete_board[0][0] = 0
    incorrect_board = [row[:] for row in solution]
    incorrect_board[0][0] = 2

    assert evaluate_board_state(incomplete_board, solution) == 'incomplete'
    assert evaluate_board_state(incorrect_board, solution) == 'incorrect'
    assert evaluate_board_state(solution, solution) == 'complete'
