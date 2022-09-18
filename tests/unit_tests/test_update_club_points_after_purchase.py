import pytest

from ..test_config import client
from P11.server import clubs


club = None
initial_points = None


def setup_function(function):
    global club, initial_points
    club = list(filter(lambda x: x['name'] == 'Iron Temple', clubs))[0]
    initial_points = int(club["points"])


def teardown_function(function):
    pass


def test_purchasing_places_should_return_status_code_200(client):
    spent_points = 1
    response = client.post('/purchasePlaces', data={"places": spent_points,
                                                    "club": club['name'],
                                                    "competition": "Fall Classic"})
    assert response.status_code == 200


def test_spending_x_points_should_remove_x_points_from_balance_points(client):
    spent_points = 10
    response = client.post('/purchasePlaces', data={"places": spent_points,
                                                    "club": club['name'],
                                                    "competition": "Fall Classic"})
    assert "Points available: "+str(initial_points - spent_points) in response.data.decode()
