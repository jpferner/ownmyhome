from werkzeug.security import generate_password_hash
from app.models import Users
from app.forms import LoginForm
from app import db, create_app
import pytest

# Andrew Court - Testing the Login Page Where Users Log In to Access Their Account

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

        # Remove all users from the database
        db.session.query(Users).delete()

        # Add a test user to the database
        user = Users(first_name='Max', last_name='Fisher', email='testing@gmail.com',
                     password_hash= generate_password_hash("Testing123!", "sha256"))

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


def test_login_url(client):
    """
     a test function that uses the client fixture to make a GET request
      to the /login endpoint and asserts that the response status code is 200 (OK).
    Args:
        client: client fixture

    Returns: response status code is 200 (OK).

    """
    response = client.get('/login')
    assert response.status_code == 200

def test_log_in_to_account_success(client, app):
    with app.app_context():

        form = LoginForm()
        form.email.data = "testing@gmail.com"
        form.password_hash.data = "Testing123!"

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/login', data=form.data, follow_redirects=True)
        print(response.data)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Welcome, Max' in response.data

def test_login_wrong_password(client, app):
    with app.app_context():

        form = LoginForm()
        form.email.data = "testing@gmail.com"
        form.password_hash.data = "WrongPassword!"

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/login', data=form.data, follow_redirects=True)
        print(response.data)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Invalid Email and/or Password. Please try again.' in response.data

def test_login_user_does_not_exist(client, app):
    with app.app_context():

        form = LoginForm()
        form.email.data = "wrongemail@gmail.com"
        form.password_hash.data = "WrongPassword!"

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/login', data=form.data, follow_redirects=True)
        print(response.data)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Invalid Email and/or Password. Please try again.' in response.data


