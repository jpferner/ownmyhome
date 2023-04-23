import json
import re

from flask import url_for
import requests_mock
from app import app

from app.models import ChecklistItems
from app.routes import add_checklist_items, get_page_token


from app.forms import LoginForm
from unittest.mock import patch

from werkzeug.security import generate_password_hash
from app.models import Users

from app.forms import SignUpForm
from app import db, create_app
import pytest


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


# Andrew Court - Testing the Sign-Up Page Where Users Create A New Account

@pytest.fixture(scope='function')
def ac_app():
    """
    Create a Flask application object for the tests to use
    """

    ac_app = create_app()

    # Load test configuration from object
    ac_app.config['TESTING'] = True
    ac_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    ac_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection during testing

    with ac_app.app_context():
        # Create database tables
        db.create_all()

        # Add a test user to the database
        user = Users(first_name='Max', last_name='Fisher', email='testing@gmail.com',
                     password_hash=generate_password_hash("Testing123!", "sha256"))

        db.session.add(user)
        db.session.commit()

    yield ac_app

    with ac_app.app_context():
        # Remove the test user
        user = Users.query.filter_by(email='testing@gmail.com').first()
        db.session.delete(user)
        db.session.commit()

        # # Drop all tables
        # db.drop_all()


@pytest.fixture
def client(ac_app):
    """
    a fixture that uses the app fixture and returns a test client instance for the Flask app.
    The test client is used to make requests to the app in tests.

    Args:
        ac_app: the app fixture

    Returns: a test client instance for the Flask app

    """
    return ac_app.test_client()


def test_create_account_url(client):
    """
     a test function that uses the client fixture to make a GET request
      to the /sign-up endpoint and asserts that the response status code is 200 (OK).
    Args:
        client: client fixture

    Returns: response status code is 200 (OK).

    """
    response = client.get('/sign-up')
    assert response.status_code == 200


def test_signup_with_valid_data(client, ac_app):
    """
    Test that a user can sign up with valid data, and the app redirects to the login page
    and displays a success message.

    :param client: Flask test client object
    :param ac_app: Flask application object
    """

    with ac_app.app_context():
        # Create a SignUpForm object and populate it with valid data
        form = SignUpForm()
        form.first_name.data = "Jared"
        form.last_name.data = "Blackmon"
        form.email.data = "jblackmon@aol.com"
        form.confirm_email.data = "jblackmon@aol.com"
        form.password_hash.data = "Testing123!"
        form.confirm_password_hash.data = "Testing123!"
        form.accept_tos.data = True

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/sign-up', data=form.data, follow_redirects=True)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Account created!\n\nPlease use your credentials to log in.' in response.data


def test_signup_with_existing_email(client, ac_app):
    """
    Test that a user cannot sign up with an email that is already in use, and the app displays
    an error message.

    :param client: Flask test client object
    :param ac_app: Flask application object
    """

    #  # Create a SignUpForm object and populate it with data that matches the existing user's email
    with ac_app.app_context():
        form = SignUpForm()
        form.first_name.data = "Kyle"
        form.last_name.data = "Salomon"
        form.email.data = "testing@gmail.com"
        form.confirm_email.data = "testing@gmail.com"
        form.password_hash.data = "Testing123!"
        form.confirm_password_hash.data = "Testing123!"
        form.accept_tos.data = True

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/sign-up', data=form.data, follow_redirects=True)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200  # 200 is the HTTP status code for redirect
        assert b'Sign up unsuccessful.\n\n Please try again using a different email address' in response.data

def test_signup_with_invalid_first_name(client):
    # submit the signup form with an invalid first name
    response = client.post('/sign-up', data={
        'first_name': '',  # blank first name
        'last_name': 'Cameron',
        'email': 'cam@gmail.com',
        'confirm_email': 'cam@gmail.com',
        'password_hash': 'Testing123!',
        'confirm_password_hash': 'Testing123!',
        'accept_tos': True}, follow_redirects=True)

    # assert that the form validation error is shown to the user
    assert b'This field is required.' in response.data


def test_signup_with_invalid_password(client):
    # submit the signup form with an invalid password
    response = client.post('/sign-up', data={
        'first_name': 'Joseph',  # blank first name
        'last_name': 'Cameron',
        'email': 'cam@gmail.com',
        'confirm_email': 'cam@gmail.com',
        'password_hash': 'Testing12<3!',
        'confirm_password_hash': 'Testing12<3!',
        'accept_tos': True}, follow_redirects=True)

    # assert that the form validation error is shown to the user
    assert b'Password must have at least one uppercase character, \nat least one lowercase character, ' \
           b'\nat least one number,\n and at least one special character.' in response.data

def test_signup_with_mismatched_emails(client):
    # submit the signup form with emails that do not match
    response = client.post('/sign-up', data={
        'first_name': 'Joseph',  # blank first name
        'last_name': 'Cameron',
        'email': 'cam123@gmail.com',
        'confirm_email': 'cam@gmail.com',
        'password_hash': 'Testing123!',
        'confirm_password_hash': 'Testing123!',
        'accept_tos': True}, follow_redirects=True)

    print(response.data)
    # assert that the form validation error is shown to the user
    assert b'Emails do not match. Please try again.' in response.data

