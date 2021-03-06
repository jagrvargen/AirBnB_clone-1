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


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    db = storage.all()
    cities = []
    states = []
    for key, value in db.items():
        if "State" in key:
            states.append(value)
            for city in value.cities:
                if city.state_id == value.id:
                    cities.append(city)
    return render_template("8-cities_by_states.html", cities=cities,
                           states=states)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
