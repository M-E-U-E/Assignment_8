import unittest
from trip.db.models import Hotel

class TestHotelModel(unittest.TestCase):
    def test_hotel_model_fields(self):
        """Test Hotel model fields initialization."""
        hotel = Hotel(
            city_name="Test City",
            title="Test Hotel",
            hotel_id="123",
            price=100.0,
            rating=4.5,
            location="Test Address",
            latitude=12.34,
            longitude=56.78,
            room_type="Deluxe",
            image_url="http://example.com/img.jpg",
            image_path="/path/to/image.jpg"
        )
        self.assertEqual(hotel.city_name, "Test City")
        self.assertEqual(hotel.hotel_id, "123")
        self.assertEqual(hotel.price, 100.0)
        self.assertEqual(hotel.rating, 4.5)

if __name__ == "__main__":
    unittest.main()
