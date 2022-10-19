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

    def test_buying_x_places_should_add_x_points_to_competitions_club_bought_places(self):
        club = next(item for item in self.app.config['P11'].server.clubs
                    if item["name"] == "Club Test 3")
        competition = next(item for item in self.app.config['P11'].server.competitions
                           if item["name"] == "Incoming Competition")
        initial_points = competition[club['name']]
        spent_points = 10
        self.client.post('/purchasePlaces', data={
            "places": spent_points,
            "club": club['name'],
            "competition": competition['name']})
        assert competition[club['name']] == initial_points + spent_points
