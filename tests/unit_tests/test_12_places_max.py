import pytest

from ..test_config import client

from P11.server import clubs, competitions



def setup_module(module):
    global club, initial_points, competition
    club = list(filter(lambda x: x['name'] == 'Simply Lift', clubs))[0]
    competition = list(filter(lambda x: x['name'] == 'Spring Festival', competitions))[0]
    initial_points = int(club["points"])


def teardown_module(module):
    club['points'] = str(initial_points)
    competition[club['name']] = 0



def test_spend_more_than_12_points_in_one_purchase_should_return_code_403(client):
    response = client.post('/purchasePlaces', data={"places": 13,
                                                    "club": "Simply Lift",
                                                    "competition": "Spring Festival"})
    assert response.status_code == 403


def test_spend_less_than_12_points_in_several_purchases_should_return_code_200(client):
    # club has bought no place yet. It's possible to buy 12 more places
    response = client.post('/purchasePlaces', data={"places": 7,
                                                    "club": "Simply Lift",
                                                    "competition": "Spring Festival"})
    assert response.status_code == 200


def test_spend_more_than_12_points_in_several_purchases_should_return_code_403(client):
    # club has already bought 7 places. It's possible to buy 5 more places
    response = client.post('/purchasePlaces', data={"places": 6,
                                                    "club": "Simply Lift",
                                                    "competition": "Spring Festival"})
    assert response.status_code == 403
