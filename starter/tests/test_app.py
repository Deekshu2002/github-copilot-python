import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page_loads_successfully(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data
