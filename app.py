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
        return jsonify([wishlist.to_dict() for wishlist in wishlists]), 200
    except Exception as e:
        return jsonify(f"Error: Something went wrong when getting all wishlists - {str(e)}"), 400


def handle_create_wishlist():
    try:
        # Get user inputs from front-end form
        destination = request.form.get('destination')
        planned_date = request.form.get('planned_date')
        # Check the validity of user input
        if destination is None or destination == "" or planned_date is None or planned_date == "":
            return jsonify("Error: Invalid input"), 400
        # Strip any leading or trailing whitespaces in inputs and make them lowercase
        destination = destination.strip(" ").lower()
        planned_date = planned_date.strip(" ")

        # Check if the destination already exists in DB
        wishlist_db = Wishlist.query.filter_by(destination=destination).first()
        # If destination does NOT exist, add the user's desired destination and planned travel date into DB
        if not wishlist_db:
            new_wishlist = Wishlist(
                destination=destination, planned_date=planned_date)
            db.session.add(new_wishlist)
            db.session.commit()
            return jsonify("Success: New wishlist added!"), 201
        # If destination ALREADY exists, update the corresponding date to the destination into DB
        else:
            wishlist_db.planned_date = planned_date
            db.session.commit()
            return jsonify("Success: Wishlist updated!"), 201
    except Exception as e:
        return jsonify(f"Error: Something went wrong when creating a new wishlist - {str(e)}"), 400


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
