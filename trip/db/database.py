from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .models import Base

# Replace credentials with your PostgreSQL details
DATABASE_URL = "postgresql+psycopg2://username:password@db:5432/hotel_db"

# Initialize the database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create Database Engine and Base
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Base = declarative_base()
def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)