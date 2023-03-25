from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user

from app import app
from app import data_manager
from app.forms import SignUpForm, LoginForm  # used for sign_up() view and login() view
from app.models import *

# from app.models import Property

# Load checklist data from file
checklist_items = data_manager.load_checklist_data()


# Import the database models; this needs to be at the bottom to prevent a circular error
# from models import *


# Define routes
@app.route("/")
def home():
    """
    Renders the home page of the website.

    Returns: The rendered home page HTML.
    """
    return render_template("index.html")


@app.route('/properties', methods=['GET', 'POST'])
def properties():
    """
    Renders the properties page of the website.

    Returns: The rendered properties page HTML.
    """
    if request.method == 'POST':
        return redirect(url_for('index'))
    # props = Property.query.all()
    return render_template('properties.html')


@app.route('/checklist', methods=['GET', 'POST'])
# @login_required  # requires user to be logged in to access Checklist
def checklist():
    """
    Renders the checklist page of the website, which displays a list of checklist items that can be marked as completed.

    Returns: The rendered checklist page HTML.
    """
    global checklist_items

    if request.method == 'POST':
        # If a POST request is received, toggle the status of the corresponding checklist item and save the updated data
        data = request.get_json()
        item_id = int(data['id'])

        for item in checklist_items:
            if item.order_no == item_id:
                item.toggle_status()
                data_manager.save_checklist_data(checklist_items)
                return jsonify({'success': True})

        return jsonify({'success': False})

    # If a GET request is received, retrieve the list of checklist items and separate them into completed and incomplete
    # items, then render the checklist page HTML with these lists as template variables.
    todo_table = [item for item in checklist_items if not item.status]
    completed_table = [item for item in checklist_items if item.status]
    todo_table = sorted(todo_table, key=lambda x: x.order_no)
    completed_table = sorted(completed_table, key=lambda y: y.order_no)

    return render_template('checklist.html', todo_table=todo_table, completed_table=completed_table)


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
        data = request.form

        homeVal = request.form.get('HomeVal')
        downPay = request.form.get('DownPay')
        loanAmt = request.form.get('LoanAmt')
        interestRate = request.form.get('InterestRate')
        loanTerm = request.form.get('LoanTerm')
        startDate = request.form.get('StartDate')
        propTax = request.form.get('PropTax')
        loanType = request.form.get('LoanType')

        # Checks to see if info is found via console
        print(data)
        if int(homeVal) > 0:
            return render_template('calculator.html', HomeVal=homeVal, DownPay=downPay,
                                   LoanAmt=loanAmt, InterestRate=interestRate, LoanTerm=loanTerm,
                                   StartDate=startDate, PropTax=propTax, LoanType=loanType,
                                   MortTotal=homeVal)
    return render_template('calculator.html')


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
