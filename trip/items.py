from sqlalchemy import Column, Integer, String, Float, Text
from .db.database import Base

# Define SQLAlchemy Hotel Table Model
class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)  # Changed to match 'property_title'
    city_name = Column(String, nullable=False)
    hotel_id = Column(String, unique=True, nullable=False)
    price = Column(Float)
    rating = Column(Float)
    location = Column(Text)  # Changed to match 'address'
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(String)
    image_url = Column(String)  # Matches 'image' from Scrapy
    image_path = Column(String)
