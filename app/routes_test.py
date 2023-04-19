import json
import re
from unittest.mock import patch

from flask import url_for
import requests_mock
from werkzeug.security import generate_password_hash
from app import app, db, Users
import pytest

from app.models import ChecklistItems
from app.routes import add_checklist_items, get_page_token


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection during testing

    with app.test_client() as client, app.app_context():
        db.create_all()
        yield client
        db.session.remove()


def test_home_page_displayed(test_client):
    response = test_client.get('/index')
    assert response.status_code == 200
    assert b'<h1>Welcome To Own My Home</h1>' in response.data


def test_checklist_page_displayed(test_client):
    # Create a test user in the database
    hashed_password = generate_password_hash('test_password', "sha256")
    test_user = Users(first_name='Test2', last_name='User2', email='testuser2@example.com', password_hash=hashed_password)
    db.session.add(test_user)
    db.session.commit()

    # simulate logging in with the test user's credentials
    response = test_client.post('/login', data=dict(
        email='testuser2@example.com',
        password_hash='test_password'
    ), follow_redirects=True)

    # assert that the login was successful and redirected to the home page
    assert response.status_code == 200

    response = test_client.get('/checklist')
    assert response.status_code == 200
    assert b'<h1 class="completed-header">Completed</h1>' in response.data

    # Clean up the test user
    db.session.delete(test_user)
    db.session.commit()


def test_sign_up_form_displayed(test_client):
    response = test_client.get('/sign-up')
    assert response.status_code == 200
    assert b'<h1 id="title">Sign Up</h1>' in response.data


def test_services_page_displayed(test_client):
    response = test_client.get('/services')
    assert response.status_code == 200
    assert b'<h2>Search for Home Buying Services</h2>' in response.data


def test_services_post(test_client):
    response = test_client.post('/services')
    assert response.status_code == 302
    assert response.location.endswith(url_for('index'))


def test_login_page_displayed(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'<h1 id="title">Login</h1>' in response.data


def test_sign_up(test_client):
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'confirm_email': 'johndoe@example.com',
        'password_hash': 'password',
        'confirm_password_hash': 'password',
        'accept_tos': True
    }

    response = test_client.post('/sign-up', data=data, follow_redirects=True)

    assert response.status_code == 200


def test_successful_login(test_client):
    # create a test user in the database
    hashed_password = generate_password_hash('test_password', "sha256")
    test_user = Users(first_name='Test', last_name='User', email='testuser@example.com', password_hash=hashed_password)
    db.session.add(test_user)
    db.session.commit()

    # simulate logging in with the test user's credentials
    response = test_client.post('/login', data=dict(
        email='testuser@example.com',
        password_hash='test_password'
    ), follow_redirects=True)

    # assert that the login was successful and redirected to the home page
    assert response.status_code == 200
    db.session.delete(test_user)
    db.session.commit()


def test_incorrect_email_login(test_client):
    # Simulate logging in with incorrect email
    response = test_client.post('/login', data=dict(
        email='incorrectemail@example.com',
        password='test_password'
    ), follow_redirects=True)

    # Assert that the response is OK (status code 200)
    assert response.status_code == 200


def test_checklist_items_added(test_client):
    # Create a test user in the database
    hashed_password = generate_password_hash('test_password', "sha256")
    test_user = Users(first_name='Test2', last_name='User2', email='testuser2@example.com',
                      password_hash=hashed_password)
    db.session.add(test_user)
    db.session.commit()

    # Call the function to create the checklist items for the test user
    add_checklist_items(test_user.id)

    # simulate logging in with the test user's credentials
    response = test_client.post('/login', data=dict(
        email='testuser2@example.com',
        password_hash='test_password'
    ), follow_redirects=True)

    # assert that the login was successful and redirected to the home page
    assert response.status_code == 200
    # Check if the checklist items are added to the database
    items = ChecklistItems.query.filter_by(user_id=test_user.id).order_by(ChecklistItems.order_no).all()
    assert len(items) == 5
    # Clean up the checklist items for the test user
    ChecklistItems.query.filter_by(user_id=test_user.id).delete()
    db.session.commit()
    # Clean up the test user
    db.session.delete(test_user)
    db.session.commit()


