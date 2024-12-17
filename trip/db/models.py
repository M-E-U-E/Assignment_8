from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text,create_engine # Import Text explicitly

Base = declarative_base()

class Hotel(Base):

    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String, nullable=False)
    property_title = Column(String, nullable=False)
    hotel_id = Column(String, unique=True, nullable=False)
    price = Column(Float)
    rating = Column(Float)
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(String)
    image = Column(String)
    image_path = Column(String, nullable=True)
