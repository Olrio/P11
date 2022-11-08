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

    def test_booking_places_with_incorrect_club_or_competition_should_return_status_code_403(self):
        response = self.client.get(f"/book/Past Competition2/Club Test 22")
        assert response.status_code == 403

    def test_booking_places_with_incorrect_club_or_competition_should_return_flash_message(self):
        self.client.get(f"/book/Past Competition2/Club Test 22")
        assert self.flashed_messages[0][0] == "Something went wrong-please try again"

    def test_booking_places_with_incorrect_club_or_competition_should_use_html_page_welcome_(self):
        self.client.get(f"/book/Past Competition2/Club Test 22")
        self.assert_template_used('welcome.html')
