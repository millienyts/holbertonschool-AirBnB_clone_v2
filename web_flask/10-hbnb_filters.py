#!/usr/bin/python3
import sys
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'

@app.route('/c/<text>', strict_slashes=False)
def c_display(text="is cool"):    
    text = text.replace('_', ' ')
    return f"C {text}"

# Both routes apply to the same method
@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_display(text="is cool"): 
    text = text.replace('_', ' ')
    return f"Python {text}"

@app.route('/number/<n>', strict_slashes=False)
def int_display(n):
    if n.isdigit():
        return f'{n} is a number'
    else:
        return '404 not found'

@app.route('/number_template/<n>', strict_slashes=False)
def display_number(n):
    if n.isdigit():
        return(render_template('5-number.html', number=n))
    else:
        return render_template('error.html', status_msg = 'Invalid digit not integer')

@app.route('/number_odd_or_even/<n>', strict_slashes=False)
def display_even_odd(n):
    if n.isdigit():
        n = int(n)
        n_type = 'odd'
        if n % 2 == 0:
            n_type = 'even'
        return(render_template('6-number_odd_or_even.html', number=n, number_type=n_type))
    else:
        return render_template('error.html', status_msg = 'Digit not valid, need integer')

@app.route('/states_list', strict_slashes=False)
def display_states():
    states = storage.all(State)
    states = sorted(states.values(), key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)

@app.route('/cities_by_states', strict_slashes=False)
def display_cities_states():
    states = storage.all(State)
    states = sorted(states.values(), key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=states)

@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def find_state(id=None):
    states = storage.all(State).values()
    if id:
        for state in states:
            if state.id == id:
                return render_template('9-states.html', state = state)
        
        return render_template('error.html')
    else:
    
        return render_template('9-states.html', states = states)

@app.teardown_appcontext
def teardown(exception=None):
    storage.close()


@app.errorhandler(404)
def not_found_error(e):
    return render_template('error.html', status_msg = str(e)), 404


@app.route('/hbnb_filters')
def display_filter_search():

    states = storage.all(State)
    states = sorted(states.values(), key=lambda state: state.name)

    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        print(f"-{amenity.name}-")

    return render_template('10-hbnb_filters.html', states = states, amenities = amenities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
