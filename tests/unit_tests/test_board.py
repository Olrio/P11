from ..test_config import client
from P11.server import app
from flask_testing import TestCase


class MyTest(TestCase):
    def create_app(self):
        app.config.from_object("P11.tests.test_config")
        return app

    def test_board_page_response_should_return_200(self):
        response = self.client.get('/board')
        assert response.status_code == 200

    def test_asking_for_current_clubs_points_balance_should_use_html_page_board(self):
        self.client.get('/board')
        self.assert_template_used('board.html')
