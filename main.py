from fasthtml.common import *
import requests
from typing import Optional
import os

app, rt = fast_app(live=True)

def get_delft_sunniness_data() -> Optional[float]:
    """Get current cloud coverage data for Delft, Netherlands using Open-Meteo API.
    
    Returns:
        Optional[float]: Cloud coverage percentage (0-100) if successful, None if failed
    """
    # Delft coordinates
    lat = 52.00667
    lon = 4.35556
    
    # Call Open-Meteo API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=cloud_cover"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('current', {}).get('cloud_cover')  # Cloud coverage percentage
        return None
    except Exception:
        return None


@rt("/")
def get():
    cloud_coverage = get_delft_sunniness_data()
    if cloud_coverage is None:
        return Div(P("Unable to fetch weather data for Delft"))
    elif cloud_coverage < 50:  # Less than 50% cloud coverage is considered sunny
        return Div(P(f"Hello sunny Delft! (Cloud coverage: {cloud_coverage}%)"))
    else:
        return Div(P(f"Hello cloudy Delft! (Cloud coverage: {cloud_coverage}%)"))


serve()
