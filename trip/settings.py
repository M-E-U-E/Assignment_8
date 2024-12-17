import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

BOT_NAME = 'trip'

SPIDER_MODULES = ['trip.spiders']
NEWSPIDER_MODULE = 'trip.spiders'

# ITEM_PIPELINES = {
#     'trip.pipelines.TripPipeline': 300,
#     'trip.pipelines.TripImagesPipeline': 1,
# }
# FEEDS = {
#     'json_of_hotels/%(name)s.json': {
#         'format': 'json',
#         'encoding': 'utf8',
#         'indent': 4,
#     }
# }
ITEM_PIPELINES = {
    'trip.pipelines.HotelImagesPipeline': 1,  # Handles image downloading
    'trip.pipelines.PostgresPipeline': 300,   # Handles database storage
}

IMAGES_STORE = 'city_data/images_of_hotels'
# DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:my_password@localhost:5432/tripdb')

# Duplicate filter for images
IMAGES_EXPIRES = 90  # Days to retain images

# Database Connection
DATABASE_URL = 'postgresql://username:password@db:5432/hotel_db' 