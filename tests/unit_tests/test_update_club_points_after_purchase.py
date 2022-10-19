import pytest
from flask_testing import TestCase
from ..test_config import client, get_clubs, get_competitions
from P11.server import app

@pytest.mark.usefixtures('get_clubs')
@pytest.mark.usefixtures('get_competitions')
class MyTest(TestCase):
    def create_app(self):
        app.config.from_object("P11.tests.test_config")
        return app

    def test_spending_x_points_should_remove_x_points_from_balance_points(self):
        club = next(item for item in self.app.config['P11'].server.clubs
                    if item["name"] == "Club Test 3")
        spent_points = 10
        final_club_points = int(club['points']) - spent_points
        response = self.client.post('/purchasePlaces', data={
            "places": spent_points,
            "club": club['name'],
            "competition": "Incoming Competition"})
        assert "Points available: "+str(final_club_points) in response.data.decode()
        assert int(club['points']) == final_club_points
