#!/usr/bin/python3
"""starts a Flask web application"""

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    """Return"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """Return"""
    return 'HBNB'


@app.route('/c/<text>')
def c_is_fun(text):
    """Return"""
    return 'C ' + text.replace('_', ' ')


@app.route('/python/')
@app.route('/python/<text>')
def python_with_text(text='is cool'):
    """Reformat"""
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>')
def number(n=None):
    """Allow reques"""
    return str(n) + ' is a number'


@app.route('/number_template/<int:n>')
def number_template(n):
    """Retrieve"""
    path = '5-number.html'
    return render_template(path, n=n)


if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
