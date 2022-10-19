from unittest.mock import patch
from P11.server import loadClubs, loadCompetitions


@patch("P11.server.json.load")
def test_loadclubs(mock_json_load):
    mock_json_load.return_value = dict({"clubs": [
        {
            "name": "Club Test 1",
            "email": "email@clubtest1.com",
            "points": "20"
        },
        {
            "name": "Club Test 2",
            "email": "email@clubtest2.com",
            "points": "10"
        }
    ]})
    assert isinstance(loadClubs(), list)
    for club in loadClubs():
        assert isinstance(club, dict)
    assert loadClubs()[0]['name'] == "Club Test 1"
    assert loadClubs()[1]['email'] == "email@clubtest2.com"


@patch("P11.server.json.load")
def test_loadcompetitions(mock_json_load):
    mock_json_load.return_value = dict({"competitions": [
        {
            "name": "First competition",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "3"
        },
        {
            "name": "Second competition",
            "date": "2025-03-27 15:00:00",
            "numberOfPlaces": "15"
        }
    ]})
    assert isinstance(loadCompetitions(), list)
    for competition in loadCompetitions():
        assert isinstance(competition, dict)
    assert loadCompetitions()[0]['name'] == "First competition"
    assert loadCompetitions()[1]['date'] == "2025-03-27 15:00:00"
