#!/usr/bin/python3
"""starts web application with two routings"""

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    """Return"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """Return"""
    return 'HBNB'

if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
