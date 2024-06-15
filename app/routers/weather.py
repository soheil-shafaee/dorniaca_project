from fastapi import status, APIRouter, HTTPException
from datetime import datetime, timedelta
from ..config.config import settings
import requests
import pandas as pd

location = "sari"
start_date = datetime(2024, 6, 11)
days = 90

router = APIRouter(prefix="/bot", tags=["Weather"])

@router.get("/")
async def get_weather():
    """
    Retrieve weather information for a specific location over a period of time.

    Returns:
    - A dictionary containing weather information for each day over the specified period.
    """
    weather_dict = {}
    for day in range(days):
        date = (start_date + timedelta(days=day)).strftime('%Y-%m-%d')
        url = f"http://api.weatherapi.com/v1/current.json?key={settings.api_key}&q={location}&aqi=no&dt={date}"
        response = requests.get(url)
        weather_dict[date] = response.json()["current"]
    df= pd.DataFrame.from_dict(weather_dict, orient="index")
    df= df.reset_index().rename(columns={"index":"Date"})
    df.to_csv("time.csv",  encoding="utf-8")
    return weather_dict