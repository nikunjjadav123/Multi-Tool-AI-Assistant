import requests
import os
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


# Tool Input Schema
class WeatherInput(BaseModel):
    city: str = Field(..., description="City name e.g. Pune")
    country_code: str = Field(default=None, description="Country code e.g. IN, US")
    units: Optional[str] = Field(
        default="metric",
        description="Units: metric (°C), imperial (°F), standard (Kelvin)",
    )
    lang: Optional[str] = Field(
        default="en", description="Language for weather description"
    )


@tool(args_schema=WeatherInput)
def get_current_weather(
    city: str, country_code: str = None, units: str = "metric", lang: str = "en"
) -> str:
    """
    Get the current weather of any city.
    """
    location = f"{city},{country_code}" if country_code else city
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": API_KEY, "units": units, "lang": lang}

    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        if response.status_code != 200:
            return f"Weather API Error: {data.get('message', 'Unknown error')}"

        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        unit_symbol = (
            "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        )

        return (
            f"Weather in {location}:\n"
            f"Temperature: {temp}{unit_symbol} (feels like {feels}{unit_symbol})\n"
            f"Condition: {condition}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s"
        )

    except Exception as e:
        return f"Tool execution failed: {str(e)}"
