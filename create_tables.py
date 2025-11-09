# create_tables.py
from db import Base, engine
from models import WeatherData

print("⏳ Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
