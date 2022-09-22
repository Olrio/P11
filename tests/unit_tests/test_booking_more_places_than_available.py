import pytest

from ..test_config import client

from P11.server import clubs, competitions

def setup_module(module):
    global club, initial_points, competition
    club = list(filter(lambda x: x['name'] == 'Simply Lift', clubs))[0]
    competition = list(filter(lambda x: x['name'] == 'Spring Festival', competitions))[0]
    competition['numberOfPlaces'] = 5
    initial_points = int(club["points"])


def teardown_module(module):
    club['points'] = str(initial_points)


def test_booking_more_places_than_available_in_competition_should_return_status_code_403(client):
    response = client.post('/purchasePlaces', data={"places": 10,
                                                    "club": club['name'],
                                                    "competition": competition['name']})
    assert response.status_code == 403


def test_booking_less_or_equal_places_than_available_in_competition_should_return_status_code_200(client):
    response = client.post('/purchasePlaces', data={"places": 3,
                                                    "club": club['name'],
                                                    "competition": competition['name']})
    assert response.status_code == 200
