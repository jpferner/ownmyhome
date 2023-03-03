from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from password_strength import PasswordPolicy
from password_strength import PasswordStats
import ChecklistItems

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY='8*bb2(n^)jk'
)

policy = PasswordPolicy.from_names(
    length=8,  # min length for password is 8 characters
    uppercase=1,  # requires minimum 1 uppercase letter
    numbers=1,  # requires minimum 1 digit
    strength=0.50  # password score of at least 0.5; good, strong passwords start at 0.66
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/properties', methods=['GET', 'POST'])
def properties():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('properties.html')


@app.route('/checklist', methods=['GET', 'POST'])
def checklist():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('checklist.html', checklist_items=ChecklistItems.sorted_checklist_items)


@app.route('/complete-item', methods=['POST'])
def complete_item():
    data = request.get_json()
    item_id = data['id']
    for item in ChecklistItems.checklist_items:
        if item.order_no == int(item_id):
            item.mark_completed()
            return jsonify({'success': True})
    return jsonify({'success': False})


@app.route('/undo-item', methods=['POST'])
def undo_item():
    data = request.get_json()
    item_id = data['id']
    for item in ChecklistItems.checklist_items:
        if item.order_no == item_id:
            item.completed = False
            return jsonify({'success': True})
    return jsonify({'success': False})


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('calendar.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email1 = request.form.get('email')
        email2 = request.form.get('confirm-email')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm-password')
        stats = PasswordStats(password1)  # gives password strength stats on backend

        # show the data on the backend (in terminal) that user entered
        data = request.form
        print(data)

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
        elif stats.strength() < 0.50:
            flash('Password is not strong enough.', category='error')
            print(stats.strength())
        elif password1 != password2:
            flash('Passwords do not match.', category='error')

        else:  # all form fields are valid
            flash('Account created!', category='success')
            #time.sleep(1)  # give 1 second for flash message to show

            print(stats.strength())  # show in command line how strong password is
            return render_template('index.html')  # take user to homepage

    return render_template('sign_up.html')


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('calculator.html')


@app.route('/services', methods=['GET', 'POST'])
def services():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('services.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
