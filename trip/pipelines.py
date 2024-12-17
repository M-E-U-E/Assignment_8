import os
from scrapy.pipelines.images import ImagesPipeline
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from trip.db.models import Base, Hotel
from .db.database import engine, SessionLocal, init_db   # Import engine and session
from sqlalchemy.exc import IntegrityError
# class TripPipeline:
#     def __init__(self):
#         engine = create_engine(os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/tripdb'))
#         Base.metadata.create_all(engine)
#         self.Session = sessionmaker(bind=engine)

#     def process_item(self, item, spider):
#         session = self.Session()
#         hotel = Hotel(
#             title=item['title'],
#             rating=float(item['rating']) if item['rating'] else None,
#             location=item['location'],
#             latitude=item['latitude'],
#             longitude=item['longitude'],
#             room_type=item['room_type'],
#             price=item['price'],
#             image_path=item['image_paths'][0] if item['image_paths'] else None
#         )
#         session.add(hotel)
#         session.commit()
#         session.close()
#         return item

# class TripImagesPipeline(ImagesPipeline):
#     def file_path(self, request, response=None, info=None, *, item=None):
#         return f"images/{os.path.basename(request.url)}"

#     def item_completed(self, results, item, info):
#         item['image_paths'] = [x['path'] for ok, x in results if ok]
#         return item

# class TripImagesPipeline(ImagesPipeline):
#     def file_path(self, request, response=None, info=None, *, item=None):
#         # Custom image file path
#         return f"images/{os.path.basename(request.url)}"

#     def item_completed(self, results, item, info):
#         # Store downloaded image paths
#         item['image_path'] = [x['path'] for ok, x in results if ok][0] if results else None
#         return item

class HotelImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # Generate a file path for each image
        city_name = item.get("city_name", "unknown").lower().replace(" ", "_")
        hotel_name = item.get("property_title", "hotel").lower().replace(" ", "_")
        filename = f"{hotel_name}_{os.path.basename(request.url)}"
        return f"images/{city_name}/{filename}"

    def item_completed(self, results, item, info):
        # Retrieve and store the image path
        image_paths = [x["path"] for ok, x in results if ok]
        if image_paths:
            item["image_path"] = image_paths[0]  # Store the first image path
        return item

class PostgresPipeline:
    def __init__(self):
        # Create tables if they don't exist
        init_db()
        # Hotel.metadata.create_all(bind=engine)

    def open_spider(self, spider):
        # Open a database session
        print("Database session opened.")
        self.session = SessionLocal()
        

    def close_spider(self, spider):
        # Close the database session
        print("Database session Closed.")
        self.session.close()
        
    def process_item(self, item, spider):
        try:
            hotel = Hotel(
                city_name=item.get("city_name"),
                property_title=item.get("property_title"),  # Use 'property_title' to match the model
                hotel_id=item.get("hotel_id"),
                price=float(item.get("price", 0.0)) if item.get("price") else None,  # Validate price
                rating=float(item.get("rating", 0.0)) if item.get("rating") else None,  # Validate rating
                address=item.get("address"),
                latitude=float(item.get("latitude", 0.0)) if item.get("latitude") else None,  # Validate latitude
                longitude=float(item.get("longitude", 0.0)) if item.get("longitude") else None,  # Validate longitude
                room_type=item.get("room_type"),
                image=item.get("image"),
                image_path=item.get("image_path"),
            )
            self.session.add(hotel)
            self.session.commit()
            spider.logger.info(f"Hotel data saved: {hotel}")
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Failed to save hotel: {e}")
        finally:
            self.session.close()
        return item

    # def process_item(self, item, spider):
    #     # Map incoming Scrapy data to Hotel model fields
    #     hotel = Hotel(
    #         title=item.get("property_title"),  # Maps 'property_title' to 'title'
    #         city_name=item.get("city_name"),
    #         hotel_id=item.get("hotel_id"),
    #         price=float(item.get("price", 0.0)),
    #         rating=float(item.get("rating", 0.0)),
    #         location=item.get("address"),  # Maps 'address' to 'location'
    #         latitude=float(item.get("latitude", 0.0)),
    #         longitude=float(item.get("longitude", 0.0)),
    #         room_type=item.get("room_type"),
    #         image_url=item.get("image"),
    #         image_path=item.get("image_path"),
    #     )
    #     try:
    #         self.session.add(hotel)
    #         self.session.commit()
    #         print(f"Item inserted successfully: {item}")
    #     except IntegrityError:
    #         self.session.rollback()  # Handle duplicates
    #     return item
        # # Add and commit the hotel instance to the database
        # self.session.add(hotel)
        # self.session.commit()
        # return item
