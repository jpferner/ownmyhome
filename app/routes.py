from flask import render_template, flash, redirect, url_for, request, jsonify

from app import app
from app.models import *
from app.forms import SignUpForm  # used for sign_up() view


# Define routes
@app.route("/")
def home():
    """
    Renders the home page of the website.

    Returns: The rendered home page HTML.
    """
    test = ChecklistItems.query.all()

    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template("index.html", test=test)


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
def checklist():
    """
    Renders the checklist page of the website, which displays a list of checklist items that can be marked as completed.

    Returns: The rendered checklist page HTML.
    """
    if request.method == 'POST' or 'Get':
        if request.is_json:
            item_id = request.json['item_id']
            new_status = request.json['status']

            # Update the item status in the database
            item = ChecklistItems.query.get(item_id)
            item.status = new_status
            db.session.commit()

            return jsonify(success=True)

        else:
            return redirect(url_for('index'))

    items = ChecklistItems.query.filter_by(user_id=current_user.id).all()
    return render_template('checklist.html', items=items)


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
        -If the request is a GET request: the rendered sign_up.html template.
        -If the request is a POST request: either the rendered index.html template or the rendered sign_up.html template
          with error messages, depending on the validity of the form data.
    """
    signup_form = SignUpForm()

    # Validate the Sign-Up form
    if signup_form.validate_on_submit():
        flash('Account created!', category='success')
        return redirect(url_for('sign_up'))
        # return redirect(url_for())

    return render_template('sign_up.html', form=signup_form)


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
