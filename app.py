from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database


# Database URI
database_uri = 'postgresql://postgres:postgres@localhost/datawarehouse'


# Create database
def create_datawarehouse(database_uri):
    if not database_exists(database_uri):
        create_database(database_uri)
        print("Database created successfully!")
    else:
        print("Database already exists!")


# Flask and postgre database configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
create_datawarehouse(database_uri)


# Database schema initialization
class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(20), nullable=False)
    planned_date = db.Column(db.Date, nullable=False)
    weather_forecast = db.Column(db.String(200))
    recommendation = db.Column(db.String(200))

    def __init__(self, destination, planned_date, weather_forecast=None, recommendation=None):
        self.destination = destination
        self.planned_date = planned_date
        self.weather_forecast = weather_forecast
        self.recommendation = recommendation

    def __repr__(self):
        return f'<Wishlist {self.destination}>'

    def to_dict(self):
        return {
            'id': self.id,
            'destination': self.destination,
            'planned_date': self.planned_date,
            'weather_forecast': self.weather_forecast,
            'recommendation': self.recommendation
        }


# Initialize table in database
@app.cli.command('create-db')
def create_db():
    db.create_all()


# Handlers for wishlist endpoint
def handle_get_all():
    try:
        wishlists = Wishlist.query.all()
        if wishlists:
            return jsonify([wishlist.to_dict() for wishlist in wishlists]), 200
        else:
            return jsonify({"Error: Wishlist not found!"}), 204
    except Exception as e:
        return jsonify(f"Error: Something went wrong when getting all wishlists - {str(e)}"), 400


def handle_create_wishlist():
    return


def handle_get_single(destination):
    return


def handle_update_single(destination):
    return


def handle_delete_single(destination):
    return


@app.route('/wishlist', methods=['GET', 'POST'])
@app.route('/wishlist/<destination>', methods=['GET', 'PUT', 'DELETE'])
def wishlist(destination=None):
    try:
        if destination is None:
            if request.method == "GET":  # Get all wishlist
                return handle_get_all()
            elif request.method == "POST":  # Create a new wishlist
                return handle_create_wishlist()
            else:
                return jsonify("Error: Unsupported HTTP method"), 400
        else:
            destination = destination.lower()
            if request.method == "GET":  # Get one single wishlist
                return handle_get_single(destination)
            elif request.method == "PUT":  # Update one single wishlist
                return handle_update_single(destination)
            elif request.method == "DELETE":  # Delete one single wishlist
                return handle_delete_single(destination)
            else:
                return jsonify("Error: Unsupported HTTP method"), 400
    except Exception as e:
        return jsonify(f"Error: Something went wrong in the wishlist endpoint - {str(e)}"), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