def test_checklist_items_fetched(test_client):
    # Create a test user in the database
    hashed_password = generate_password_hash('test_password', "sha256")
    test_user = Users(first_name='Test2', last_name='User2', email='testuser2@example.com',
                      password_hash=hashed_password)
    db.session.add(test_user)
    db.session.commit()

    # Add test checklist items to the database
    add_checklist_items(test_user.id)

    # Log in as the test user
    test_client.post('/login', data=dict(
        email='testuser2@example.com',
        password_hash='test_password'
    ), follow_redirects=True)

    # Check if the checklist items are fetched
    response = test_client.get('/checklist')
    assert response.status_code == 200
    for item in ChecklistItems.query.filter_by(user_id=test_user.id).all():
        assert item.detail.encode() in response.data

    # Clean up the checklist items for the test user
    ChecklistItems.query.filter_by(user_id=test_user.id).delete()
    db.session.commit()

    # Clean up the test user
    db.session.delete(test_user)
    db.session.commit()


def test_checklist_item_update(test_client):
    # Create a test user in the database
    hashed_password = generate_password_hash('test_password', "sha256")
    test_user = Users(first_name='Test2', last_name='User2', email='testuser2@example.com',
                      password_hash=hashed_password)
    db.session.add(test_user)
    db.session.commit()

    # Add test checklist items to the database
    add_checklist_items(test_user.id)

    # Log in as the test user
    test_client.post('/login', data=dict(
        email='testuser2@example.com',
        password_hash='test_password'
    ), follow_redirects=True)

    # Update the status of a checklist item
    item = ChecklistItems.query.filter_by(user_id=test_user.id, order_no=1).first()
    response = test_client.post('/checklist', json={'order_no': 1, 'status': True})
    assert response.status_code == 200
    assert response.json == {'success': True}
    item = ChecklistItems.query.filter_by(user_id=test_user.id, order_no=1).first()
    assert item.status is True

    # Clean up the checklist items for the test user
    ChecklistItems.query.filter_by(user_id=test_user.id).delete()
    db.session.commit()

    # Clean up the test user
    db.session.delete(test_user)
    db.session.commit()


def test_checklist_redirect(test_client):
    # Create a test user in the database
    hashed_password = generate_password_hash('test_password', "sha256")
    test_user = Users(first_name='Test2', last_name='User2', email='testuser2@example.com',
                      password_hash=hashed_password)
    db.session.add(test_user)
    db.session.commit()

    # Log in as the test user
    test_client.post('/login', data=dict(
        email='testuser2@example.com',
        password_hash='test_password'
    ), follow_redirects=True)

    # Send a non-GET, non-POST request to the `/checklist` route and check if it returns a 405 Method Not Allowed status
    response = test_client.put('/checklist')
    assert response.status_code == 405

    # Clean up the test user
    db.session.delete(test_user)
    db.session.commit()


def test_checklist_update_status(test_client):
    # Create a test user in the database
    hashed_password = generate_password_hash('test_password', "sha256")
    test_user = Users(first_name='Test2', last_name='User2', email='testuser2@example.com',
                      password_hash=hashed_password)
    db.session.add(test_user)
    db.session.commit()

    # Add a checklist item for the test user
    test_item = ChecklistItems(order_no=1, status=False, detail="Test checklist item", user_id=test_user.id)
    db.session.add(test_item)
    db.session.commit()

    # Log in as the test user
    test_client.post('/login', data=dict(
        email='testuser2@example.com',
        password_hash='test_password'
    ), follow_redirects=True)

    # Send a POST request to the `/checklist` route to update the status of the test item
    response = test_client.post('/checklist', json={
        'order_no': 1,
        'status': True
    }, content_type='application/json')

    # Assert that the response is OK (status code 200) and the 'success' key in the JSON response is True
    assert response.status_code == 200
    assert response.json['success'] == True

    # Assert that the status of the test item has been updated in the database
    updated_item = ChecklistItems.query.filter_by(user_id=test_user.id, order_no=1).first()
    assert updated_item.status == True

    # Clean up the test item and test user
    db.session.delete(test_item)
    db.session.delete(test_user)
    db.session.commit()


