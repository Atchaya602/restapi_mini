from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import extract
from datetime import datetime
import os

from db import SessionLocal
from models import WeatherData

app = FastAPI(title="Delhi Weather API")

# Database connection dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to the Delhi Weather API!"}

# Weather API endpoint
@app.get("/weather/")
def get_weather(date: str = None, month: int = None, db: Session = Depends(get_db)):
    query = db.query(WeatherData)

    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}
        data = query.filter(WeatherData.date == date_obj).all()

    elif month:
        data = query.filter(extract('month', WeatherData.date) == month).all()
    else:
        return {"error": "Please provide either a date (YYYY-MM-DD) or month (1–12)."}

    if not data:
        return {"message": "No data found for the given input."}

    return [
        {
            "date": record.date,
            "temperature": record.temperature,
            "humidity": record.humidity,
            "pressure": record.pressure,
            "heat_index": record.heat_index
        }
        for record in data
    ]

# Serve HTML directly (no Jinja2)
@app.get("/ui")
def serve_ui():
    file_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    return FileResponse(file_path)
