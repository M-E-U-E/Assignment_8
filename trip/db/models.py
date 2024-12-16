from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    rating = Column(Float, nullable=True)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    room_type = Column(String, nullable=False)
    price = Column(String, nullable=False)
    image_path = Column(String, nullable=False)
