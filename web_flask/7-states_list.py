#!/usr/bin/python3
'''
   Starts a Flask web application listening on 0.0.0.0:5000. Used to
   retrieve objects from storage and rendered into HTML.
'''
from models import storage
from flask import Flask
from flask import render_template
from models import State
app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def state():
    db = storage.all(State)
    states = []
    for value in db.values():
        states.append(value)
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
