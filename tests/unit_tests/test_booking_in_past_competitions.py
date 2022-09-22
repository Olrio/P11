import pytest
import datetime

from ..test_config import client

from P11.server import clubs, competitions


def test_booking_places_in_a_past_competition_should_return_status_code_403(client):
    club = list(filter(lambda x: x['name'] == 'Simply Lift', clubs))[0]
    competition = list(filter(lambda x: x['name'] == 'Spring Festival', competitions))[0]
    competition['date'] = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=100),
                                                     "%Y-%m-%d %H:%M:%S")
    response = client.get(f"/book/{competition['name']}/{club['name']}", data={"club": club['name'],
                                                    "competition": competition['name']})
    assert response.status_code == 403


def test_booking_places_in_a_future_competition_should_return_status_code_200(client):
    club = list(filter(lambda x: x['name'] == 'Simply Lift', clubs))[0]
    competition = list(filter(lambda x: x['name'] == 'Spring Festival', competitions))[0]
    competition['date'] = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=100),
                                                     "%Y-%m-%d %H:%M:%S")
    response = client.get(f"/book/{competition['name']}/{club['name']}", data={"club": club['name'],
                                                    "competition": competition['name']})
    assert response.status_code == 200
