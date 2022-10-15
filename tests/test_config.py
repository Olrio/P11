import pytest
import datetime
import P11.server
from ..server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def get_clubs(mocker):
    clubs = mocker.patch.object(P11.server, "clubs", [
        {
            "name": "Club Test 1",
            "email": "mail1@myweb.com",
            "points": "13"
        },
        {
            "name": "Club Test 2",
            "email": "mail2@myweb.com",
            "points": "4"
        },
        {"name": "Club Test 3",
         "email": "mail3@myweb.com",
         "points": "12"
         }
    ])
    return clubs

@pytest.fixture
def get_competitions(mocker):
    competitions = mocker.patch.object(P11.server, "competitions", [
        {
            "name": "Past Competition",
            "date": datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=100),
                                                     "%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "25"
        },
        {
            "name": "Incoming Competition",
            "date": datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=100),
                                                     "%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "13"
        }
    ])
    return competitions
