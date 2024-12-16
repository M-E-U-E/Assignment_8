import scrapy
import json
import re
import random
import os
import requests


class RandomHotelSpider(scrapy.Spider):
    name = "trip"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Extract and parse `window.IBU_HOTEL` data using CSS selectors
        script_data = response.css("script::text").re_first(r"window\.IBU_HOTEL\s*=\s*(\{.*?\});")
        if script_data:
            try:
                # Parse the JSON data
                ibu_hotel_data = json.loads(script_data)
                
                # Extract cities from `initData.htlsData`
                inbound_cities = ibu_hotel_data.get("initData", {}).get("htlsData", {}).get("inboundCities", [])
                outbound_cities = ibu_hotel_data.get("initData", {}).get("htlsData", {}).get("outboundCities", [])
                cities_to_search = inbound_cities + outbound_cities  # Combine both lists
                
                # Randomly select 3 cities
                if len(cities_to_search) < 3:
                    self.logger.warning("Not enough cities to choose 3.")
                    return
                
                selected_cities = random.sample(cities_to_search, 3)

                # Iterate through the 3 selected cities
                for city in selected_cities:
                    city_name = city.get("name", "Unknown")
                    city_id = city.get("id", "")
                    
                    if not city_id:
                        self.logger.warning(f"No ID found for city: {city_name}")
                        continue
                    
                    # Construct URL for the city's hotel list page
                    city_hotels_url = f"https://uk.trip.com/hotels/list?city={city_id}"
                    yield scrapy.Request(
                        url=city_hotels_url,
                        callback=self.parse_city_hotels,
                        meta={'city_name': city_name, 'city_id': city_id}
                    )
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON: {e}")
            except Exception as e:
                self.logger.error(f"An unexpected error occurred: {e}")

    def parse_city_hotels(self, response):
        # Extract and parse `window.IBU_HOTEL` data from city hotels page using CSS selectors
        script_data = response.css("script::text").re_first(r"window\.IBU_HOTEL\s*=\s*(\{.*?\});")
        city_name = response.meta.get('city_name', 'Unknown')

        # Folder for JSON and images
        output_folder = os.path.join(os.getcwd(), 'city_data')
        images_dir = os.path.join(output_folder, 'images_of_hotels', city_name.lower().replace(' ', '_'))
        os.makedirs(images_dir, exist_ok=True)

        # JSON file folder
        json_folder = os.path.join(output_folder, 'json_of_hotels')
        os.makedirs(json_folder, exist_ok=True)

        city_json_path = os.path.join(json_folder, f"{city_name.lower().replace(' ', '_')}.json")
        city_hotels = []

        if script_data:
            try:
                # Parse the JSON data
                ibu_hotel_data = json.loads(script_data)

                # Extract hotel list from initData.firstPageList.hotelList
                hotel_list = ibu_hotel_data.get("initData", {}).get("firstPageList", {}).get("hotelList", [])

                # Process and save hotel data
                for hotel in hotel_list:
                    hotel_id = hotel.get("hotelBasicInfo", {}).get("hotelId", "")
                    hotel_name = hotel.get("hotelBasicInfo", {}).get("hotelName", "").replace(" ", "_")
                    image_url = hotel.get("hotelBasicInfo", {}).get("hotelImg", "")
                    
                    # Prepare hotel info
                    hotel_info = {
                        "city_name": city_name,
                        "property_title": hotel.get("hotelBasicInfo", {}).get("hotelName", ""),
                        "hotel_id": hotel_id,
                        "price": hotel.get("hotelBasicInfo", {}).get("price", ""),
                        "rating": hotel.get("commentInfo", {}).get("commentScore", ""),
                        "address": hotel.get("positionInfo", {}).get("positionName", ""),
                        "latitude": hotel.get("positionInfo", {}).get("coordinate", {}).get("lat", ""),
                        "longitude": hotel.get("positionInfo", {}).get("coordinate", {}).get("lng", ""),
                        "room_type": hotel.get("roomInfo", {}).get("physicalRoomName", ""),
                        "image": image_url
                    }

                    # Download and save the image
                    if image_url:
                        try:
                            image_filename = f"{hotel_id}_{hotel_name}.jpg"
                            image_path = os.path.join(images_dir, image_filename)
                            response_img = requests.get(image_url)
                            if response_img.status_code == 200:
                                with open(image_path, 'wb') as f:
                                    f.write(response_img.content)
                                hotel_info['local_image_path'] = os.path.relpath(image_path, output_folder)
                                self.logger.info(f"Image saved: {image_path}")
                            else:
                                self.logger.warning(f"Failed to download image: {image_url}")
                        except Exception as e:
                            self.logger.error(f"Error downloading image for {hotel_name}: {e}")

                    city_hotels.append(hotel_info)

                # Save the city data into a JSON file
                with open(city_json_path, 'w', encoding='utf-8') as f:
                    json.dump(city_hotels, f, indent=4, ensure_ascii=False)
                self.logger.info(f"Data saved for city {city_name} in {city_json_path}")

            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON: {e}")
            except Exception as e:
                self.logger.error(f"An unexpected error occurred: {e}")
        else:
            self.logger.warning(f"No script data found for city: {city_name}")
