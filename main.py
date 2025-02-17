from fasthtml.common import *
import requests
from typing import Optional
import os

# Initialize app with proper CSS
app, rt = fast_app()

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
        return Div({"class": "center-screen"},
            H1("WEATHER DATA UNAVAILABLE", {"class": "big-text"}),
            P("Unable to fetch current weather information", {"class": "small-text"})
        )
    
    message = "IT'S SUNNY RIGHT NOW IN DELFT!" if cloud_coverage < 50 else "IT'S CLOUDY RIGHT NOW IN DELFT!"
    bg_color = "#fef9c3" if cloud_coverage < 50 else "#e5e7eb"  # Light yellow for sunny, light gray for cloudy
    
    return Div({"class": "center-screen", "style": f"background-color: {bg_color};"},
        H1(message, {"class": "big-text"}),
        P(f"{cloud_coverage}% cloud coverage", {"class": "small-text"})
    )

serve()
