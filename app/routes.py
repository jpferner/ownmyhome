from flask import render_template, flash, redirect, url_for, request, jsonify
from password_strength import PasswordStats

from app import app
from app import data_manager
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Renders the login.html template and handles POST requests.
    POST requests are not currently used and will simply redirect the user to the index page.

    Returns:
    - If the request is a GET request: the rendered login.html template.
    - If the request is a POST request: a redirect to the index page.
    """
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Renders the sign_up.html template and handles POST requests.
    If the form data is valid, the function will flash a success message and render the index.html template.
    If the form data is invalid, the function will flash an error message and remain on the sign_up.html template.

    Returns:
    - If the request is a GET request: the rendered sign_up.html template.
    - If the request is a POST request: either the rendered index.html template or the rendered sign_up.html template
      with error messages, depending on the validity of the form data.
    """
    if request.method == 'POST':

        # data object to capture the form data
        data = request.form

        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email1 = request.form.get('email')
        email2 = request.form.get('confirm-email')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm-password')
        stats = PasswordStats(password1)  # gives password strength stats on backend

        # show the data on the backend (in terminal) that user entered
        print(data)

        # show in command line how strong password is
        print(stats.strength())

        # set up requirements for each field on the sign-up page
        # category = 'error'
        if len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(lastName) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif len(email1) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif email1 != email2:
            flash('Email addresses do not match.', category='error')
        elif stats.strength() < 0.30:
            flash('Password is not strong enough.', category='error')
            print(stats.strength())
        elif password1 != password2:
            flash('Passwords do not match.', category='error')

        else:  # all form fields are valid
            flash('Account created!', category='success')
            # time.sleep(1)  # give 1 second for flash message to show

            # print(stats.strength())  # show in command line how strong password is
            return render_template('index.html')  # take user to homepage

    return render_template('sign_up.html')


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
