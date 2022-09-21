import pytest

from ..test_config import client
from P11.server import clubs, competitions


def setup_module(module):
    global club, initial_points, competition
    club = list(filter(lambda x: x['name'] == 'Iron Temple', clubs))[0]
    competition = list(filter(lambda x: x['name'] == 'Fall Classic', competitions))[0]
    initial_points = int(club["points"])


def teardown_module(module):
    club['points'] = str(initial_points)




def test_spend_more_than_available_points_should_return_code_403(client):
    response = client.post('/purchasePlaces', data={"places": 10,
                                                    "club": club['name'],
                                                    "competition": competition['name']})
    assert response.status_code == 403


def test_spend_less_or_equal_than_available_points_should_return_code_200(client):
    response = client.post('/purchasePlaces', data={"places": 4,
                                                    "club": club['name'],
                                                    "competition": competition['name']})
    assert response.status_code == 200
