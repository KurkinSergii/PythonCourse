import requests

BASE_URL = "https://api.punkapi.com/"


def test_get_request():
    url = BASE_URL + "v2/beers/8"
    expected_status_code = 200
    expected_name = 'Fake Lager'
    expected_abv = 4.7
    response = requests.get(url)
    assert response.status_code == expected_status_code, \
        f"Status code from URL '{url}' is not {expected_status_code}"
    assert response.json()[0]['name'] == expected_name
    assert response.json()[0]['abv'] == expected_abv


def test_delete_request():
    url = BASE_URL + "v2/beers/8"
    expected_status_code = 404
    expected_message = "No endpoint found that matches '/v2/beers/8'"
    response = requests.delete(url)
    assert response.status_code == expected_status_code
    assert response.json()['message'] == expected_message