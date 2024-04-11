from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    states = storage.all("State").values()
    return render_template('10-states.html', states=states)


@app.route('/states/<state_id>', strict_slashes=False)
def state_cities(state_id):
    state = storage.get("State", state_id)
    if state:
        cities = sorted(state.cities, key=lambda x: x.name)
        return render_template('10-states.html', state=state, cities=cities)
    else:
        return "<h1>Not found!</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
