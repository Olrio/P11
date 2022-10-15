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

    def test_purchasing_places_with_incorrect_club_or_competition_should_return_status_code_403(self):
        with self.client:
            response = self.client.post('/purchasePlaces', data={"places": 10,
                                                                 "club": "bad club",
                                                                 "competition": "bad competition"})
            assert response.status_code == 403

    def test_purchasing_places_with_incorrect_club_or_competition_should_return_flash_message(self):
        with self.client:
            self.client.post('/purchasePlaces', data={"places": 10,
                                                      "club": "bad club",
                                                      "competition": "bad competition"})
            assert self.flashed_messages[0][0] == "Something went wrong-please try again"

    def test_purchasing_places_response_should_be_the_expected_html_page_welcome_with_incorrect_club_or_competition(self):
        with self.client:
            self.client.post('/purchasePlaces', data={"places": 10,
                                                      "club": "bad club",
                                                      "competition": "bad competition"})
            self.assert_template_used('welcome.html')
