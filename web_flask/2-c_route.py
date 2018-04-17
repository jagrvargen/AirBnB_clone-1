#!/usr/bin/python3
'''
   This module contains a script which will start a Flask web application and
   display "Hello HBNB!" and "HBNB" from the "/" and "/hbnb" URLs respectively.
   "C <text>" will be displayed by calling /c/<text> where any text can replace
   <text>.
'''
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    return "Hello HBNB!"

@app.route("/hbnb/", strict_slashes=False)
def hbnb():
    return "HBNB"

@app.route("/c/<string:text>/", strict_slashes=False)
def c(text):
    return "C {}".format(text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
