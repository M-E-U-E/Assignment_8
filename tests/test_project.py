# import unittest
# from unittest.mock import patch, MagicMock, mock_open, AsyncMock
# import os
# import sys
# import json
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from trip.spiders.async_trip_spider import AsyncHotelSpider

# class TestAsyncHotelSpider(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         """Set up the test class instance."""
#         cls.spider = AsyncHotelSpider()

#     @patch("os.makedirs")
#     def test_create_folders(self, mock_makedirs):
#         """Test folder creation for hotel data."""
#         city_name = "Test City"
#         folders = self.spider.create_folders(city_name)

#         expected_json_path = os.path.join(os.getcwd(), "city_data", "json_of_hotels")
#         expected_images_path = os.path.join(os.getcwd(), "city_data", "images_of_hotels", "test_city")

#         self.assertEqual(folders['json'], expected_json_path)
#         self.assertEqual(folders['images'], expected_images_path)
#         mock_makedirs.assert_called()

#     def test_parse_json_data_valid(self):
#         """Test JSON parsing for valid JSON data."""
#         script_data = '{"key": "value"}'
#         result = self.spider.parse_json_data(script_data)
#         self.assertEqual(result, {"key": "value"})

#     def test_parse_json_data_invalid(self):
#         """Test JSON parsing for invalid JSON data."""
#         script_data = '{"key": "value"'
#         with self.assertLogs(self.spider.logger, level="ERROR") as log:
#             result = self.spider.parse_json_data(script_data)
#             self.assertEqual(result, {})
#             self.assertIn("Failed to parse JSON", log.output[0])

#     def test_get_cities(self):
#         """Test city extraction from JSON data."""
#         data = {
#             "initData": {
#                 "htlsData": {
#                     "inboundCities": [{"name": "City1"}],
#                     "outboundCities": [{"name": "City2"}]
#                 }
#             }
#         }
#         result = self.spider.get_cities(data)
#         self.assertEqual(len(result), 2)
#         self.assertIn({"name": "City1"}, result)
#         self.assertIn({"name": "City2"}, result)

#     def test_extract_script_data(self):
#         """Test extracting script data from a response."""
#         response = MagicMock()
#         response.css().re_first.return_value = '{"key": "value"}'
#         result = self.spider.extract_script_data(response)
#         self.assertEqual(result, '{"key": "value"}')

#     def test_extract_hotel_list(self):
#         """Test extracting the hotel list from JSON data."""
#         data = {
#             "initData": {
#                 "firstPageList": {
#                     "hotelList": [{"hotelName": "Hotel1"}, {"hotelName": "Hotel2"}]
#                 }
#             }
#         }
#         result = self.spider.extract_hotel_list(data)
#         self.assertEqual(len(result), 2)
#         self.assertIn({"hotelName": "Hotel1"}, result)

#     def test_process_hotel(self):
#         """Test processing individual hotel data."""
#         hotel = {
#             "hotelBasicInfo": {
#                 "hotelId": "123",
#                 "hotelName": "Test Hotel",
#                 "hotelImg": "http://example.com/image.jpg"
#             },
#             "commentInfo": {"commentScore": 4.5},
#             "positionInfo": {
#                 "positionName": "Test Address",
#                 "coordinate": {"lat": 50.0, "lng": 10.0}
#             },
#             "roomInfo": {"physicalRoomName": "Deluxe Room"}
#         }
#         city_name = "Test City"
#         images_dir = "/test/images/"
#         result = self.spider.process_hotel(hotel, city_name, images_dir)

#         self.assertEqual(result["city_name"], "Test City")
#         self.assertEqual(result["property_title"], "Test Hotel")
#         self.assertEqual(result["hotel_id"], "123")
#         self.assertEqual(result["image_path"], "/test/images/123_Test_Hotel.jpg")

#     @patch("builtins.open", new_callable=mock_open)
#     def test_save_to_json(self, mock_file):
#         """Test saving hotel data to a JSON file."""
#         data = [{"key": "value"}]
#         path = "/test/path.json"
#         self.spider.save_to_json(data, path)

#         mock_file.assert_called_with(path, 'w', encoding='utf-8')
#         mock_file().write.assert_called_once_with(json.dumps(data, indent=4, ensure_ascii=False))

#     @patch("aiohttp.ClientSession.get", new_callable=AsyncMock)
#     async def test_download_image(self, mock_get):
#         """Test downloading a single image asynchronously."""
#         mock_response = MagicMock()
#         mock_response.status = 200
#         mock_response.read = AsyncMock(return_value=b"image_data")
#         mock_get.return_value.__aenter__.return_value = mock_response

#         with patch("builtins.open", mock_open()) as mock_file:
#             await self.spider.download_image(mock_get, "http://example.com/image.jpg", "/test/path.jpg")
#             mock_file.assert_called_with("/test/path.jpg", 'wb')
#             mock_file().write.assert_called_once_with(b"image_data")

#     @patch("aiohttp.ClientSession.get", new_callable=AsyncMock)
#     async def test_download_images(self, mock_get):
#         """Test downloading multiple images asynchronously."""
#         hotel_list = [
#             {"image": "http://example.com/image1.jpg", "image_path": "/test/image1.jpg"},
#             {"image": "http://example.com/image2.jpg", "image_path": "/test/image2.jpg"},
#         ]
#         mock_response = MagicMock()
#         mock_response.status = 200
#         mock_response.read = AsyncMock(return_value=b"image_data")
#         mock_get.return_value.__aenter__.return_value = mock_response

