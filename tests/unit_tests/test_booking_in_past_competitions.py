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

    def test_booking_places_in_a_past_competition_should_return_status_code_403(self):
        response = self.client.get(f"/book/Past Competition/Club Test 2")
        assert response.status_code == 403

    def test_booking_places_in_a_past_competition_mail_should_return_flash_message(self):
        self.client.get(f"/book/Past Competition/Club Test 2")
        assert "Sorry, the competition Past Competition is finished" in self.flashed_messages[0][0]

    def test_booking_places_in_an_incoming_competition_should_return_status_code_200(self):
        response = self.client.get(f"/book/Incoming Competition/Club Test 2")
        assert response.status_code == 200

    def test_booking_places_in_incoming_competition_should_use_html_page_booking(self):
        self.client.get(f"/book/Incoming Competition/Club Test 2")
        self.assert_template_used('booking.html')

    def test_booking_places_in_past_competition_should_use_html_page_welcome(self):
        self.client.get(f"/book/Past Competition/Club Test 2")
        self.assert_template_used('welcome.html')
