import os
from scrapy.pipelines.images import ImagesPipeline
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from trip.db.models import Base, Hotel

class TripPipeline:
    def __init__(self):
        engine = create_engine(os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/tripdb'))
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        hotel = Hotel(
            title=item['title'],
            rating=float(item['rating']) if item['rating'] else None,
            location=item['location'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            room_type=item['room_type'],
            price=item['price'],
            image_path=item['image_paths'][0] if item['image_paths'] else None
        )
        session.add(hotel)
        session.commit()
        session.close()
        return item

class TripImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return f"images/{os.path.basename(request.url)}"

    def item_completed(self, results, item, info):
        item['image_paths'] = [x['path'] for ok, x in results if ok]
        return item
