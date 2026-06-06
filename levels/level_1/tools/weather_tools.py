import os
import requests

def get_nairobi_pulse_tool(lat: float, lon: float) -> dict:
    """
    Fetches real-time weather from OpenWeatherMap and calculates flash flood risk.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "API Key Missing"}

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    # Extract rain data (mm in the last hour)
    current_rain = data.get("rain", {}).get("1h", 0)
    
    # Calculate Flash Index
    flash_index = min(current_rain / 50.0, 1.0)
    
    # Determine Status
    if flash_index <= 0.2:
        status = "🟢 Low Pulse (Safe)"
    elif flash_index <= 0.6:
        status = "🟡 Moderate Pulse (Caution)"
    else:
        status = "🔴 Critical Pulse (MOVE TO RIDGE)"
        
    return {
        "rain_mm_h": current_rain,
        "flash_index": round(flash_index, 2),
        "status": status,
        "description": data.get("weather", [{}])[0].get("description", "clear")
    }