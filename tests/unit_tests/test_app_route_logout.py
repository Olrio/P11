from ..test_config import client
from P11.server import app
from flask_testing import TestCase


class MyTest(TestCase):
    def create_app(self):
        app.config.from_object("P11.tests.test_config")
        return app

    def test_logout_page_response_should_return_302(self):
        response = self.client.get('/logout')
        assert response.status_code == 302

    def test_bad_logout_page_response_should_return_404(self):
        response = self.client.get('bad')
        assert response.status_code == 404

    def test_logout_route_should_redirect_to_html_index_page(self):
        response = self.client.get('/logout')
        self.assertEqual(response.location, '/')
