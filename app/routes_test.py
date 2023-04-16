from flask_login import login_user
from werkzeug.security import generate_password_hash
from app import app, db, Users
import pytest

from app.models import ChecklistItems
from app.routes import add_checklist_items


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
    assert b'<h1>Sign Up</h1>' in response.data


def test_services_page_displayed(test_client):
    response = test_client.get('/services')
    assert response.status_code == 200
    assert b'<h2>Search for Home Buying Services</h2>' in response.data


def test_login_page_displayed(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'<h1>Login</h1>' in response.data


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

    # Check if the desired flash message appears
    # with test_client.session_transaction() as sess:
    #     messages = [sess.get('_flashes', [])]
    #     print(messages)  # Add this line to print out the messages in the session
    #     assert ('error', 'Invalid Email and/or Password. Please try again.') in messages


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
