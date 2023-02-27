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
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('checklist.html', checklist_items=ChecklistItems.checklist_items)


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
