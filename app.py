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


@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        return jsonify({"status": "success", "response": "test recommend"}), 200
    except:
        return jsonify({"status": "error", "response": "test recommend"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
