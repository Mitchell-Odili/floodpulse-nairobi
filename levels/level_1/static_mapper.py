"""
FloodPulse Nairobi - Level 1: Terrain Discovery (Static Mapper)
Orchestrates mission map generation using a dedicated asset pipeline.
"""

import os
import json
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# 1. Pathing Setup
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Level 0 Assets (Personas)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "levels", "level_0", "outputs")
# Level 1 Assets (New Directory Structure)
BASEMAPS_DIR = os.path.join(os.path.dirname(__file__), "assets", "basemaps")
MAPS_DIR = os.path.join(os.path.dirname(__file__), "assets", "maps")

# Ensure sub-directories exist
os.makedirs(BASEMAPS_DIR, exist_ok=True)
os.makedirs(MAPS_DIR, exist_ok=True)

# Load API Key
load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def fetch_basemap(lat, lon, filename):
    """Fetches high-resolution satellite tile for Mbagathi Basin."""
    if not API_KEY:
        raise ValueError("❌ Missing GOOGLE_MAPS_API_KEY. Check your .env file!")
        
    print(f"🛰️ Requesting terrain tile: {lat}, {lon}...")
    
    url = (
        f"https://maps.googleapis.com/maps/api/staticmap?"
        f"center={lat},{lon}&zoom=17&size=640x640"
        f"&maptype=satellite&key={API_KEY}"
    )
    
    response = requests.get(url)
    response.raise_for_status()
    
    img = Image.open(BytesIO(response.content))
    img.save(filename)
    return img

def overlay_agent_icon(basemap, agent_name, output_filename):
    """Stamps the responder identity icon onto the terrain map."""
    icon_path = os.path.join(ASSETS_DIR, f"{agent_name}_icon.png")
    
    if not os.path.exists(icon_path):
        print(f"❌ Missing asset: {icon_path}")
        return

    icon = Image.open(icon_path).convert("RGBA").resize((64, 64))
    
    # Overlay at center (288, 288)
    basemap.paste(icon, (288, 288), icon)
    basemap.save(output_filename)
    print(f"✅ Mission Map Ready: {output_filename}")

if __name__ == "__main__":
    print("\n🌊 FLOODPULSE: TERRAIN DISCOVERY MODE...")
    
    # Responder Locations
    responder_locations = {
        "sarah": {"lat": -1.3148, "lon": 36.8115},
        "juma": {"lat": -1.3165, "lon": 36.8135},
        "kamau": {"lat": -1.3110, "lon": 36.8185}
    }

    # Automatically discover available icons
    available_icons = [f.replace("_icon.png", "") for f in os.listdir(ASSETS_DIR) if f.endswith("_icon.png")]
    
    if not available_icons:
        print("❌ No responder icons found in level_0/outputs/. Run 'create_identity.py' first.")
    else:
        for agent in available_icons:
            coords = responder_locations.get(agent, {"lat": -1.3120, "lon": 36.8150})
            print(f"📡 Sector Sync: {agent.upper()}...")
            
            # Paths to new organized subdirectories
            tile_path = os.path.join(BASEMAPS_DIR, f"{agent}_basemap.png")
            map_path = os.path.join(MAPS_DIR, f"{agent}_mission_map.png")
            
            # Fetch & Overlay
            basemap = fetch_basemap(coords['lat'], coords['lon'], tile_path)
            overlay_agent_icon(basemap, agent, map_path)

    print("-------------------------------------------")
    print("🚀 Terrain discovery complete. Vision.mcp is ready to scan.")