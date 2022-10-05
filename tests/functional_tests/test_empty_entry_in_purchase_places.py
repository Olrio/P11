from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from P11.server import app, clubs, competitions


def setup_module():
    global club, competition, initial_points, places_left
    club = list(filter(lambda x: x['name'] == 'Simply Lift', clubs))[0]
    competition = list(filter(lambda x: x['name'] == 'Spring Festival', competitions))[0]
    competition['date'] = "2025-03-27 10:00:00"
    initial_points = int(club["points"])
    places_left = competition['numberOfPlaces']


def teardown_module():
    club['points'] = str(initial_points)
    competition['numberOfPlaces'] = places_left


class TestPlacesInput(LiveServerTestCase):
    def create_app(self):
        app.config.from_object("P11.tests.test_config")
        app.config['TESTING'] = True
        return app

    def test_enter_empty_entry_should_display_required_message(self):
        browser = webdriver.Firefox()
        browser.get(self.get_server_url() + url_for("book", competition=competition['name'], club=club['name']))
        places = browser.find_element(By.NAME, 'places')
        submit = browser.find_element(By.XPATH, '//button')
        submit.click()
        validation = places.get_attribute("validationMessage")
        assert validation == "Veuillez saisir un nombre."
