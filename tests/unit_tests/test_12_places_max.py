import pytest

from ..test_config import client

def test_spend_more_than_12_points_should_return_code_403(client):
    response = client.post('/purchasePlaces', data={"places": 13,
                                                    "club": "Simply Lift",
                                                    "competition": "Spring Festival"})
    assert response.status_code == 403