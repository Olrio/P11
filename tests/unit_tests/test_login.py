import pytest
from ..test_config import client


def test_index_page_response_should_return_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_post_with_registered_email_should_return_response_200(client):
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200


def test_login_post_with_unknown_email_should_return_response_401(client):
    response = client.post('/showSummary', data={'email': 'bad@foo.com'})
    assert response.status_code == 401


def test_login_post_with_uncomplete_email_should_return_response_401(client):
    response = client.post('/showSummary', data={'email': 'badfoocom'})
    assert response.status_code == 401

