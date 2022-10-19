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

    def test_purchasing_more_places_than_available_in_competition_should_return_status_code_403(self):
        response = self.client.post('/purchasePlaces', data={"places": 12,
                                                             "club": "Club Test 1",
                                                             "competition": "Incoming Competition"})
        assert response.status_code == 403

    def test_purchasing_less_or_equal_places_than_available_in_competition_should_return_status_code_200(self):
        response = self.client.post('/purchasePlaces', data={
            "places": 5,
            "club": "Club Test 1",
            "competition": "Incoming Competition"})
        assert response.status_code == 200

    def test_purchasing_more_places_than_available_in_competition_should_return_flash_message(self):
        place_to_purchase = 12
        self.client.post('/purchasePlaces', data={"places": place_to_purchase,
                                                  "club": "Club Test 1",
                                                  "competition": "Incoming Competition"})
        competition = next(item for item in self.app.config['P11'].server.competitions
                           if item["name"] == "Incoming Competition")
        assert self.flashed_messages[0][0] == f"Sorry, only {competition['numberOfPlaces']} " \
                                              f"places left. You can't buy {place_to_purchase}."

    def test_purchasing_less_or_equal_places_than_available_in_competition_should_use_html_page_welcome(self):
        self.client.post('/purchasePlaces', data={"places": 10,
                                                  "club": "Club Test 1",
                                                  "competition": "Incoming Competition"})
        self.assert_template_used('welcome.html')

    def test_purchasing_more_places_than_available_in_competition_should_use_html_page_welcome(self):
        self.client.post('/purchasePlaces', data={"places": 12,
                                                  "club": "Club Test 1",
                                                  "competition": "Incoming Competition"})
        self.assert_template_used('welcome.html')
