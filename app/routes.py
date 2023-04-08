import time
from random import choice

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf.csrf import validate_csrf

import requests

from app import app

from app.forms import SignUpForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import *
from datetime import date

import bleach

# required import for password reset
from flask_mail import Message
from app import mail




# Define routes
@app.route("/")
@app.route("/index")
def home():
    """
        Renders the home page of the website, which includes a login form and a checklist of items for authenticated users.

        If the user is authenticated, the first incomplete item in the user's checklist is retrieved from the database and
        displayed on the page.

        Returns:
            str: The rendered HTML for the home page.
    """
    login_form = LoginForm()

    first_incomplete_item = None
    if current_user.is_authenticated:
        first_incomplete_item = ChecklistItems.query.filter_by(user_id=current_user.id, status=False).order_by(
            ChecklistItems.order_no).first()

    all_properties = Property.query.all()
    random_property = choice(all_properties) if all_properties else None

    return render_template('index.html', login_form=login_form, first_incomplete_item=first_incomplete_item,
                           random_property=random_property)


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


@app.route('/properties', methods=['GET', 'POST'])
@login_required
def properties():
    """
        Renders the properties page of the website.

        If the request method is POST, redirects the user to the index page.

        Returns:
            The rendered properties page HTML.
    """


    if request.method == 'POST':
        return redirect(url_for('index'))
    props = Property.query.filter_by(user_id=current_user.id).all()
    return render_template('properties.html', props=props)


