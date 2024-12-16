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

IMAGES_STORE = 'images'
# DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:my_password@localhost:5432/tripdb')
