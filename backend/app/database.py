import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load .env file
load_dotenv()

# Get database URL from .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if DATABASE_URL is None and raise an error if it is
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set.")


# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(

    autocommit=False, 
    autoflush=False, 
    bind=engine

)

# Create a base class for declarative models
Base = declarative_base()

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()