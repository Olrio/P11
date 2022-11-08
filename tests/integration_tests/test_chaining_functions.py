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

    def test_chaining_functions(self):
        # loading clubs and verify that Club Test 1 is actually loaded
        clubs_tests = app.config['P11'].server.clubs
        clubs_tests_names = [club['name'] for club in clubs_tests]
        clubs_tests_emails = [club['email'] for club in clubs_tests]
        assert 'Club Test 1' in clubs_tests_names
        assert 'mail1@myweb.com' in clubs_tests_emails
        club_test = [club for club in clubs_tests
                     if club['name'] == 'Club Test 1'][0]
        club_test_initial_points = int(club_test['points'])

        # loading competitions and verify that Incoming Competition is actually loaded
        competitions_tests = app.config['P11'].server.competitions
        competitions_tests_names = [competition['name'] for competition in competitions_tests]
        assert 'Incoming Competition' in competitions_tests_names
        competition_test = [competition for competition in competitions_tests
                            if competition['name'] == 'Incoming Competition'][0]
        competition_test_initial_available_places = int(competition_test['numberOfPlaces'])

        # opening index web page
        response = self.client.get('/')
        assert response.status_code == 200

        # logging as secretary of Club Test 1
        response = self.client.post('/showSummary', data={'email': 'mail1@myweb.com'})
        assert response.status_code == 200

        # consulting Incoming Competition
        response = self.client.get('book/Incoming Competition/Club Test 1')
        assert response.status_code == 200

        # purchasing 5 places in Incoming Competition
        places_purchased = 5
        response = self.client.post('/purchasePlaces', data={
            "places": places_purchased,
            "club": "Club Test 1",
            "competition": "Incoming Competition"})
        assert response.status_code == 200
        assert club_test['points'] == club_test_initial_points - places_purchased
        assert competition_test['numberOfPlaces'] == \
               competition_test_initial_available_places - places_purchased

        # consulting clubs points board
        self.client.get('/board')
        self.assert_template_used('board.html')

        # logout
        response = self.client.get('/logout')
        assert response.status_code == 302
        self.assertEqual(response.location, '/')
