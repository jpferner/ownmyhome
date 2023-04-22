from werkzeug.security import generate_password_hash
from app.models import Users
from app.forms import LoginForm
from app import db, create_app
from flask_mail import Mail, Message

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

    # Configure email settings for testing the password reset
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'ownmyhome.csc450@gmail.com'  # set this to your email
    app.config['MAIL_PASSWORD'] = 'lbuhsobvyoodshlh!'  # set this to your email password
    app.config['MAIL_DEFAULT_SENDER'] = 'ownmyhome.csc450@gmail.com'  # set this to your email

    mail = Mail(app)

    with app.app_context():
        # Create database tables
        db.create_all()

        # Remove all users from the database
        db.session.query(Users).delete()

        # Add a test user to the database
        user = Users(first_name='Max', last_name='Fisher', email='testing@example.com',
                     password_hash= generate_password_hash("Testing123!", "sha256"))

        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        # Remove the test user
        user = Users.query.filter_by(email='testing@example.com').first()
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
    """
    a test function that checks if a user can successfully log in to their account

    Args:
        client: client fixture
        app: app fixture
    """
    with app.app_context():
        form = LoginForm()
        form.email.data = "testing@example.com"
        form.password_hash.data = "Testing123!"

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/login', data=form.data, follow_redirects=True)
        print(response.data)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Welcome, Max' in response.data

def test_login_wrong_password(client, app):
    """
        a test function that checks for an error message when a user tries to log in to their account
        with an invalid password

        Args:
            client: client fixture
            app: app fixture
        """
    with app.app_context():

        form = LoginForm()
        form.email.data = "testing@example.com"
        form.password_hash.data = "WrongPassword!"

        # Send a POST request to the sign-up route with the form data and follow the redirect
        response = client.post('/login', data=form.data, follow_redirects=True)
        print(response.data)

        # Check that the HTTP response status code is 200 OK and the success message is displayed
        assert response.status_code == 200
        assert b'Invalid Email and/or Password. Please try again.' in response.data

def test_login_user_does_not_exist(client, app):
    """
        a test function that checks for an error message when a user tries to log in to their account
        but the user does not have an account yet

        Args:
            client: client fixture
            app: app fixture
        """
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


def test_logout(client, app):
    """
    a test function that checks if a user can successfully log out of their account

    Args:
        client: client fixture
        app: app fixture
    """
    with app.app_context():
        # Log in to the account
        form = LoginForm()
        form.email.data = "testing@example.com"
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


@pytest.fixture (scope='module')
def mail(app):
    """
        Create a Flask-Mail object for the password reset tests to use
    """
    with app.app_context():
        mail = Mail(app)
        yield mail
@pytest.mark.parametrize('email', ['test@example.com', 'test2@example.com'])  # passes list of email address to the test
def test_reset_password_request_success(client, app, email, mail):
    """
    Test that a user can successfully request a password reset email
    """
    with app.app_context():
        # Create a user to test with
        user = Users(email=email, password_hash="Testing123!")
        db.session.add(user)
        db.session.commit()

        # Send a POST request to the password reset request route with the user's email
        response = client.post('/reset_password', data={'email': user.email}, follow_redirects=True)

        # Check that the HTTP response status code is 200 OK
        assert response.status_code == 200

        # Check that the success message is displayed in the response
        assert b'Thank you for submitting your email address.\n\n' \
               b'If an account is associated with this email, a\n' \
               b'password reset link will be sent to your inbox shortly.\n\n' \
               b'Please check your email and follow the instructions\n' \
               b'to reset your password.\n\n' \
               b'Important: Password reset link expires in 5 minutes.' in response.data

        # print(response.data)
        #
        # # Check that the user received a password reset email
        # assert len(mail.outbox) == 1
        # assert mail.outbox[0].subject == "Password Reset Request"
        # assert mail.outbox[0].to == [user.email]
