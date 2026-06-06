import os
import requests
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent

# --- PATH & ENV RESOLUTION ---
def load_project_env():
    """Finds the .env file in the project root and loads it."""
    current_path = Path(__file__).resolve()
    for parent in [current_path] + list(current_path.parents):
        env_file = parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            return True
    return False

load_project_env()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

class WeatherGatherer(Agent):
    def __init__(self):
        super().__init__(
            name="WeatherGatherer",
            description="Fetches real-time weather data for specific coordinates in Nairobi and calculates flash flood risk.",
        )

    def get_flash_status(self, index):
        """Translates the numerical Flash Index into a Strategic Alert."""
        if index <= 0.2:
            return "🟢 Low Pulse (Steady Rains - Safe for now)"
        elif index <= 0.6:
            return "🟡 Moderate Pulse (Clogged Drain Risk - Avoid Sumps)"
        else:
            return "🔴 Critical Pulse (Flash Flood Imminent - MOVE TO RIDGE)"

    def execute(self, inputs: dict) -> dict:
        """
        Fetches real-time weather and calculates risk for a specific Node.
        Expects inputs: {'name': str, 'lat': float, 'lon': float}
        """
        name = inputs.get("name")
        lat = inputs.get("lat")
        lon = inputs.get("lon")

        if not API_KEY:
            return {"error": "API Key Missing from .env"}

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            # Extract Rain (mm in the last hour)
            current_rain = data.get("rain", {}).get("1h", 0)
            
            # Calculate Flash Index
            flash_index = min(current_rain / 50.0, 1.0)
            status = self.get_flash_status(flash_index)
            
            return {
                "node": name,
                "rain_mm_h": current_rain,
                "flash_index": round(flash_index, 2),
                "status": status,
                "description": data.get("weather", [{}])[0].get("description", "clear sky")
            }
        except Exception as e:
            return {"error": str(e)}

# Export the instance for the orchestrator
weather_gatherer = WeatherGatherer()