def test_search(test_client, requests_mock):
    # Mock the Google Geocoding API response
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geocode_mock_response = {
        "status": "OK",
        "results": [
            {
                "geometry": {
                    "location": {
                        "lat": 37.7749,
                        "lng": -122.4194
                    }
                }
            }
        ]
    }
    requests_mock.get(geocode_url, json=geocode_mock_response)

    # Mock the Google Places API response
    places_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    places_mock_response = {
        "results": [
            {
                "name": "Test Place",
                "formatted_address": "123 Test St, San Francisco, CA 94103",
                "formatted_phone_number": "(123) 456-7890",
                "photos": [{"photo_reference": "test_photo_reference"}],
                "geometry": {
                    "location": {
                        "lat": 37.7749,
                        "lng": -122.4194
                    }
                },
                "place_id": "test_place_id"
            }
        ]
    }
    requests_mock.get(places_url, json=places_mock_response)

    response = test_client.get('/search', query_string={'query': 'Test', 'zip': '94103'})
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json['results']) == 1
    assert response_json['results'][0]['title'] == 'Test Place'
    assert response_json['totalResults'] == 1


def test_search_invalid_zip(test_client):
    with requests_mock.Mocker() as m:
        # Mock the response for the Google Geocoding API with an invalid zip code
        invalid_zip_response = {
            "status": "ZERO_RESULTS",
            "results": []
        }
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        m.get(f"{geocode_url}?address=00000&key=AIzaSyBlz0-Xrd-UmDgkjHXFmVv_NAFBqTh11YU", json=invalid_zip_response)

        # Send a GET request to the `/search` route with an invalid zip code
        response = test_client.get('/search', query_string=dict(query="test", zip="00000"))

        # Assert that the response is OK (status code 200)
        assert response.status_code == 200

        # Parse the JSON response
        data = json.loads(response.data)

        # Assert that the 'results' key in the JSON response is an empty list
        assert data["results"] == []

        # Assert that the 'totalResults' key in the JSON response is 0
        assert data["totalResults"] == 0


def test_search_pagination(test_client):
    with requests_mock.Mocker() as m, patch('app.routes.get_lat_lng_from_zip') as mock_get_lat_lng:
        # Set the mock return value for get_lat_lng_from_zip
        mock_get_lat_lng.return_value = (37.7749, -122.4194)

        # Mock the responses for the Google Places API
        places_response = {
            "status": "OK",
            "results": [{
                "name": "Test Place",
                "formatted_address": "123 Test St",
                "place_id": "test_place_id",
                "geometry": {
                    "location": {
                        "lat": 37.7749,
                        "lng": -122.4194
                    }
                }
            }],
            "next_page_token": "test_page_token"
        }
        places_url = re.compile("https://maps.googleapis.com/maps/api/place/textsearch/json.*")
        m.register_uri('GET', places_url, json=places_response)

        # Send a GET request to the `/search` route with a start_index greater than 1
        response = test_client.get('/search', query_string=dict(query="test", zip="94103", start=21))

        # Assert that the response is OK (status code 200)
        assert response.status_code == 200

        # Parse the JSON response
        data = json.loads(response.data)
        # print(data)
        assert "results" in data


def test_get_page_token():
    # Test with valid response containing next_page_token
    response = {
        "status": "OK",
        "results": [
            {"name": "Test Place 1", "place_id": "test_place_id_1"},
            {"name": "Test Place 2", "place_id": "test_place_id_2"}
        ],
        "next_page_token": "test_page_token"
    }
    expected_token = "test_page_token"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": "test", "key": "test_key", "pagetoken": "test_page_token"}
    offset = 21
    assert get_page_token(offset, url, params) == expected_token
