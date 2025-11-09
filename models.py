from sqlalchemy import Column, Integer, Float, String, DateTime
from db import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    heat_index = Column(Float)
    location = Column(String(50))
