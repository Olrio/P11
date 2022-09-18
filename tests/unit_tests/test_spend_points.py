import pytest

from ..test_config import client


def test_spend_more_than_available_points_should_return_code_403(client):
    response = client.post('/purchasePlaces', data={"places": 10,
                                                    "club": "Iron Temple",
                                                    "competition": "Fall Classic"})
    assert response.status_code == 403


def test_spend_less_or_equal_than_available_points_should_return_code_200(client):
    response = client.post('/purchasePlaces', data={"places": 4,
                                                    "club": "Iron Temple",
                                                    "competition": "Fall Classic"})
    assert response.status_code == 200
