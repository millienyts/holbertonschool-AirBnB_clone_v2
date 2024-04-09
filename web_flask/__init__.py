from flask import Flask

# Create Flask application instance
app = Flask(__name__)

# Import your routes
from web_flask.0-hello_route import *
from web_flask.1-hbnb_route import *
from web_flask.2-c_route import *
from web_flask.3-python_route import *
from web_flask.4-number_route import *
from web_flask.5-number_template import *

def main():
    app.run(host='0.0.0.0', port=5000)

# If this script is run directly, run the Flask app
if __name__ == '__main__':
    main()

