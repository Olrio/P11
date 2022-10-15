import pytest
from flask_testing import TestCase
from ..test_config import client, get_clubs
from P11.server import app


@pytest.mark.usefixtures('get_clubs')
class MyTest(TestCase):
    def create_app(self):
        app.config.from_object("P11.tests.test_config")
        return app

    def test_login_post_with_registered_email_should_return_response_200(self):
        with self.client:
            response = self.client.post('/showSummary', data={'email': 'mail1@myweb.com'})
            assert response.status_code == 200

    def test_login_post_with_unknown_email_should_return_response_401(self):
        with self.client:
            response = self.client.post('/showSummary', data={'email': 'badmail@foo.com'})
            assert response.status_code == 401

    def test_login_post_with_uncomplete_email_should_return_response_401(self):
        with self.client:
            response = self.client.post('/showSummary', data={'email': 'badfoocom'})
            assert response.status_code == 401

    def test_login_page_response_should_be_the_expected_html_page_welcome_with_succes_login(self):
        with self.client:
            self.client.post('/showSummary', data={'email': 'mail1@myweb.com'})
            self.assert_template_used('welcome.html')

    def test_login_page_response_should_be_the_expected_html_page_index_with_fail_login(self):
        with self.client:
            self.client.post('/showSummary', data={'email': 'badmail@foo.com'})
            self.assert_template_used('index.html')

