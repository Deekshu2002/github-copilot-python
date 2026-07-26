import pytest

from app import app
from sudoku_generator import count_solutions, get_clues_for_difficulty


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
