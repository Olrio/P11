import pytest

from ..test_config import client
from P11.server import clubs, competitions


def setup_module(module):
    global club, initial_points, competition
    club = list(filter(lambda x: x['name'] == 'Simply Lift', clubs))[0]
    competition = list(filter(lambda x: x['name'] == 'Fall Classic', competitions))[0]
    initial_points = int(club["points"])


def teardown_module(module):
    club['points'] = str(initial_points)


def test_purchasing_places_should_return_status_code_200(client):
    spent_points = 1
    response = client.post('/purchasePlaces', data={"places": spent_points,
                                                    "club": club['name'],
                                                    "competition": competition['name']})
    assert response.status_code == 200


def test_spending_x_points_should_remove_x_points_from_balance_points(client):
    spent_points = 10
    final_club_points = int(club['points']) - spent_points
    response = client.post('/purchasePlaces', data={"places": spent_points,
                                                    "club": club['name'],
                                                    "competition": competition['name']})
    assert "Points available: "+str(final_club_points) in response.data.decode()
