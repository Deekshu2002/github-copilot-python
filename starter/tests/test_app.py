import pytest

from app import app
from sudoku_blueprint import CURRENT
from sudoku_generator import count_solutions, generate_puzzle, get_clues_for_difficulty
from sudoku_validator import evaluate_board_state


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


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
    incorrect_board = [
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