def add_properties(user_id):
    properties_data = [
        {'propId': 1, 'street': '1007 Orange St', 'city': 'Wilmington', 'state': 'NC', 'zcode': 28401,
         'county': 'New Hanover', 'price': 299900, 'yearBuilt': 2023, 'numBeds': 2, 'numBaths': 2, 'image_filename':'prop1.gif','propUrl':'https://www.zillow.com/homedetails/1007-Orange-St-Wilmington-NC-28401/54309332_zpid/'},
        {'propId': 2, 'street': '6604 Whimbrel Ct', 'city': 'Wilmington', 'state': 'NC', 'zcode': 28409,
         'county': 'New Hanover', 'price': 370000, 'yearBuilt': 1990, 'numBeds': 3, 'numBaths': 3, 'image_filename':'prop2.gif', 'propUrl':'https://www.zillow.com/homedetails/6604-Whimbrel-Ct-Wilmington-NC-28409/2133943557_zpid/'},
        {'propId': 3, 'street': '3507 S College Rd', 'city': 'Wilmington', 'state': 'NC', 'zcode': 28412,
         'county': 'New Hanover', 'price': 415000, 'yearBuilt': 1968, 'numBeds': 3, 'numBaths': 2, 'image_filename':'prop3.gif','propUrl':'https://www.zillow.com/homedetails/3507-S-College-Rd-Wilmington-NC-28409/54332506_zpid/'},
        {'propId': 4, 'street': '4770 Tupelo Dr', 'city': 'Wilmington', 'state': 'NC', 'zcode': 28411,
         'county': 'New Hanover', 'price': 549000, 'yearBuilt': 2017, 'numBeds': 4, 'numBaths': 3, 'image_filename':'prop4.gif','propUrl':'https://www.zillow.com/homedetails/4770-Tupelo-Dr-Wilmington-NC-28411/247832477_zpid/'},
        {'propId': 5, 'street': '311 S 3rd. St', 'city': 'Wilmington', 'state': 'NC', 'zcode': 28401,
         'county': 'New Hanover', 'price': 995000, 'yearBuilt': 1868, 'numBeds': 4, 'numBaths': 3, 'image_filename':'prop5.gif','propUrl':'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
       # add more properties as needed
    ]

    for data in properties_data:
        property = Property(
            propId=data['propId'],
            street=data['street'],
            city=data['city'],
            state=data['state'],
            zcode=data['zcode'],
            county=data['county'],
            price=data['price'],
            yearBuilt=data['yearBuilt'],
            numBeds=data['numBeds'],
            numBaths=data['numBaths'],
            favorite=False,
            image_filename=data['image_filename'],
            propUrl=data['propUrl'],
            user_id=user_id
        )
        db.session.add(property)

    db.session.commit()


@app.route('/checklist', methods=['GET', 'POST'])
@login_required
def checklist():
    """
        Renders the checklist page of the website.

        If the request method is GET, fetches all the checklist items for the current user from the database, orders them
        by their order_no, and renders the checklist page with the items passed as an argument to the template.

        If the request method is POST, updates the status of the checklist item with the given order_no for the current user
        in the database to the new status provided in the JSON payload of the request. Returns a JSON response with a
        success key set to True.

        If the request method is neither GET nor POST, redirects the user to the index page.

        Returns:
        The rendered checklist page HTML if the request method is GET.
        A JSON response with a success key set to True if the request method is POST.
        A redirect response to the index page if the request method is neither GET nor POST.
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
    """
        Adds checklist items for a user to the database.

        Args:
            user_id (int): The ID of the user to add checklist items for.

        Returns:
            None
    """
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
        Renders the calendar page of the website.

        GET request:
        - Renders the calendar.html template.

        POST request:
        - Redirects the user to the index page.

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
    """
       Renders the login page of the website and handles user login form submissions.

       If the form data is valid, the user is logged in and redirected to the home page.
       If the form data is invalid, an error message is flashed and the user is redirected back to the login page.

       Returns:
           - If the request is a GET request: The rendered login page HTML.
           - If the request is a POST request and the form data is valid: A redirect to the home page.
           - If the request is a POST request and the form data is invalid: The rendered login page HTML with error messages.
    """
    # if request.method == 'POST':
    #     return redirect(url_for('index'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        login_form.email.data = bleach.clean(login_form.email.data, strip=True)
        login_form.password_hash.data = bleach.clean(login_form.password_hash.data, strip=True)

        # check for the user in the database with email in lowercase
        user = Users.query.filter_by(email=login_form.email.data.lower()).first()

        # True if Remember_me checkbox is checked and false otherwise
        remember_me = True if request.form.get('remember_me') else False
        if user:
            # Check the hashed password
            if check_password_hash(user.password_hash, login_form.password_hash.data):
                # logs in the user and creates session
                login_user(user, remember=remember_me)
                # flash(f"Login Successful! Welcome back, {user.first_name}!", category='success')
                return redirect(url_for('home'))
            else:
                flash("Invalid Email and/or Password. Please try again.", category='error')

        else:  # user is not found and doesn't exist in database
            flash("Invalid Email and/or Password. Please try again.", category='error')

    # Reset the Remember Me checkbox if error occurs during Login
    login_form.remember_me.data = False

    return render_template('login.html', form=login_form)


# the Sign-Up
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
        Renders the sign-up page of the website and handles POST requests.
        If the form data is valid, the function will create a new user and add them to the database. It will then add
        checklist items for the new user, flash a success message and redirect them to the login page.
        If the form data is invalid, the function will flash an error message and redirect them to the sign-up page.

        Returns:
        - If the request is a GET request: the rendered sign_up.html template.
        - If the request is a POST request: either a redirect to the login page with a success message or a redirect to the
          sign-up page with error messages, depending on the validity of the form data.
    """
    # name = None
    signup_form = SignUpForm()


    # Validate the Sign-Up form
    if signup_form.validate_on_submit():

        # sanitize/clean all fields on the sign-up form before storing in database
        signup_form.first_name.data = bleach.clean(signup_form.first_name.data, strip=True)
        signup_form.last_name.data = bleach.clean(signup_form.last_name.data, strip=True)
        signup_form.email.data = bleach.clean(signup_form.email.data, strip=True)
        signup_form.confirm_email.data = bleach.clean(signup_form.confirm_email.data, strip=True)
        signup_form.password_hash.data = bleach.clean(signup_form.password_hash.data, strip=True)
        signup_form.confirm_password_hash.data = bleach.clean(signup_form.confirm_password_hash.data, strip=True)


        # strip all whitespace from beginning and end of the sting
        signup_form.first_name.data = signup_form.first_name.data.strip()
        signup_form.last_name.data = signup_form.last_name.data.strip()

        # convert email field to lowercase before being stored in the db and strip
        signup_form.email.data = signup_form.email.data.lower().strip()

        # password is entered into db as entered due to case sensitivity and is stripped
        signup_form.password_hash.data = signup_form.password_hash.data.strip()

        # hash the new user's password
        hashed_password = generate_password_hash(signup_form.password_hash.data, "sha256")

        user = Users.query.filter_by(email=signup_form.email.data).first()
        if user is None:
            # Create a new user and the user to the database
            user = Users(first_name=signup_form.first_name.data, last_name=signup_form.last_name.data,
                         email=signup_form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()

            add_properties(user.id)
            # Add checklist items for the new user
            add_checklist_items(user.id)

            flash('Account created! Please use your credentials to log in.', category='success')
            return redirect(url_for('login'))
        else:  # redirect user to the sign-up page, so they can create a new account
            flash('We\'re sorry. This email address already exists in our system.\n', category='error')
            return redirect(url_for('sign_up'))

    # current_users = Users.query.order_by(Users.id)  # query current db of Users

    # Reset the checkbox for Accept TOS if error occurs at Sign Up
    signup_form.accept_tos.data = False

    return render_template('sign_up.html', form=signup_form)


# the Logout view
@app.route('/logout', methods=['GET', 'POST'])
@login_required  # user must be logged in to logout
def logout():
    """
        Logs the user out by calling the logout_user() function and flashes a success message to the user
        before redirecting to the home page.

        Returns: A redirect to the home page.
    """
    logout_user()
    flash("You have successfully logged out!", category='logout')
    return redirect(url_for('login'))

def send_password_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password Reset Request',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[user.email])

    # _external=True will send an absolute URL
    message.body = f"""To reset your password, please follow this link:"
                   
                   {url_for('reset_token', token=token, _external=True)}
                   
                   If you ignore this email, no changes will be made regarding your account.
                   Thank you!
                   """
    mail.send(message)
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    password_reset_form = ResetPasswordRequestForm()
    if password_reset_form.validate_on_submit():
        user = Users.query.filter_by(email=password_reset_form.email.data.lower()).first()

        # if the user exists
        if user:
            send_password_reset_email(user)
            flash('Password reset request has been sent.\nPlease check your email for instructions'
                  ' on how how to reset your password.\n\n'
                  'Important: Password reset link expires in 5 minutes.', category='success')
            return redirect(url_for('login'))
        else:
            flash("We're sorry. There is no account associated with the email provided.", category='error')
    return render_template('reset_password_request.html', title='Password Reset Request', form=password_reset_form,)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = Users.verify_reset_token(token)
    if user is None:  # redirect the user to the request password reset page
        flash("Invalid or expired token. Please try again.")
        return redirect(url_for('reset_password_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        # sanitize/clean all fields on the sign-up form before storing in database
        form.password_hash.data = bleach.clean(form.password_hash.data, strip=True)
        form.confirm_password_hash.data = bleach.clean(form.confirm_password_hash.data, strip=True)

        # password is entered into db as entered due to case sensitivity
        form.password_hash.data = form.password_hash.data.strip()

        # hash the new password
        hashed_password = generate_password_hash(form.password_hash.data, "sha256")

        # make the user's new password the hashed password
        user.password_hash = hashed_password

        # commit the password change to the database
        db.session.commit()
        flash('Password change successful! Please log into your account.', category='success')

        return redirect(url_for('login'))
    return render_template('change_password.html', title="Reset Password", form=form)



@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    """
        Renders the calculator.html template and handles POST requests. If the form data is valid, the function will calculate
        and display the mortgage total on the page.

        GET request: The function renders the calculator.html template with default values for the inputs.

        POST request: The function calculates the mortgage total using the user's input data and displays the result on the
        calculator.html template.

        Returns:
            - If the request is a GET request: the rendered calculator.html template.
            - If the request is a POST request: the rendered calculator.html template with the mortgage total displayed.
    """
    if request.method == 'POST':
        return render_template('calculator.html')
    return render_template('calculator.html', HomeVal=500000, DownPay=150000,
                           LoanAmt=350000, InterestRate=6.5, LoanTerm=30,
                           StartDate=date.today(), PropTax=2400,
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


@app.route('/search', methods=['GET'])
def search():
    """
        Renders the search results page of the website, using the Google Places API to search for locations
        based on a user-provided query and zip code.

        Returns: A JSON object containing search results and the total number of results.
    """
    query = request.args.get('query')
    zip_code = request.args.get('zip')
    start_index = int(request.args.get('start', 1))
    radius = request.args.get('radius', 5000)  # Default radius is 5,000 meters (approx. 3.1 miles)

    lat, lng = get_lat_lng_from_zip(zip_code)
    if lat and lng:
        places_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": f"{query} near {zip_code}",
            "location": f"{lat},{lng}",
            "radius": radius,
            "key": "AIzaSyBlz0-Xrd-UmDgkjHXFmVv_NAFBqTh11YU",
        }

        if start_index > 1:
            params["pagetoken"] = get_page_token(start_index - 1, places_url, params)

        response = requests.get(places_url, params=params)
        data = response.json()
        results = [
            {
                "title": item["name"],
                "link": item["formatted_address"],
                "snippet": item.get("formatted_phone_number", ""),
                "photo_reference": item["photos"][0]["photo_reference"] if "photos" in item else None,
                "lat": item["geometry"]["location"]["lat"],
                "lng": item["geometry"]["location"]["lng"],
                "maps_link": f"https://www.google.com/maps/place/?q=place_id:{item['place_id']}"
            }
            for item in data.get("results", [])
        ]
        total_results = len(results)
    else:
        results = []
        total_results = 0

    return jsonify({"results": results, "totalResults": total_results})


def get_page_token(offset, url, params):
    """
        Given an offset, url, and parameters for a Google Places API request, retrieves the page token associated with
        the corresponding page of results. Page tokens are used by the API to allow pagination of results, and each page
        token corresponds to a specific set of 20 results. This function iterates through the pages of results until it
        reaches the page corresponding to the given offset, and returns the page token associated with that page.

        Args:
            offset (int): The 1-based index of the page of results to retrieve the page token for.
            url (str): The URL of the Google Places API endpoint to send the request to.
            params (dict): The parameters to include in the request, including any search parameters and API key.

        Returns:
            str: The page token for the specified page of results, or None if no such page exists.
    """
    for _ in range(offset // 20):
        response = requests.get(url, params=params)
        data = response.json()
        if "next_page_token" in data:
            params["pagetoken"] = data["next_page_token"]
        else:
            break
        time.sleep(2)  # Google Places API requires a short delay between requests for the next page token
    return params.get("pagetoken")


def get_lat_lng_from_zip(zip_code):
    """
        Given a zip code, sends a request to the Google Geocoding API to get the latitude and longitude of the location
        associated with the zip code.

        Args:
            zip_code (str): A string representing a zip code.

        Returns:
            tuple: A tuple containing the latitude and longitude of the location associated with the given zip code.
                If the zip code is invalid or the Google Geocoding API does not return a valid response, the function
                returns a tuple of None values.
    """
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key=AIzaSyBlz0-Xrd-UmDgkjHXFmVv_NAFBqTh11YU"
    response = requests.get(geocode_url)
    data = response.json()
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        return None, None


@app.route('/update_favorites', methods=['POST'])
def update_favorites():
    """
        Updates the favorite status of a property based on user input from the frontend.
        Expects the following POST parameters:
            - csrf_token: A CSRF token to protect against cross-site request forgery attacks.
            - propId: The ID of the property to update.
            - checked: A string representation of a boolean value indicating whether the property should be favorited or not.

        Returns:
            - A JSON object containing the rendered HTML for the updated properties table and favorites table.
    """
    csrf_token = request.form['csrf_token']
    validate_csrf(csrf_token)

    propId = request.form['propId']
    checked = request.form['checked'] == 'true'

    # Get the property instance
    prop = Property.query.filter_by(propId=propId).first()

    # Update the favorite status of the property
    if checked:
        favorite = UserFavorite(user_id=current_user.id, property_id=propId)
        existing_favorite = UserFavorite.query.filter_by(user_id=current_user.id, property_id=propId).first()
        if not existing_favorite:
            db.session.add(favorite)
            print('1')

    else:
        favorite = UserFavorite.query.filter_by(user_id=current_user.id, property_id=propId).first()
        if favorite:
            print('2')
            db.session.delete(favorite)

    db.session.commit()  # Save changes to the database

    # Get the list of favorite properties for the user
    user_favorites = UserFavorite.query.filter_by(user_id=current_user.id).all()
    favorite_props = [uf.property for uf in user_favorites]

    # Render the templates
    props_table = render_template('props_table.html', props=Property.query.all(), favorite_props=favorite_props)
    favorites_table = render_template('favorites_table.html', favorite_props=favorite_props)

    return jsonify(props=props_table, favorites=favorites_table)


@app.route('/favorites_table')
def favorites_table():
    """
        Renders the favorites_table.html template, which displays a table of properties marked as "favorite" by the user.

        Returns:
        - The rendered favorites_table.html template.
    """
    user_favorites = UserFavorite.query.filter_by(user_id=current_user.id).all()
    favorite_props = [uf.property for uf in user_favorites]
    return render_template('favorites_table.html', favorite_props=favorite_props)
