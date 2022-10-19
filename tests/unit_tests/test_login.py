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
        response = self.client.post('/showSummary', data={'email': 'mail1@myweb.com'})
        assert response.status_code == 200

    def test_login_post_with_unknown_email_should_return_response_401(self):
        response = self.client.post('/showSummary', data={'email': 'badmail@foo.com'})
        assert response.status_code == 401

    def test_login_post_with_uncomplete_email_should_return_response_401(self):
        response = self.client.post('/showSummary', data={'email': 'badfoocom'})
        assert response.status_code == 401

    def test_login_with_bad_or_uncompleted_mail_should_return_flash_message(self):
        self.client.post('/showSummary', data={'email': 'badfoocom'})
        assert "Sorry, email badfoocom is not associated with a club" in self.flashed_messages[0][0]

    def test_succes_login_should_use_html_page_welcome(self):
        self.client.post('/showSummary', data={'email': 'mail1@myweb.com'})
        self.assert_template_used('welcome.html')

    def test_fail_login_should_use_html_page_index(self):
        self.client.post('/showSummary', data={'email': 'badmail@foo.com'})
        self.assert_template_used('index.html')
