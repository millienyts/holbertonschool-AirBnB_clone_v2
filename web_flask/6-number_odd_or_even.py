#!/usr/bin/python3
'''
    Flask app
'''
from flask import Flask
from flask import render_template

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


# Route to display "c <text>"
@app.route('/c/<text>', strict_slashes=False)
def c_display(text="is cool"):
    '''
        Prints c <text>
    '''
    text = text.replace('_', ' ')
    return f"C {text}"


# Route to display "python <text>/ is cool"
@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_display(text="is cool"):
    '''
        Prints python <text>/ is cool
    '''
    text = text.replace('_', ' ')
    return f"Python {text}"


# Route to display "number <n>"
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


# Route to display number_template with n
@app.route('/number_template/<int:n>')
def display_number(n):
    '''
        Renders template and also number <n> is sent
    '''
    # Check if n is an integer
    if isinstance(n, int):
        return render_template('5-number.html', number=n)


# Route to display number_odd_or_even with n
@app.route('/number_odd_or_even/<int:n>')
def display_even_odd(n):
    # Check if n is an integer
    if isinstance(n, int):
        n_type = 'odd'
        # Determine if n is even or odd
        if n % 2 == 0:
            n_type = 'even'
        return render_template('6-number_odd_or_even.html', number=n,
                               number_type=n_type)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
