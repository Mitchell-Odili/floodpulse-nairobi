import os
import sys
import requests
import random
from pathlib import Path
from google.adk.tools import ToolContext

# Add the project root (3 levels up from tools/) to the system path
root_dir = Path(__file__).resolve().parents[3]
sys.path.append(str(root_dir))

# Now import utils directly
from utils import http_retry

@http_retry
def get_nairobi_pulse_tool(lat: float, lon: float, simulate: bool = False) -> dict:
    """
    Fetches real-time weather data or generates a simulation pulse.
    
    Args:
        lat (float): Latitude of the target location.
        lon (float): Longitude of the target location.
        simulate (bool): If True, ignores API and generates random rainfall (0-70mm).
        
    Returns:
        dict: Weather metrics and status strings.

    Raises:
        ConnectionError: If API key is missing or service is unreachable.
    """
    
    if simulate:
        current_rain = random.uniform(0, 70) 
    else:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise ConnectionError("Weather API Key Missing. Cannot fetch data.")
        
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            current_rain = data.get("rain", {}).get("1h", 0)
        except Exception as e:
            return {"error": f"API Connection Error: {str(e)}"}

    # Calculate Flash Index (Normalized to 0-1)
    flash_index = min(current_rain / 50.0, 1.0)
    
    # Determine Status
    if flash_index <= 0.2:
        status = "Low Pulse"
    elif flash_index <= 0.6:
        status = "Moderate Pulse"
    else:
        status = "Critical Pulse"
        
    return {
        "rain_mm_h": round(current_rain, 2),
        "flash_index": round(flash_index, 2),
        "status": status,
        "telemetry_type": "weather"
    }

def get_active_weather_pulse(tool_context: ToolContext):
    """
    Adapter: Uses injected ToolContext to safely retrieve mission 
    coordinates from the active session and calls the core weather tool.
    """
    # 1. Access the session object directly from the injected context
    metadata = tool_context.session.state
    
    lat = metadata.get("latitude")
    lon = metadata.get("longitude")
    
    if lat is None or lon is None:
        raise ValueError("Session metadata missing latitude/longitude for weather lookup.")
        
    # Call your original tool logic
    return get_nairobi_pulse_tool(lat, lon, simulate=False)