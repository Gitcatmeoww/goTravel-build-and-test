import unittest
import json
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

    # Wishlist database should be created properly
    def test_database_setup(self):
        test_record_add = Wishlist(
            destination="berkeley", planned_date="04/18/2023")
        db.session.add(test_record_add)
        db.session.commit()

        test_record_get = Wishlist.query.filter_by(
            destination="berkeley").first()
        self.assertEqual(test_record_get.destination, "berkeley")
        self.assertEqual(test_record_get.planned_date, "04/18/2023")

    # Recommend endpoint should return {"status": "success", "response": "test recommend"} with a status code 200
    def test_get_recommend(self):
        response = self.client.get('/recommend')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode()), {
            "status": "success", "response": "test recommend"})


if __name__ == "__main__":
    unittest.main()
