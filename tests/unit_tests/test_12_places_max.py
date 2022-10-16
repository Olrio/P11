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

    def test_purchasing_more_than_12_places_once_should_return_code_403(self):
        with self.client:
            response = self.client.post('/purchasePlaces', data={
                "places": 13,
                "club": "Club Test 3",
                "competition": "Competition 12"})
            assert response.status_code == 403

    def test_purchasing_no_more_than_12_places_in_several_purchases_should_return_code_200(self):
        with self.client:
            self.client.post('/purchasePlaces', data={
                "places": 7,
                "club": "Club Test 3",
                "competition": "Competition 12"})
            response = self.client.post('/purchasePlaces', data={
                "places": 5,
                "club": "Club Test 3",
                "competition": "Competition 12"})
            assert response.status_code == 200

    def test_purchasing_more_than_12_places_in_several_purchases_should_return_code_403(self):
        with self.client:
            self.client.post('/purchasePlaces', data={
                "places": 7,
                "club": "Club Test 3",
                "competition": "Competition 12"})
            response = self.client.post('/purchasePlaces', data={
                "places": 8,
                "club": "Club Test 3",
                "competition": "Competition 12"})
            assert response.status_code == 403

    def test_purchasing_more_than_12_places_should_return_flash_message(self):
        with self.client:
            self.client.post('/purchasePlaces', data={
                "places": 7,
                "club": "Club Test 3",
                "competition": "Competition 12"})
            self.client.post('/purchasePlaces', data={
                "places": 8,
                "club": "Club Test 3",
                "competition": "Competition 12"})
            assert self.flashed_messages[0][0] == "Great-booking complete!"
            assert self.flashed_messages[1][0] == "Sorry, your total number of places can't exceed 12."

    def test_purchasing_more_than_12_places_response_should_be_the_expected_html_page_welcome(self):
        with self.client:
            self.client.post('/purchasePlaces', data={
                "places": 13,
                "club": "Club Test 3",
                "competition": "Competition 12"})
            self.assert_template_used('welcome.html')

    def test_purchasing_no_more_than_12_places_response_should_be_the_expected_html_page_welcome(self):
        with self.client:
            self.client.post('/purchasePlaces', data={
                "places": 8,
                "club": "Club Test 3",
                "competition": "Competition 12"})
            self.assert_template_used('welcome.html')
