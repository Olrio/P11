import pytest
from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from P11.server import app
from ..test_config import client, get_clubs, get_competitions

@pytest.mark.usefixtures('get_clubs')
@pytest.mark.usefixtures('get_competitions')
class TestglobalPurchase(LiveServerTestCase):
    def create_app(self):
        app.config.from_object("P11.tests.test_config")
        app.config['TESTING'] = True
        return app

    def test_purchase_places(self):
        # Secretary of Club Test 3 wants to purchase 5 places in Incoming Competition
        # then 7 places in Competition 12
        # there should be 3 points left
        # so secretary of Club Test 3 purchase 8 mores places in Competition 12
        browser = webdriver.Firefox()
        # loading login page
        browser.get(self.get_server_url() + url_for("index"))
        # login as secretary of Club Test 3
        browser.find_element(By.NAME, 'email').send_keys('mail3@myweb.com')
        browser.find_element(By.XPATH, '//button').click()
        # click on 'book places' for 'Incoming Competition'
        browser.find_element(By.XPATH, '//a[contains(@href, "Incoming")]').click()
        # purchase 5 places in 'Incoming Competition'
        browser.find_element(By.NAME, 'places').send_keys('5')
        browser.find_element(By.XPATH, '//button').click()
        # click on 'book places' for 'Competition 12'
        browser.find_element(By.XPATH, '//a[contains(@href, "Competition%2012")]').click()
        # purchase 7 places in 'Competition 12'
        browser.find_element(By.NAME, 'places').send_keys('7')
        browser.find_element(By.XPATH, '//button').click()
        # let's verify that Club Test 3 has 3 points left
        available_points = browser.find_element(By.CSS_SELECTOR, 'body').text.find('Points available: 3')
        assert available_points != -1
        # click on 'book places' for 'Competition 12'
        browser.find_element(By.XPATH, '//a[contains(@href, "Competition%2012")]').click()
        # purchase 3 places in 'Competition 12'
        browser.find_element(By.NAME, 'places').send_keys('3')
        browser.find_element(By.XPATH, '//button').click()
        # let's verify that Club Test 3 has 0 point left
        available_points = browser.find_element(By.CSS_SELECTOR, 'body').text.find('Points available: 0')
        assert available_points != -1
        validation_message = browser.find_element(By.CSS_SELECTOR, 'body').text.find('Great-booking complete!')
        assert validation_message != -1
