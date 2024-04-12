#!/usr/bin/python3
import sys
sys.path.append('c:\\https://github.com/millienyts/holbertonschool-AirBnB_clone_v2.git')
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)

# Route to display "Hello HBNB!"
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
        return '404 not found'

@app.route('/number_odd_or_even/<n>', strict_slashes=False)
def display_even_odd(n):
    if n.isdigit():
        n = int(n)
        n_type = 'odd'
        if n % 2 == 0:
            n_type = 'even'
        return(render_template('6-number_odd_or_even.html', number=n, number_type=n_type))
    else:
        return '404 not found'

@app.route('/states_list', strict_slashes=False)
def display_states():
    states = storage.all(State)
    # Get the objects from {state_id: {objects}} and order by name A -Z
    states = sorted(states.values(), key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)

@app.route('/cities_by_states', strict_slashes=False)
def display_cities_states():
    states = storage.all(State)
    # Get the objects from {state_id: {objects}} and order by name A -Z
    states = sorted(states.values(), key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
