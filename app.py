from flask import Flask, render_template, request, url_for, redirect, jsonify

import ChecklistItems

app = Flask(__name__)


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
    todo_table = []
    completed_table = []

    for item in ChecklistItems.checklist_items:
        if item.status:
            completed_table.append(item)
        else:
            todo_table.append(item)

    todo_table = sorted(todo_table, key=lambda x: x.order_no)
    completed_table = sorted(completed_table, key=lambda y: y.order_no)

    if request.method == 'POST':
        data = request.get_json()
        item_id = int(data['id'])

        for item in ChecklistItems.checklist_items:
            if item.order_no == item_id:
                item.toggle_status()
                return jsonify({'success': True})

        return jsonify({'success': False})

    return render_template('checklist.html', todo_table=todo_table, completed_table=completed_table)


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
