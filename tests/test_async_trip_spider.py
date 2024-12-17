import unittest
from unittest.mock import patch, MagicMock, AsyncMock, mock_open
import json
from scrapy.http import HtmlResponse
from trip.spiders.async_trip_spider import AsyncHotelSpider


class TestAsyncHotelSpider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the spider for testing."""
        cls.spider = AsyncHotelSpider()

    # 1. Test extract_script_data method
    def test_extract_script_data_valid(self):
        """Test extracting valid script data."""
        response = MagicMock()
        response.xpath.return_value.get.return_value = 'window.IBU_HOTEL = {"key": "value"};'

        result = self.spider.extract_script_data(response)
        self.assertEqual(result, '{"key": "value"}')

    def test_extract_script_data_invalid(self):
        """Test extracting script data when no match is found."""
        response = MagicMock()
        response.xpath.return_value.get.return_value = None

        result = self.spider.extract_script_data(response)
        self.assertIsNone(result)

    # 2. Test parse_json_data method
    def test_parse_json_data_valid(self):
        """Test parsing valid JSON data."""
        script_data = '{"key": "value"}'
        result = self.spider.parse_json_data(script_data)
        self.assertEqual(result, {"key": "value"})

    def test_parse_json_data_invalid(self):
        """Test handling invalid JSON data."""
        script_data = '{"key": "value"'
        with self.assertLogs(self.spider.logger, level="ERROR") as log:
            result = self.spider.parse_json_data(script_data)
            self.assertEqual(result, {})
            self.assertIn("Failed to parse JSON", log.output[0])

    # 3. Test get_cities method
    def test_get_cities(self):
        """Test extracting cities from JSON data."""
        data = {
            "initData": {
                "htlsData": {
                    "inboundCities": [{"name": "City1"}],
                    "outboundCities": [{"name": "City2"}]
                }
            }
        }
        result = self.spider.get_cities(data)
        self.assertEqual(len(result), 2)
        self.assertIn({"name": "City1"}, result)
        self.assertIn({"name": "City2"}, result)

    # 4. Test create_folders method
    @patch("os.makedirs")
    def test_create_folders(self, mock_makedirs):
        """Test folder creation."""
        city_name = "Test City"
        result = self.spider.create_folders(city_name)

        self.assertIn("json", result)
        self.assertIn("images", result)
        mock_makedirs.assert_called()

    # 5. Test process_hotel method
    def test_process_hotel(self):
        """Test processing hotel data."""
        hotel = {
            "hotelBasicInfo": {
                "hotelId": "123",
                "hotelName": "Test Hotel",
                "hotelImg": "http://example.com/image.jpg"
            },
            "commentInfo": {"commentScore": 4.5},
            "positionInfo": {"positionName": "Test Address", "coordinate": {"lat": 1.23, "lng": 4.56}},
            "roomInfo": {"physicalRoomName": "Deluxe"}
        }
        city_name = "Test City"
        images_dir = "/images/"

        result = self.spider.process_hotel(hotel, city_name, images_dir)
        self.assertEqual(result["hotel_id"], "123")
        self.assertEqual(result["city_name"], "Test City")
        self.assertEqual(result["image_path"], "/images/123_Test_Hotel.jpg")

    # 6. Test save_to_json method
    @patch("builtins.open", new_callable=mock_open)
    def test_save_to_json(self, mock_file):
        """Test saving data to JSON."""
        data = [{"key": "value"}]
        path = "/test/file.json"

        self.spider.save_to_json(data, path)
        mock_file.assert_called_with(path, 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with(json.dumps(data, indent=4, ensure_ascii=False))

    # 7. Test async download_image method
    @patch("aiohttp.ClientSession.get", new_callable=AsyncMock)
    async def test_download_image_success(self, mock_get):
        """Test successful image download."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"image_data")
        mock_get.return_value.__aenter__.return_value = mock_response

        with patch("builtins.open", mock_open()) as mock_file:
            await self.spider.download_image(mock_get, "http://example.com/image.jpg", "/path/image.jpg")
            mock_file.assert_called_with("/path/image.jpg", 'wb')
            mock_file().write.assert_called_once_with(b"image_data")

    @patch("aiohttp.ClientSession.get", new_callable=AsyncMock)
    async def test_download_image_failure(self, mock_get):
        """Test handling failed image download."""
        mock_response = MagicMock()
        mock_response.status = 404
        mock_get.return_value.__aenter__.return_value = mock_response

        with patch.object(self.spider.logger, "warning") as mock_warning:
            await self.spider.download_image(mock_get, "http://example.com/image.jpg", "/path/image.jpg")
            mock_warning.assert_called_with("Failed to download image: http://example.com/image.jpg")

    # 8. Test parse method
    @patch("scrapy.Request")
    def test_parse_valid(self, mock_request):
        """Test parse method with valid response."""
        response = MagicMock()
        response.xpath.return_value.get.return_value = 'window.IBU_HOTEL = {"initData": {"htlsData": {"inboundCities": [{"name": "City1", "id": "1"}]}}};'

        results = list(self.spider.parse(response))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].url, "https://uk.trip.com/hotels/list?city=1")

    def test_parse_no_script_data(self):
        """Test parse method when no script data is found."""
        response = MagicMock()
        response.xpath.return_value.get.return_value = None

        with patch.object(self.spider.logger, "warning") as mock_warning:
            results = list(self.spider.parse(response))
            self.assertEqual(len(results), 0)
            mock_warning.assert_called_with("No script data found. Cannot extract hotel data.")


if __name__ == "__main__":
    unittest.main()
