from unittest.mock import patch
from ..test_config import client


def simulate_index_render_template():
    return "This is index HTML page"

def test_index_page_response_should_return_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_bad_index_page_response_should_return_404(client):
    response = client.get('bad')
    assert response.status_code == 404


def test_index_page_response_should_be_the_expected_html_page(mocker, client):
    mocker.patch('flask.app.Flask.dispatch_request', return_value=simulate_index_render_template())
    response = client.get('/')
    expected_value = simulate_index_render_template()
    assert response.data.decode() == expected_value
