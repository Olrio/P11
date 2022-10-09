from unittest.mock import patch
from P11.server import loadClubs


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
