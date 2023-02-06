from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)

# TASK = [
#     {
#         'id': 1,
#         'step': 'First',
#         'title': 'Check Your Credit Scores',
#         'complete': False
#     },
#     {
#         'id': 2,
#         'step': 'Second',
#         'title': 'Calculate A Budget',
#         'complete': False
#     }
# ]

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
    return render_template('checklist.html')

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
