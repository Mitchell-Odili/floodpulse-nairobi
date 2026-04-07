import os
import requests
import sys
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_flash_status(index):
    """
    Translates the numerical Flash Index into a Strategic Alert.
    """
    if index <= 0.2:
        return "🟢 Low Pulse (Steady Rains - Safe for now)"
    elif index <= 0.6:
        return "🟡 Moderate Pulse (Clogged Drain Risk - Avoid Sumps)"
    else:
        return "🔴 Critical Pulse (Flash Flood Imminent - MOVE TO RIDGE)"

def get_nairobi_pulse(name, lat, lon):
    """
    Fetches real-time weather and calculates risk for a specific Node.
    """
    if not API_KEY:
        return {"error": "API Key Missing from .env"}

    # OpenWeather Current Weather API
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # 1. Extract Rain (mm in the last hour)
        # OpenWeather only includes 'rain' key if it is currently raining
        current_rain = data.get("rain", {}).get("1h", 0)
        
        # 2. Calculate Flash Index (0.0 to 1.0)
        # We normalize against 50mm/h (extreme tropical downpour)
        flash_index = min(current_rain / 50.0, 1.0)
        
        # 3. Get Human-Readable Status
        status = get_flash_status(flash_index)
        
        # print(f"📍 Node: {name:15} | 🌧️ {current_rain:4}mm/h | {status}")
        print(f"DEBUG: Checking {name}", file=sys.stderr)
        
        return {
            "node": name,
            "rain_mm_h": current_rain,
            "flash_index": round(flash_index, 2),
            "status": status,
            "description": data.get("weather", [{}])[0].get("description", "clear sky")
        }
    except Exception as e:
        # print(f"❌ Error fetching {name}: {e}")
        return None

if __name__ == "__main__":
    # The Trinity: Mission-Critical Deployment Nodes
    nodes = [
        {"name": "Sarah (Sump)", "lat": -1.3148, "lon": 36.8115},
        {"name": "Juma (Arterial)", "lat": -1.3165, "lon": 36.8135},
        {"name": "Kamau (Ridge)", "lat": -1.3110, "lon": 36.8185}
    ]

    # print("🛰️  INITIATING MBAGATHI BASIN PULSE CHECK...")
    # print("-" * 65)
    
    basin_results = []
    for node in nodes:
        result = get_nairobi_pulse(node["name"], node["lat"], node["lon"])
        if result:
            basin_results.append(result)
    
    # print("-" * 65)
    # print(f"✅ Level 2: {len(basin_results)} Nodes Synced.")