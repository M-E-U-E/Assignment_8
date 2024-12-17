import unittest
from trip.items import Hotel

class TestItems(unittest.TestCase):
    def test_hotel_item_fields(self):
        """Test Hotel item creation."""
        hotel = Hotel()
        hotel.city_name = "Test City"
        hotel.title = "Test Hotel"
        hotel.hotel_id = "123"
        hotel.price = 200.0
        self.assertEqual(hotel.city_name, "Test City")
        self.assertEqual(hotel.title, "Test Hotel")
        self.assertEqual(hotel.hotel_id, "123")
        self.assertEqual(hotel.price, 200.0)

if __name__ == "__main__":
    unittest.main()
