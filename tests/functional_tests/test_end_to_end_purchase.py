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
        # Secretary of Club Test 3 wants to purchase 15 places in Competition 12
        # it's forbidden to buy more than 12 places
        # then secretary decides to purchase 12 places in Incoming Competition
        # there are only 11 places left in this competition
        # Secretary of Club Test 3 wants to purchase 5 places in Incoming Competition
        # then 7 places in Competition 12
        # there should be 3 points left
        # secretary tries to purchase 4 places. That's not possible
        # so secretary of Club Test 3 purchases 3 mores places in Competition 12
        browser = webdriver.Firefox()
        # loading login page
        browser.get(self.get_server_url() + url_for("index"))
        # login as secretary of Club Test 3
        browser.find_element(By.NAME, 'email').send_keys('mail3@myweb.com')
        browser.find_element(By.XPATH, '//button').click()
        # click on 'book places' for 'Competition 12'
        browser.find_element(By.XPATH, '//a[contains(@href, "Competition%2012")]').click()
        # try to purchase 15 places in 'Competition 12'
        browser.find_element(By.NAME, 'places').send_keys('15')
        browser.find_element(By.XPATH, '//button').click()
        validation = browser.find_element(By.XPATH, '//body/ul')
        assert validation.text == "Sorry, your total number of places can't exceed 12."
        # click on 'book places' for 'Incoming Competition'
        browser.find_element(By.XPATH, '//a[contains(@href, "Incoming")]').click()
        # purchase 12 places in 'Incoming Competition'
        browser.find_element(By.NAME, 'places').send_keys('12')
        browser.find_element(By.XPATH, '//button').click()
        validation = browser.find_element(By.XPATH, '//body/ul')
        assert validation.text == "Sorry, only 11 places left. You can't buy 12."
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
        available_points = browser.find_element(By.TAG_NAME, 'body').text.split('Points available: ')[1].split('\n')[0]
        assert available_points == "3"
        # click on 'book places' for 'Competition 12'
        browser.find_element(By.XPATH, '//a[contains(@href, "Competition%2012")]').click()
        # purchasing more places in 'Competition 12' than remaining points should not be possible
        browser.find_element(By.NAME, 'places').send_keys('4')
        browser.find_element(By.XPATH, '//button').click()
        validation = browser.find_element(By.XPATH, '//body/ul')
        assert validation.text == "Sorry, you just have 3 points.You can't buy 4 places."
        # click on 'book places' for 'Competition 12'
        browser.find_element(By.XPATH, '//a[contains(@href, "Competition%2012")]').click()
        # purchase 3 places in 'Competition 12'
        browser.find_element(By.NAME, 'places').send_keys('3')
        browser.find_element(By.XPATH, '//button').click()
        # let's verify that Club Test 3 has 0 point left and that purchase was successfull
        available_points = browser.find_element(By.TAG_NAME, 'body').text.split('Points available: ')[1].split('\n')[0]
        assert available_points == "0"
        validation = browser.find_element(By.XPATH, '//body/ul')
        assert validation.text == "Great-booking complete!"
