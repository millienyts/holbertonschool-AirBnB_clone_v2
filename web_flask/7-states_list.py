#!/usr/bin/python3
'''
    Flask app
'''
from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)

# Route to display "Hello HBNB!"
@app.route('/', strict_slashes=False)
def hello_hbnb():
    '''
        Prints Hello HBNB!
    '''
    return 'Hello HBNB!'

# Route to display "HBNB"
@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''
        Prints HBNB
    '''
    return 'HBNB'

# Route to display text that starts with 'c'
@app.route('/c/<text>', strict_slashes=False)
def c_display(text="is cool"):
    '''
        Prints c <text>
    '''
    text = text.replace('_', ' ')
    return f"C {text}"

# Both routes apply to the same method
@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_display(text="is cool"):
    '''
        Prints python <text>/ is cool
    '''
    text = text.replace('_', ' ')
    return f"Python {text}"

# Route to display a number
@app.route('/number/<int:n>', strict_slashes=False)
def int_display(n):
    '''
        prints number <n>
    '''
    # Check if n is an integer
    if isinstance(n, int):
        return f'{n} is a number'
    else:
        return '404 not found'

# Route to display a number and render a template
@app.route('/number_template/<int:n>')
def display_number(n):
    '''
        Renders template and also number <n> is sent
    '''
    if isinstance(n, int):
        return render_template('5-number.html', number=n)

# Route to display if a number is odd or even
@app.route('/number_odd_or_even/<int:n>')
def display_even_odd(n):
    # Check if n is an integer
    if isinstance(n, int):
        n = int(n)
        n_type = 'odd'
        # Determine if the number is even or odd
        if n % 2 == 0:
            n_type = 'even'
        return render_template('6-number_odd_or_even.html', number=n,
                                number_type=n_type)

# Route to display a list of states
@app.route('/states_list')
def display_states():
    '''
        Displays all states with id
    '''
    # Get all State objects
    states = storage.all(State)
    # Sort states alphabetically by name
    states = sorted(states.values(), key=lambda state: state.name)
    # Render template and pass states to it
    return render_template('7-states_list.html', states=states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
