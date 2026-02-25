from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.tools import tool
from datetime import datetime   
import pytz
from utils.date_time_expression import city_to_timezone

class DateTimeInput(BaseModel):
    """Input schema for date/time tools."""
    location: str = Field(
        description="City or country name like Mumbai, Paris, India, USA"
    )


@tool(args_schema=DateTimeInput)
def get_current_datetime(location: str) -> str:
    """
    Get current date and time for a given city or country.
    """

    print("\n🕒 DATETIME TOOL EXECUTED\n")

    tz_name = city_to_timezone(location)
    if tz_name is None:
        return f"Invalid or unknown location: {location}"

    try:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)

        print(now.strftime("%Y-%m-%d %H:%M:%S %Z"))

        return now.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return "Error retrieving time"