def test_signup_without_accepting_tos(client):
    # submit the signup form with emails that do not match
    response = client.post('/sign-up', data={
        'first_name': 'Joseph',  # blank first name
        'last_name': 'Cameron',
        'email': 'cam@gmail.com',
        'confirm_email': 'cam@gmail.com',
        'password_hash': 'Testing123!',
        'confirm_password_hash': 'Testing123!',
        # fail to check the checkbox agreeing to the terms of service
        }, follow_redirects=True)

    print(response.data)
    # assert that the form validation error is shown to the user
    assert b'This field is required.' in response.data

# Andrew Court - Testing the Login Page Where Users Log In to Access Their Accounts
def test_login_url(client):
    """
     Test function that uses the client fixture to make a GET request
      to the /login endpoint and asserts that the response status code is 200 (OK).
    Args:
        client: client fixture

    Returns: response status code is 200 (OK).

    """
    response = client.get('/login')
    assert response.status_code == 200

def test_log_in_to_account_success(client, ac_app):
    """
    Test function that checks if a user can successfully log in to their account

    Args:
        client: client fixture
        ac_app: app fixture
    """
    with ac_app.app_context():
        form = LoginForm()
        form.email.data = "testing@gmail.com"
        form.password_hash.data = "Testing123!"

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/login', data=form.data, follow_redirects=True)
        print(response.data)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Welcome, Max' in response.data

def test_login_wrong_password(client, ac_app):
    """
        Test function that checks for an error message when a user tries to log in to their account
        with an invalid password

        Args:
            client: client fixture
            ac_app: app fixture
        """
    with ac_app.app_context():

        form = LoginForm()
        form.email.data = "testing@example.com"
        form.password_hash.data = "WrongPassword!"

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/login', data=form.data, follow_redirects=True)
        print(response.data)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Invalid Email and/or Password. Please try again.' in response.data

def test_login_wrong_password_correct_email(client, ac_app):
    """
        Test function that checks for an error message when a user tries to log in to their account
        with an invalid password

        Args:
            client: client fixture
            ac_app: app fixture
        """
    with ac_app.app_context():

        form = LoginForm()
        form.email.data = "testing@gmail.com"
        form.password_hash.data = "WrongPassword!"

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/login', data=form.data, follow_redirects=True)
        print(response.data)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Invalid Email and/or Password. Please try again.' in response.data

def test_login_user_does_not_exist(client, ac_app):
    """
        Test function that checks for an error message when a user tries to log in to their account
        but the user does not have an account yet

        Args:
            client: client fixture
            ac_app: app fixture
        """
    with ac_app.app_context():

        form = LoginForm()
        form.email.data = "wrongemail@gmail.com"
        form.password_hash.data = "WrongPassword!"

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/login', data=form.data, follow_redirects=True)
        print(response.data)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Invalid Email and/or Password. Please try again.' in response.data


def test_logout(client, ac_app):
    """
    a test function that checks if a user can successfully log out of their account

    Args:
        client: client fixture
        ac_app: app fixture
    """
    with ac_app.app_context():
        # Log in to the account
        form = LoginForm()
        form.email.data = "testing@gmail.com"
        form.password_hash.data = "Testing123!"

        # Send a POST request to the login route with the form data and follow the redirect
        response = client.post('/login', data=form.data, follow_redirects=True)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Welcome, Max' in response.data

        # Log out of the account
        response = client.get('/logout', follow_redirects=True)

        # Check that the HTTP response status code is 200 OK and the logout message is displayed
        assert response.status_code == 200
        assert b'You have successfully logged out!' in response.data


# Andrew Court - Testing the Password Reset Functionality Where Users Access the Password Reset Request Page,
# Are Sent Password Reset Links, and Access the Change Password Page
def test_password_reset_page_url(client):
    """
        Test that the password reset page can be accessed via its URL.

        This function sends a GET request to the password reset URL and checks
        that the server responds with a 200 status code, indicating that the
        page was successfully accessed.

        Args:
            client: The Flask test client to use for sending the request.
        """

    response = client.get('/reset_password_request')
    print(f" THIS IS IT: {response.data}")
    assert response.status_code == 200

