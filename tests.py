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

    # Test #4: Create a new (non-existing) wishlist should return a success message with a status code 201
    def test_create_new_wishlist(self):
        with app.app_context():
            response = self.client.post(
                '/wishlist', data=dict(destination="berkeley", planned_date=datetime.date(2023, 5, 1)))
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, "Success: New wishlist added!")

            new_wishlist = Wishlist.query.filter_by(
                destination="berkeley").first()
            self.assertIsNotNone(new_wishlist)
            self.assertEqual(new_wishlist.planned_date,
                             datetime.date(2023, 5, 1))

    # Test #5: Create an existing wishlist should return a success message with a status code 201
    def test_create_existing_wishlist(self):
        with app.app_context():
            existing_wishlist = Wishlist(
                destination="berkeley", planned_date=datetime.date(2023, 5, 1))
            db.session.add(existing_wishlist)
            db.session.commit()

            response = self.client.post(
                '/wishlist', data=dict(destination="berkeley", planned_date=datetime.date(2023, 5, 2)))
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, "Success: Wishlist updated!")

            updated_wishlist = Wishlist.query.filter_by(
                destination="berkeley").first()
            self.assertIsNotNone(updated_wishlist)
            self.assertEqual(updated_wishlist.planned_date,
                             datetime.date(2023, 5, 2))

    # Test #6: Get all wishlist should return a list of json with a status code 200
    def test_get_all_wishlists(self):
        with app.app_context():
            wishlist1 = Wishlist(
                destination="berkeley", planned_date=datetime.date(2023, 5, 1))
            wishlist2 = Wishlist(
                destination="oakland", planned_date=datetime.date(2023, 5, 2))
            db.session.add(wishlist1)
            db.session.add(wishlist2)
            db.session.commit()

            response = self.client.get('/wishlist')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json[0], {'destination': 'berkeley', 'id': 1,
                             'planned_date': 'Mon, 01 May 2023 00:00:00 GMT', 'recommendation': None, 'weather_forecast': None})
            self.assertEqual(response.json[1], {'destination': 'oakland', 'id': 2,
                             'planned_date': 'Tue, 02 May 2023 00:00:00 GMT', 'recommendation': None, 'weather_forecast': None})

    # Test #7: Get a single wishlist that does not exist should return a status code 204
    def test_get_single_wishlist_no_record(self):
        response = self.client.get('/wishlist/berkeley')
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
