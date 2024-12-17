import unittest
from unittest.mock import patch, MagicMock
from trip.pipelines import PostgresPipeline, HotelImagesPipeline

class TestPostgresPipeline(unittest.TestCase):
    @patch("trip.pipelines.SessionLocal")
    def test_process_item(self, mock_session):
        """Test PostgresPipeline process_item."""
        pipeline = PostgresPipeline()
        pipeline.open_spider(MagicMock())

        mock_session_instance = mock_session.return_value
        mock_session_instance.add.return_value = None
        mock_session_instance.commit.return_value = None

        item = {
            "city_name": "Test City",
            "property_title": "Test Hotel",
            "hotel_id": "123",
            "price": 200.0
        }

        processed_item = pipeline.process_item(item, MagicMock())
        self.assertEqual(processed_item["hotel_id"], "123")
        pipeline.close_spider(MagicMock())

    def test_image_pipeline_file_path(self):
        """Test HotelImagesPipeline file_path method."""
        pipeline = HotelImagesPipeline()
        request = MagicMock()
        request.url = "http://example.com/image.jpg"
        item = {"city_name": "Test City", "property_title": "Test Hotel"}
        file_path = pipeline.file_path(request, item=item)
        self.assertIn("images/test_city/test_hotel_image.jpg", file_path)

if __name__ == "__main__":
    unittest.main()