def test_password_reset_request_invalid_email(client):
    """
        Test that a password reset request with an invalid email address returns an error message.
        For this particular test, the user enters an email address that is not in the expected valid format.

        Args:
            client: Flask test client object.

        Returns:
            None.
        """
    response = client.post('/reset_password_request', data=dict(
        email='invalid_email'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid or missing character(s) in email address.' in response.data

def test_password_reset_request_success_and_redirects_to_login(client):
    """
        Test that a password reset request is successfully submitted for a valid email in the database,
        and that the user is redirected to the login page with the expected success message.

        Args:
            client: a test client object for the Flask application.

        Returns:
            None
        """
    response = client.post('/reset_password_request', data=dict(
        email='testing@gmail.com'
    ), follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Thank you for submitting your email address.\n\nIf an account is associated ' \
           b'with this email,\na password reset link will be sent to your inbox shortly.\n\n ' \
           b'Please check your email and follow the instructions\nto reset your password.\n\n' \
           b'Important: Password reset link expires in 10 minutes.' in response.data

def test_password_reset_request_fail_user_not_in_database_and_redirects_to_login(client):
    """Test that a user is redirected to the login page and shown a password reset message if they try to submit a
        password reset request, but the email is not associated with an account in our database. For security reasons,
        the user is still redirected to the login page and shown the same message someone with an account in our
        database would be shown

        Args:
            client: Flask test client object that is used to simulate HTTP requests to the application.

        Returns:
            None
        """
    response = client.post('/reset_password_request', data=dict(
        email='failtestexample@gmail.com'
    ), follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    assert b'Thank you for submitting your email address.\n\nIf an account is associated ' \
           b'with this email,\na password reset link will be sent to your inbox shortly.\n\n ' \
           b'Please check your email and follow the instructions\nto reset your password.\n\n' \
           b'Important: Password reset link expires in 10 minutes.' in response.data


def test_password_reset_valid_token_for_successful_password_change(client, ac_app):
    """
        Test that password reset fails when passwords do not match on the change password page.

        Args:
            client: Test client for making HTTP requests to Flask application.
            ac_app: Application context for the Flask application.

        Returns:
            None
        """

    # Create a test user object and add the test user to the database
    with ac_app.app_context():
        test_user = Users.query.filter_by(email="testing@gmail.com".lower()).first()
        token = Users.generate_password_reset_token(test_user)

        # Create the form data
        form_data = {
            'password_hash': 'Newpassword123!',
            'confirm_password_hash': 'Newpassword123!'
        }

        response = client.post(f'/change_password/{token}', data=form_data, follow_redirects=True)

        # Check that the response status code is 200 and response message indicates a failed reset password attempt
        assert response.status_code == 200
        assert b'Password reset successful! Please log into your account.' in response.data

def test_password_reset_with_mismatch_passwords_on_change_password_page(client, ac_app):
    # Create a test user object and add the test user to the database
    with ac_app.app_context():
        test_user = Users.query.filter_by(email="testing@gmail.com".lower()).first()
        token = Users.generate_password_reset_token(test_user)

        # Create the form data
        form_data = {
            'password_hash': 'Newpassword123!',
            'confirm_password_hash': 'DoesNotMatch123!'
        }

        response = client.post(f'/change_password/{token}', data=form_data, follow_redirects=True)
        print(response.data)
        assert response.status_code == 200
        assert b'Passwords do not match. Please try again.' in response.data


def test_password_reset_for_expired_token_for_failed_password_change_attempt(client, ac_app):
    """Test that the password reset fails when using an expired token. The token is manipulated in
        this test to be expired.

        The test creates a user object and generates a password reset token that is already expired.
        It then attempts to reset the password using the expired token and verifies that the password
        reset fails and returns the appropriate error message.

        Args:
            client: The Flask test client.
            ac_app: The Flask application context.

        Returns:
            None.
        """
    # Create a test user object and add the test user to the database
    with ac_app.app_context():
        test_user = Users.query.filter_by(email="testing@gmail.com".lower()).first()
        # Generate a password reset token that is already expired
        token = Users.generate_password_reset_token(test_user, expires_in=-10)

        # Create a dictionary to hold the form data
        form_data = {
            'password_hash': 'Newpassword123!',
            'confirm_password_hash': 'Newpassword123'
        }

        # Post the form data to the reset password endpoint with the expired token
        response = client.post(f'/change_password/{token}', data=form_data, follow_redirects=True)
        print(response.data)
        # Check that the response status code is 200
        assert response.status_code == 200

        # Check that the response message indicates that the password reset failed
        assert b'The password reset link has expired. \n Please request a new one.' in response.data

def test_password_reset_for_invalid_token_for_failed_password_change_attempt(client, ac_app):
    """Test that the password reset fails when using an invalid token.

    The test generates an invalid token and attempts to reset the password using the invalid token.
    It then verifies that the password reset fails and redirects the user back to the password reset
    request page.

    Args:
        client: The Flask test client.
        ac_app: The Flask application context.

    Returns:
        None.
    """
    # Generate an invalid token that will not match any user in the database
    token = "invalid_token"

    # Create a dictionary to hold the form data
    form_data = {
        'password_hash': 'Newpassword123!',
        'confirm_password_hash': 'Newpassword123'
    }

    # Post the form data to the reset password endpoint with the invalid token
    response = client.post(f'/change_password/{token}', data=form_data, follow_redirects=True)
    print(response.data)
    # Check that the response status code is 200
    assert response.status_code == 200

    # Check that the response message indicates that the password reset failed as user is redirect to Reset
    # Password Request page
    assert b'The password reset link is invalid or has expired.\nPlease try again.' in response.data

