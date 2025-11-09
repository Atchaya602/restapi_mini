import pandas as pd
from sqlalchemy.orm import Session
from db import SessionLocal
from models import WeatherData
import math

# 1️⃣ Read the CSV file
df = pd.read_csv(r"C:\Users\Administrator\Downloads\weather_project\weather_data.csv")

# 2️⃣ Clean column names
df.columns = [col.strip().lower() for col in df.columns]

# 3️⃣ Rename columns to match our model
df = df.rename(columns={
    'datetime_utc': 'date',
    '_tempm': 'temperature',
    '_hum': 'humidity',
    '_pressurem': 'pressure',
    '_heatindexm': 'heat_index',
    '_conds': 'condition'
})

# 4️⃣ Convert and clean data
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])  # Drop invalid dates

# Replace NaN or None values with defaults
df['temperature'] = df['temperature'].fillna(0)
df['humidity'] = df['humidity'].fillna(0)
df['pressure'] = df['pressure'].fillna(0)
df['heat_index'] = df['heat_index'].fillna(0)
df['condition'] = df['condition'].fillna('Unknown')

# 5️⃣ Insert data into database
session = SessionLocal()

try:
    for _, row in df.iterrows():
        weather_entry = WeatherData(
            date=row['date'].date(),
            temperature=float(row['temperature']) if not math.isnan(row['temperature']) else 0.0,
            humidity=float(row['humidity']) if not math.isnan(row['humidity']) else 0.0,
            pressure=float(row['pressure']) if not math.isnan(row['pressure']) else 0.0,
            heat_index=float(row['heat_index']) if not math.isnan(row['heat_index']) else 0.0,
            # condition removed if not in model
        )
        session.add(weather_entry)
    session.commit()
    print("✅ Data inserted successfully!")
except Exception as e:
    session.rollback()
    print("❌ Error inserting data:", e)
finally:
    session.close()
