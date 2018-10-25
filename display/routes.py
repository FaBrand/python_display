from display import app, model
from flask import render_template, redirect, url_for, flash
from model import Monitors
@app.route('/')
def index():
    return render_template('display.html', display=model.display)

@app.route('/success')
def new_success():
    model.display.add_change(model.ChangeFactory.make_success())
    return redirect(url_for('index'))

@app.route('/fail')
def new_failure():
    model.display.add_change(model.ChangeFactory.make_failure())
    return redirect(url_for('index'))

@app.route('/random')
def new_random():
    model.display.add_change(model.ChangeFactory.make_change())
    return redirect(url_for('index'))
