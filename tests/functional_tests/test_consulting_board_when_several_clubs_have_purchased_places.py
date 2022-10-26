import pytest
from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from P11.server import app
from ..test_config import client, get_clubs, get_competitions

@pytest.mark.usefixtures('get_clubs')
@pytest.mark.usefixtures('get_competitions')
class TestglobalConsultingBoard(LiveServerTestCase):
    def create_app(self):
        app.config.from_object("P11.tests.test_config")
        app.config['TESTING'] = True
        return app

    def test_consulting_board(self):
        # secretary of Club Test 1 purchases 5 places in Incoming Competition
        # secretary of Club Test 2 purchases 3 places in Incoming Competition
        # secretary of Club Test 3 purchases 4 places in Competition 12
        # then someone want to consult board page
        # Balance points should be 8 points for Club Test 1, 1 point for Club Test 2
        # and 11 points for Club Test 3
        browser = webdriver.Firefox()
        # loading login page
        browser.get(self.get_server_url() + url_for("index"))
        # login as secretary of Club Test 1
        browser.find_element(By.NAME, 'email').send_keys('mail1@myweb.com')
        browser.find_element(By.XPATH, '//button').click()
        # click on 'book places' for 'Incoming Competition'
        browser.find_element(By.XPATH, '//a[contains(@href, "Incoming")]').click()
        # purchase 5 places in 'Incoming Competition'
        browser.find_element(By.NAME, 'places').send_keys('5')
        browser.find_element(By.XPATH, '//button').click()
        # secretary of Club Test 1 logout
        browser.find_element(By.XPATH, '//a[contains(@href, "logout")]').click()
        # login as secretary of Club Test 2
        browser.find_element(By.NAME, 'email').send_keys('mail2@myweb.com')
        browser.find_element(By.XPATH, '//button').click()
        # click on 'book places' for 'Incoming Competition'
        browser.find_element(By.XPATH, '//a[contains(@href, "Incoming")]').click()
        # purchase 3 places in 'Incoming Competition'
        browser.find_element(By.NAME, 'places').send_keys('3')
        browser.find_element(By.XPATH, '//button').click()
        # secretary of Club Test 2 logout
        browser.find_element(By.XPATH, '//a[contains(@href, "logout")]').click()
        # login as secretary of Club Test 3
        browser.find_element(By.NAME, 'email').send_keys('mail3@myweb.com')
        browser.find_element(By.XPATH, '//button').click()
        # click on 'book places' for 'Competition 12'
        browser.find_element(By.XPATH, '//a[contains(@href, "Competition%2012")]').click()
        # purchase 4 places in 'Competition 12'
        browser.find_element(By.NAME, 'places').send_keys('4')
        browser.find_element(By.XPATH, '//button').click()
        # secretary of Club Test 3 logout
        browser.find_element(By.XPATH, '//a[contains(@href, "logout")]').click()
        # someone loads login page
        browser.get(self.get_server_url() + url_for("index"))
        # someone click on Clubs points board link
        browser.find_element(By.XPATH, '//a[contains(@href, "board")]').click()
        # getting table rows and clubs points
        board_rows = browser.find_elements(By.XPATH, "//table/tbody/tr")
        row_club_test_1 = [c for c in board_rows if "Club Test 1" in c.text]
        row_club_test_2 = [c for c in board_rows if "Club Test 2" in c.text]
        row_club_test_3 = [c for c in board_rows if "Club Test 3" in c.text]
        club_test_1_points = row_club_test_1[0].text.split('Club Test 1 ')[1]
        club_test_2_points = row_club_test_2[0].text.split('Club Test 2 ')[1]
        club_test_3_points = row_club_test_3[0].text.split('Club Test 3 ')[1]
        # checking that Club Test 1 has 8 points remaining
        assert club_test_1_points == "8"
        # checking that Club Test 2 has 1 point remaining
        assert club_test_2_points == "1"
        # checking that Club Test 3 has 11 points remaining
        assert club_test_3_points == "11"