#         with patch("builtins.open", mock_open()):
#             await self.spider.download_images(hotel_list)
#             self.assertEqual(mock_get.call_count, 2)
#     # Lines 20-50: Testing parse() method
#     @patch("scrapy.Request")
#     def test_parse_valid_response(self, mock_request):
#         """Test parse() with valid script data and city extraction."""
#         response = MagicMock()
#         response.css().re_first.return_value = '{"initData": {"htlsData": {"inboundCities": [{"name": "City1", "id": "1"}], "outboundCities": [{"name": "City2", "id": "2"}]}}}'

#         requests = list(self.spider.parse(response))
#         self.assertEqual(len(requests), 2)  # Two cities should generate two requests
#         self.assertEqual(requests[0].url, "https://uk.trip.com/hotels/list?city=1")
#         self.assertEqual(requests[1].url, "https://uk.trip.com/hotels/list?city=2")

#     @patch("scrapy.Spider.logger")
#     def test_parse_no_script_data(self, mock_logger):
#         """Test parse() when no script data is found."""
#         response = MagicMock()
#         response.css().re_first.return_value = None

#         result = list(self.spider.parse(response))
#         self.assertEqual(len(result), 0)
#         mock_logger.warning.assert_called_with("No valid script data found.")

#     # Lines 56-81: Testing parse_city_hotels()
#     @patch("asyncio.run")
#     @patch("builtins.open", new_callable=mock_open)
#     def test_parse_city_hotels(self, mock_file, mock_asyncio_run):
#         """Test parse_city_hotels() processes hotels and saves JSON."""
#         response = MagicMock()
#         response.meta = {'city_name': 'Test City'}
#         response.css().re_first.return_value = '{"initData": {"firstPageList": {"hotelList": [{"hotelBasicInfo": {"hotelId": "123", "hotelName": "Test Hotel", "hotelImg": "http://example.com/image.jpg"}}]}}}'

#         with patch.object(self.spider, 'create_folders') as mock_folders, \
#              patch.object(self.spider, 'save_to_json') as mock_save:
#             mock_folders.return_value = {'json': '/test/json/', 'images': '/test/images/'}

#             self.spider.parse_city_hotels(response)
#             mock_save.assert_called_once()
#             mock_asyncio_run.assert_called_once()
#             mock_file.assert_not_called()  # open() handled inside download_image

#     # Lines 96-98: Testing extract_script_data()
#     def test_extract_script_data(self):
#         """Test extracting script data using a regex."""
#         response = MagicMock()
#         response.css().re_first.return_value = '{"key": "value"}'
#         result = self.spider.extract_script_data(response)
#         self.assertEqual(result, '{"key": "value"}')

#     # Lines 153-158: Testing process_hotel()
#     def test_process_hotel(self):
#         """Test processing a single hotel entry."""
#         hotel = {
#             "hotelBasicInfo": {
#                 "hotelId": "123",
#                 "hotelName": "Test Hotel",
#                 "hotelImg": "http://example.com/image.jpg"
#             },
#             "commentInfo": {"commentScore": 4.5},
#             "positionInfo": {
#                 "positionName": "Test Address",
#                 "coordinate": {"lat": 50.0, "lng": 10.0}
#             },
#             "roomInfo": {"physicalRoomName": "Deluxe Room"}
#         }
#         city_name = "Test City"
#         images_dir = "/test/images/"

#         result = self.spider.process_hotel(hotel, city_name, images_dir)
#         self.assertEqual(result["city_name"], "Test City")
#         self.assertEqual(result["property_title"], "Test Hotel")
#         self.assertEqual(result["hotel_id"], "123")
#         self.assertEqual(result["image_path"], "/test/images/123_Test_Hotel.jpg")

#     # Lines 164-173: Testing async download_images()
#     @patch("aiohttp.ClientSession.get", new_callable=AsyncMock)
#     async def test_download_images(self, mock_get):
#         """Test asynchronous image downloads."""
#         hotel_list = [
#             {"image": "http://example.com/image1.jpg", "image_path": "/test/image1.jpg"},
#             {"image": "http://example.com/image2.jpg", "image_path": "/test/image2.jpg"},
#         ]
#         mock_response = MagicMock()
#         mock_response.status = 200
#         mock_response.read = AsyncMock(return_value=b"image_data")
#         mock_get.return_value.__aenter__.return_value = mock_response

#         with patch("builtins.open", mock_open()) as mock_file:
#             await self.spider.download_images(hotel_list)
#             self.assertEqual(mock_get.call_count, 2)
#             self.assertEqual(mock_file.call_count, 2)

#     # Lines 182-183: Testing save_to_json()
#     @patch("builtins.open", new_callable=mock_open)
#     def test_save_to_json(self, mock_file):
#         """Test saving hotel data to JSON."""
#         data = [{"key": "value"}]
#         path = "/test/path.json"

#         self.spider.save_to_json(data, path)
#         mock_file.assert_called_with(path, 'w', encoding='utf-8')
#         mock_file().write.assert_called_once_with(json.dumps(data, indent=4, ensure_ascii=False))


# if __name__ == "__main__":
#     unittest.main()