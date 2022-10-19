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

    def test_spend_more_than_available_points_should_return_code_403(self):
        response = self.client.post('/purchasePlaces', data={
            "places": 10,
            "club": "Club Test 2",
            "competition": "Incoming Competition"})
        assert response.status_code == 403

    def test_spend_less_or_equal_than_available_points_should_return_code_200(self):
        response = self.client.post('/purchasePlaces', data={
            "places": 4,
            "club": "Club Test 2",
            "competition": "Incoming Competition"})
        assert response.status_code == 200

    def test_spend_more_than_available_points_should_return_flash_message(self):
        place_to_purchase = 10
        self.client.post('/purchasePlaces', data={
            "places": place_to_purchase,
            "club": "Club Test 2",
            "competition": "Incoming Competition"})
        club = next(item for item in self.app.config['P11'].server.clubs
                    if item["name"] == "Club Test 2")
        assert self.flashed_messages[0][0] == f"Sorry, you just have {club['points']} points." \
                                              f"You can't buy {place_to_purchase} places."

    def test_spend_more_than_available_points_should_use_html_page_welcome(self):
        self.client.post('/purchasePlaces', data={
            "places": 10,
            "club": "Club Test 2",
            "competition": "Incoming Competition"})
        self.assert_template_used('welcome.html')
