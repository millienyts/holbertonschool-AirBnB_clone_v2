from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Teardown the database session."""
    storage.close()


@app.route('/places/<id>', strict_slashes=False)
def show_place(id):
    """Show information about the place."""
    place = storage.get("Place", id)
    if place is None:
        return "Not found", 404
    return render_template('place.html', place=place)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
