from ..test_config import client
from P11.server import app
from flask_testing import TestCase


class MyTest(TestCase):
    def create_app(self):
        app.config.from_object("P11.tests.test_config")
        return app

    def test_index_page_response_should_return_200(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_bad_index_page_response_should_return_404(self):
        response = self.client.get('bad')
        assert response.status_code == 404

    def test_index_route_should_use_html_index_page(self):
        self.client.get('/')
        self.assert_template_used('index.html')
