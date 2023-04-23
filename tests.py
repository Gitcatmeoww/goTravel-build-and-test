import unittest
import json
import datetime
from app import app, db, Wishlist


class TestGoTravel(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/datawarehouse_test'
        cls.client = app.test_client()

        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls) -> None:
        with app.app_context():
            db.drop_all()

    def setUp(self) -> None:
        with app.app_context():
            db.create_all()

    def tearDown(self) -> None:
        with app.app_context():
            db.drop_all()

    # Test #1: Wishlist database should be created properly
    def test_database_setup(self):
        with app.app_context():
            test_record_add = Wishlist(
                destination="berkeley", planned_date=datetime.date(2023, 4, 18))
            db.session.add(test_record_add)
            db.session.commit()

            test_record_get = Wishlist.query.filter_by(
                destination="berkeley").first()
            self.assertEqual(test_record_get.destination, "berkeley")
            self.assertEqual(test_record_get.planned_date,
                             datetime.date(2023, 4, 18))

    # Test #2: Get all wishlist should return a empty list with a status code 200 when there is no record in the database
    def test_get_all_wishlist_no_record(self):
        response = self.client.get('/wishlist')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    # Test #3: Create an empty wishlist should return an error message with a status code 400
    def test_create_empty_wishlist(self):
        response = self.client.post(
            '/wishlist', data=dict(destination="", planned_date=""))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, "Error: Invalid input")


if __name__ == "__main__":
    unittest.main()
