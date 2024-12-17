import scrapy
import json
import re
import random
import os
import asyncio
import aiohttp

class AsyncHotelSpider(scrapy.Spider):
    """
    Spider for scraping hotel data from Trip.com with async image downloading.
    """
    name = "async_trip"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        """
        Parse the main page and extract city data.
        """
        script_data = self.extract_script_data(response)
        if not script_data:
            self.logger.warning("No script data found. Cannot extract hotel data.")
            return

        try:
            # Parse the extracted script data as JSON
            data = json.loads(script_data)
            hotel_list = data.get("initData", {}).get("htlsData", {}).get("hotelList", [])
            
            for hotel in hotel_list:
                item = {
                    "city_name": hotel.get("cityName", ""),
                    "property_title": hotel.get("hotelName", ""),
                    "hotel_id": hotel.get("hotelId", ""),
                    "price": hotel.get("price", 0),
                    "rating": hotel.get("rating", 0.0),
                    "address": hotel.get("address", ""),
                    "latitude": hotel.get("latitude", 0.0),
                    "longitude": hotel.get("longitude", 0.0),
                    "room_type": hotel.get("roomType", ""),
                    "image": hotel.get("imageUrl", ""),
                }
                self.logger.info(f"Yielding item: {item}")
                yield item
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse script data as JSON: {e}")

        script_data = self.extract_script_data(response)
        if not script_data:
            self.logger.warning("No valid script data found.")
            return

        try:
            ibu_hotel_data = self.parse_json_data(script_data)
            cities_to_search = self.get_cities(ibu_hotel_data)

            if len(cities_to_search) < 3:
                self.logger.warning("Not enough cities to choose 3.")
                return

            # Randomly select 3 cities
            selected_cities = random.sample(cities_to_search, 3)
            for city in selected_cities:
                city_name = city.get("name", "Unknown")
                city_id = city.get("id", "")
                if not city_id:
                    self.logger.warning(f"No ID found for city: {city_name}")
                    continue

                city_hotels_url = f"https://uk.trip.com/hotels/list?city={city_id}"
                self.logger.info(f"Requesting data for city: {city_name}")
                yield scrapy.Request(
                    url=city_hotels_url,
                    callback=self.parse_city_hotels,
                    meta={'city_name': city_name, 'city_id': city_id}
                )
        except Exception as e:
            self.logger.error(f"Unexpected error during parsing: {e}")

    def parse_city_hotels(self, response):
        """
        Parse the city hotels page and save data.
        """
        city_name = response.meta.get('city_name', 'Unknown')
        script_data = self.extract_script_data(response)

        output_folder = self.create_folders(city_name)
        city_json_path = os.path.join(output_folder['json'], f"{city_name.lower().replace(' ', '_')}.json")
        city_hotels = []
        
        if script_data:
            try:
                ibu_hotel_data = self.parse_json_data(script_data)
                hotel_list = self.extract_hotel_list(ibu_hotel_data)

                # Process and save hotel data
                city_hotels = [self.process_hotel(hotel, city_name, output_folder['images']) for hotel in hotel_list]
                # Process hotel details and yield each
                for hotel in hotel_list:
                    hotel_data = self.process_hotel(hotel, city_name, output_folder['images'])
                    yield hotel_data  # Ensure this line is indented properly
                # Save hotel data to JSON file
                self.save_to_json(city_hotels, city_json_path)

                # Download images asynchronously
                asyncio.run(self.download_images(city_hotels))

                self.logger.info(f"Data saved for city {city_name} in {city_json_path}")
            except Exception as e:
                self.logger.error(f"Error processing hotels for city {city_name}: {e}")
        else:
            self.logger.warning(f"No script data found for city: {city_name}")

    # Utility Methods
    # def extract_script_data(self, response):
    #     """
    #     Extract `window.IBU_HOTEL` script data from the response.
    #     """
    #     return response.css("script::text").re_first(r"window\.IBU_HOTEL\s*=\s*(\{.*?\});")
    def extract_script_data(self, response):
        pattern = r"window\.IBU_HOTEL\s*=\s*(\{.*?\});"  # Regex to capture JSON data
        match = re.search(pattern, response.text, re.DOTALL)
        if match:
            script_data = match.group(1)
            self.logger.info("Successfully extracted script data.")
            print("Extracted Script Data:", script_data)  # Debug print
            return script_data
        self.logger.warning("No script data found.")
        return None

    def parse_json_data(self, script_data):
        """
        Parse JSON-like script data.
        """
        try:
            return json.loads(script_data)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON: {e}")
            return {}

    def get_cities(self, data):
        """
        Extract inbound and outbound cities.
        """
        inbound = data.get("initData", {}).get("htlsData", {}).get("inboundCities", [])
        outbound = data.get("initData", {}).get("htlsData", {}).get("outboundCities", [])
        return inbound + outbound

    def create_folders(self, city_name):
        """
        Create directories for JSON and image storage.
        """
        output_folder = os.path.join(os.getcwd(), 'city_data')
        json_dir = os.path.join(output_folder, 'json_of_hotels')
        images_dir = os.path.join(output_folder, 'images_of_hotels', city_name.lower().replace(' ', '_'))

        os.makedirs(json_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)

        return {'json': json_dir, 'images': images_dir}

    def extract_hotel_list(self, data):
        """
        Extract hotel list from JSON data.
        """
        return data.get("initData", {}).get("firstPageList", {}).get("hotelList", [])

    def process_hotel(self, hotel, city_name, images_dir):
        """
        Process hotel details.
        """
        hotel_id = hotel.get("hotelBasicInfo", {}).get("hotelId", "")
        hotel_name = hotel.get("hotelBasicInfo", {}).get("hotelName", "").replace(" ", "_")
        image_url = hotel.get("hotelBasicInfo", {}).get("hotelImg", "")

        return {
            "city_name": city_name,
            "property_title": hotel.get("hotelBasicInfo", {}).get("hotelName", ""),
            "hotel_id": hotel_id,
            "price": hotel.get("hotelBasicInfo", {}).get("price", ""),
            "rating": hotel.get("commentInfo", {}).get("commentScore", ""),
            "address": hotel.get("positionInfo", {}).get("positionName", ""),
            "latitude": hotel.get("positionInfo", {}).get("coordinate", {}).get("lat", ""),
            "longitude": hotel.get("positionInfo", {}).get("coordinate", {}).get("lng", ""),
            "room_type": hotel.get("roomInfo", {}).get("physicalRoomName", ""),
            "image": image_url,
            "image_path": os.path.join(images_dir, f"{hotel_id}_{hotel_name}.jpg") if image_url else None
        }
    
    async def download_images(self, hotel_list):
        """
        Download hotel images asynchronously.
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for hotel in hotel_list:
                if hotel["image"] and hotel["image_path"]:
                    tasks.append(self.download_image(session, hotel["image"], hotel["image_path"]))
            await asyncio.gather(*tasks)

    async def download_image(self, session, url, path):
        """
        Download a single image asynchronously.
        """
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(path, 'wb') as f:
                        f.write(await response.read())
                    self.logger.info(f"Image saved: {path}")
                else:
                    self.logger.warning(f"Failed to download image: {url}")
        except Exception as e:
            self.logger.error(f"Error downloading image {url}: {e}")

    def save_to_json(self, data, path):
        """
        Save hotel data to a JSON file.
        """
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving JSON to {path}: {e}")
