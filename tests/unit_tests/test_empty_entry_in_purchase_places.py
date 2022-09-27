import pytest

from ..test_config import client

from P11.server import clubs, competitions

def setup_module(module):
    global club, initial_points, competition, places_left
    club = list(filter(lambda x: x['name'] == 'Simply Lift', clubs))[0]
    competition = list(filter(lambda x: x['name'] == 'Spring Festival', competitions))[0]
    competition['numberOfPlaces'] = 5
    initial_points = int(club["points"])
    places_left = competition['numberOfPlaces']


def teardown_module(module):
    club['points'] = str(initial_points)
    competition['numberOfPlaces'] = places_left


def test_enter_empty_entry_should_return_status_code_403(client):
    response = client.post('/purchasePlaces', data={"places": "",
                                                    "club": club['name'],
                                                    "competition": competition['name']})
    assert response.status_code == 403
