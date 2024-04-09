#!/usr/bin/python3
from flask import Flask
from flask import render_template

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
