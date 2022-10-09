from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from P11.server import app, clubs, competitions
import datetime


class TestPlacesInput(LiveServerTestCase):
    def create_app(self):
        app.config.from_object("P11.tests.test_config")
        app.config['TESTING'] = True
        return app

    @classmethod
    def setUpClass(cls):
        cls.club = next(filter(lambda x: x['name'] == 'Simply Lift', clubs))
        cls.competition = next(filter(lambda x: x['name'] == 'Spring Festival', competitions))
        cls.competition['date'] = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=100),
                                                         "%Y-%m-%d %H:%M:%S")

    @classmethod
    def tearDownClass(cls):
        pass

    def test_enter_empty_entry_should_display_required_message(self):
        browser = webdriver.Firefox()
        browser.get(self.get_server_url() + url_for("book", competition=self.competition['name'], club=self.club['name']))
        places = browser.find_element(By.NAME, 'places')
        submit = browser.find_element(By.XPATH, '//button')
        submit.click()
        validation = places.get_attribute("validationMessage")
        assert validation == "Veuillez saisir un nombre."
