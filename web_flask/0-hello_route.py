#!/usr/bin/python3
'''
   This module contains a script which will start a Flask web application.
'''
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    return "Hello HBNB!\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
