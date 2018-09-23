from display import app, model
from flask import render_template, redirect, url_for, flash
@app.route('/')
def index():
    return render_template('display.html', display=model.display)

@app.route('/start')
def start():
    try:
        model.t.start()
    except:
        pass
    flash('Started Timer')
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    if not model.t.is_alive():
        model.t.cancel()
    flash('Stopped Timer')
    return redirect(url_for('index'))
