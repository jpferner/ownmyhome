from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from app import app
from app.forms import SignUpForm, LoginForm  # used for sign_up() view and login() view
from app.models import *
from datetime import date


# Define routes
@app.route("/")
@app.route("/index")
def home():
    """
    Renders the home page of the website.

    Returns: The rendered home page HTML.
    """
    test = "Hello, World!"
    login_form = LoginForm()

    first_incomplete_item = None
    if current_user.is_authenticated:
        first_incomplete_item = ChecklistItems.query.filter_by(user_id=current_user.id, status=False).order_by(
            ChecklistItems.order_no).first()

    return render_template('index.html', test=test, login_form=login_form, first_incomplete_item=first_incomplete_item)


@app.route('/properties', methods=['GET', 'POST'])
def properties():
    """
    Renders the properties page of the website.

    Returns: The rendered properties page HTML.
    """
    if request.method == 'POST':
        return redirect(url_for('index'))
    props = Property.query.all()
    return render_template('properties.html', props=props)


@app.route('/checklist', methods=['GET', 'POST'])
@login_required
def checklist():
    """
    Renders the checklist page of the website, which displays a list of checklist items that can be marked as completed.

    Returns: The rendered checklist page HTML.
    """
    if request.method == 'GET':
        items = ChecklistItems.query.filter_by(user_id=current_user.id).order_by(ChecklistItems.order_no).all()
        return render_template('checklist.html', items=items)

    elif request.method == 'POST':
        order_no = request.json['order_no']
        new_status = request.json['status']

        # Update the item status in the database
        item = ChecklistItems.query.filter_by(user_id=current_user.id, order_no=order_no).first()
        item.status = new_status
        db.session.commit()

        return jsonify(success=True)

    else:
        return redirect(url_for('index'))


def add_checklist_items(user_id):
    steps = [
        "Do you know what your current credit score is? Check out our services tab above to see what options are available to you.",
        "Do you have your home picked out? Check out our properties tab to see what homes are available within your search parameters.",
        "Do you know what type of financing is available to you? Check out our services tab above to see what options are available to you.",
        "Do you know how much home you can afford? Check out our calculator tab to find out the right price for you.",
        "Do you understand your current debt to income ratio and what that means, Check out our calculator tab to find out more."
    ]

    for i, step in enumerate(steps, start=1):
        item = ChecklistItems(order_no=i, status=False, detail=step, user_id=user_id)
        db.session.add(item)

    db.session.commit()


@app.route('/calendar', methods=['GET', 'POST'])
# @login_required  # requires the user to be logged in to access this page
def calendar():
    """
    Renders the calendar.html template and handles POST requests.
    POST requests are not currently used and will simply redirect the user to the index page.

    Returns:
    - If the request is a GET request: the rendered calendar.html template.
    - If the request is a POST request: a redirect to the index page.
    """
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('calendar.html')


# the Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #     return redirect(url_for('index'))

    login_form = LoginForm()

    """
        Renders the sign_up.html template and handles POST requests.
        If the form data is valid, the function will flash a success message and render the index.html template.
        If the form data is invalid, the function will flash an error message and remain on the sign_up.html template.
        Returns:
        -If the request is a GET request: the rendered sign_up.html template.
        -If the request is a POST request: either the rendered index.html template or the rendered sign_up.html template
          with error messages, depending on the validity of the form data.
    """
    if login_form.validate_on_submit():
        user = Users.query.filter_by(email=login_form.email.data).first()
        if user:
            # Check the hashed password
            if check_password_hash(user.password_hash, login_form.password_hash.data):
                login_user(user)  # logs in the user and creates session
                flash(f"Login Successful! Welcome back, {user.first_name}!", category='success')
                return redirect(url_for('home'))
            else:
                flash("Invalid Email and/or Password. Please try again.", category='error')

        else:  # user is not found and doesn't exist in database
            flash("Invalid Email and/or Password. Please try again.", category='error')

    return render_template('login.html', form=login_form)


# the Sign-Up
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # name = None
    signup_form = SignUpForm()

    # Validate the Sign-Up form
    if signup_form.validate_on_submit():
        print(f"Plaintext Password: {signup_form.password_hash.data}")
        # hash the new user's password
        hashed_password = generate_password_hash(signup_form.password_hash.data, "sha256")
        print(f"After hashing password: {hashed_password}")

        user = Users.query.filter_by(email=signup_form.email.data).first()
        if user is None:
            # Create a new user and the user to the database
            user = Users(first_name=signup_form.first_name.data, last_name=signup_form.last_name.data,
                         email=signup_form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()

            # Add checklist items for the new user
            add_checklist_items(user.id)

            flash('Account created! Please use your credentials to log in.', category='success')
            return redirect(url_for('login'))
        else:  # redirect user to the sign-up page, so they can create a new account
            flash('We\'re sorry. This email address already exists in our system.\n', category='error')
            return redirect(url_for('sign_up'))

    # current_users = Users.query.order_by(Users.id)  # query current db of Users

    return render_template('sign_up.html', form=signup_form)


# the Logout view
@app.route('/logout', methods=['GET', 'POST'])
@login_required  # user must be logged in to logout
def logout():
    logout_user()
    flash("You have successfully logged out!", category='logout')
    return redirect(url_for('login'))


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    """
    Renders the calculator.html template and handles POST requests.
    If the form data is valid, the function will calculate and display the mortgage total on the page.

    Returns:
    - If the request is a GET request: the rendered calculator.html template.
    - If the request is a POST request: the rendered calculator.html template with the mortgage total displayed.
    """
    if request.method == 'POST':

        return render_template('calculator.html')
    return render_template('calculator.html', HomeVal=500000, DownPay=80000,
                           LoanAmt=350000, InterestRate=6.5, LoanTerm=30,
                           StartDate=date.today(), PropTax=5.0,
                           MortTotal=0)


@app.route('/services', methods=['GET', 'POST'])
def services():
    """
    Renders the services.html template and handles POST requests.
    POST requests are not currently used and will simply redirect the user to the index page.

    Returns:
    - If the request is a GET request: the rendered services.html template.
    - If the request is a POST request: a redirect to the index page.
    """
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('services.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    Renders the index.html template and handles POST requests.
    POST requests are not currently used and will simply redirect the user to the index page.

    Returns:
    - If the request is a GET request: the rendered index.html template.
    - If the request is a POST request: a redirect to the index page.
    """
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('index.html')
