from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MySQL connection string format: mysql+pymysql://username:password@localhost:3306/database_name
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:ngs123@localhost:3306/fastapi_todo")

# Add connection pool settings for better performance and error handling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    pool_size=5,         # Number of connections to maintain
    max_overflow=10      # Additional connections beyond pool_size
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()