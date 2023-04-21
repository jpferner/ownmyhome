from werkzeug.security import generate_password_hash
from app.models import Users
from app.forms import SignUpForm
from app import db, create_app
import pytest

# Andrew Court - Testing the Sign-Up Page Where Users Create A New Account

@pytest.fixture(scope='module')
def app():
    """
    Create a Flask application object for the tests to use
    """

    app = create_app()

    # Load test configuration from object
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection during testing

    with app.app_context():
        # Create database tables
        db.create_all()

        # Add a test user to the database
        user = Users(first_name='Max', last_name='Fisher', email='testing@gmail.com',
                     password_hash=generate_password_hash("Testing123", "sha256"))

        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        # Remove the test user
        user = Users.query.filter_by(email='testing@gmail.com').first()
        db.session.delete(user)
        db.session.commit()

        # Drop all tables
        db.drop_all()


@pytest.fixture
def client(app):
    """
    a fixture that uses the app fixture and returns a test client instance for the Flask app.
    The test client is used to make requests to the app in tests.

    Args:
        app: the app fixture

    Returns: a test client instance for the Flask app

    """
    return app.test_client()


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


def test_signup_with_valid_data(client, app):
    """
    Test that a user can sign up with valid data, and the app redirects to the login page
    and displays a success message.

    :param client: Flask test client object
    :param app: Flask application object
    """

    with app.app_context():
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


def test_signup_with_existing_email(client, app):
    """
    Test that a user cannot sign up with an email that is already in use, and the app displays
    an error message.

    :param client: Flask test client object
    :param app: Flask application object
    """

    #  # Create a SignUpForm object and populate it with data that matches the existing user's email
    with app.app_context():
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

    print(response.data)
    # assert that the form validation error is shown to the user
    assert b'Password cannot contain ., &lt;, &gt;, /, \\, or spaces.' in response.data

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
