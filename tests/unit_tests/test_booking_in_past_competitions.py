import pytest
import datetime

from ..test_config import client

from P11.server import clubs, competitions


def setup_module(module):
    global club, initial_points, competition, initial_date
    club = list(filter(lambda x: x['name'] == 'Simply Lift', clubs))[0]
    competition = list(filter(lambda x: x['name'] == 'Spring Festival', competitions))[0]
    initial_points = int(club["points"])
    initial_date = competition['date']


def teardown_module(module):
    club['points'] = str(initial_points)
    competition[club['name']] = 0
    competition['date'] = initial_date


def test_booking_places_in_a_past_competition_should_return_status_code_403(client):
    competition['date'] = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=100),
                                                          "%Y-%m-%d %H:%M:%S")
    spent_points = 1
    response = client.post('/purchasePlaces', data={"places": spent_points,
                                                    "club": club['name'],
                                                    "competition": competition['name']})
    assert response.status_code == 403

def test_booking_places_in_a_future_competition_should_return_status_code_200(client):
    competition['date'] = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=100),
                                                     "%Y-%m-%d %H:%M:%S")
    spent_points = 1
    response = client.post('/purchasePlaces', data={"places": spent_points,
                                                    "club": club['name'],
                                                    "competition": competition['name']})
    assert response.status_code == 200
