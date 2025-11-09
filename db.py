# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL connection URL format:
# mysql+pymysql://<username>:<password>@<host>/<database_name>
DATABASE_URL = "mysql+pymysql://root:2105@localhost:3306/weather_db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session for interacting with DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
