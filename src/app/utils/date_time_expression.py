import re
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from rapidfuzz import fuzz


def is_datetime_query(query: str) -> bool:
    keywords = ["time now", "current time", "time in"]

    for key in keywords:
        if fuzz.partial_ratio(query, key) > 80:
            return True

    return False


def extract_location(query: str):
    query = query.lower()

    # Remove common time words
    cleaned = re.sub(r"(what|is|the|current|now|time|at|in|of|\?)", "", query)

    location = cleaned.strip()

    if not location:
        return None

    return location.title()


tf = TimezoneFinder()
geolocator = Nominatim(user_agent="timezone_app")


def city_to_timezone(city_name):
    location = geolocator.geocode(city_name)
    if not location:
        return None

    tz = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    return tz
