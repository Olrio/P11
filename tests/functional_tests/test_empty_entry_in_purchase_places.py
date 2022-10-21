import pytest
from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from P11.server import app
from ..test_config import client, get_clubs, get_competitions


@pytest.mark.usefixtures('get_clubs')
@pytest.mark.usefixtures('get_competitions')
class TestPlacesInput(LiveServerTestCase):
    def create_app(self):
        app.config.from_object("P11.tests.test_config")
        app.config['TESTING'] = True
        return app

    def test_enter_empty_entry_should_display_required_message(self):
        competition = next(item for item in self.app.config['P11'].server.competitions
                           if item["name"] == "Incoming Competition")
        club = next(item for item in self.app.config['P11'].server.clubs if item["name"] == "Club Test 3")
        browser = webdriver.Firefox()
        browser.get(self.get_server_url() + url_for("book", competition=competition['name'], club=club['name']))
        places = browser.find_element(By.NAME, 'places')
        submit = browser.find_element(By.XPATH, '//button')
        submit.click()
        validation = places.get_attribute("validationMessage")
        assert validation == "Veuillez saisir un nombre."
