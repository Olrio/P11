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

    def test_buying_x_places_should_remove_x_places_to_number_of_available_places(self):
        competition = next(item for item in self.app.config['P11'].server.competitions
                           if item["name"] == "Incoming Competition")
        initial_available_places = int(competition['numberOfPlaces'])
        places_to_purchase = 10
        self.client.post('/purchasePlaces', data={
            "places": places_to_purchase,
            "club": "Club Test 3",
            "competition": competition['name']})
        assert competition['numberOfPlaces'] == initial_available_places - places_to_purchase
