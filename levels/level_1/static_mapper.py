"""
Level 1: Terrain Discovery - Static Mapper
Worker module to fetch satellite tiles and overlay agent icons.
"""

import os
import requests
from PIL import Image
from dotenv import load_dotenv
from io import BytesIO

# Load API Key from .env (usually in the root folder)
load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# 📍 MISSION COORDINATES (T-Mall Underpass / Mbagathi Sump)
SARAH_LAT, SARAH_LON = -1.3148, 36.8115
ZOOM = 17 
SIZE = "640x640"

def fetch_basemap(lat, lon, zoom=16, size="640x640", filename="mbagathi_basemap.png"):
    """
    Fetches a satellite tile for specific coordinates.
    TPM Note: Defaulting to 16 zoom and 640px for consistency across the project.
    """
    print(f"🛰️ Requesting satellite tile for coords: {lat}, {lon}...")
    
    url = (
        f"https://maps.googleapis.com/maps/api/staticmap?"
        f"center={lat},{lon}&zoom={zoom}&size={size}"
        f"&maptype=satellite&key={API_KEY}"
    )
    
    try:
        response = requests.get(url)
        response.raise_for_status() # TPM Best Practice: Catch HTTP errors early
        
        img = Image.open(BytesIO(response.content))
        
        # Ensure we save in the correct directory (Level 1)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_dir, filename)
        
        img.save(save_path)
        print(f"✓ Basemap saved: {filename}")
        return img
        
    except Exception as e:
        print(f"❌ Error fetching map: {e}")
        return None

    
def overlay_agent_icon(basemap, agent_name="sarah"):
    # 1. Get the directory where THIS script is (levels/level_1)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Go UP one level to reach the 'levels' folder
    levels_parent_dir = os.path.dirname(script_dir)
    
    # 3. Construct path directly into level_0/assets/maps/
    # Path becomes: levels/level_0/assets/maps/sarah_icon.png
    icon_path = os.path.join(levels_parent_dir, "level_0", "assets", "maps", f"{agent_name}_icon.png")
    
    print(f"🔍 Searching for icon at: {icon_path}")

    if not os.path.exists(icon_path):
        print(f"❌ Still missing! System tried to find it here: {icon_path}")
        # Final Debug: Let's see what is actually in that folder
        if os.path.exists(levels_parent_dir):
            print(f"📂 Folders found inside 'levels': {os.listdir(levels_parent_dir)}")
        return

    # 4. Success - Process the image
    icon = Image.open(icon_path).convert("RGBA")
    icon = icon.resize((64, 64)) 

    # Stamp Sarah at the center (320-32 = 288)
    pos = (288, 288)
    basemap.paste(icon, pos, icon)
    
    # Save the output in the level_1 folder
    output_path = os.path.join(script_dir, f"{agent_name}_on_mission.png")
    basemap.save(output_path)
    print(f"🚀 SUCCESS! Mission Map Ready: {output_path}")

            
if __name__ == "__main__":
    print("\n🌊 FLOODPULSE: TACTICAL SPREAD DEPLOYMENT...")
    print("-------------------------------------------")

    # 1. Define the Trinity's unique coordinates
    locations = {
        "sarah": {"lat": -1.3148, "lon": 36.8115}, # Sump
        "juma":  {"lat": -1.3165, "lon": 36.8135}, # Arterial
        "kamau": {"lat": -1.3110, "lon": 36.8185}  # Ridge
    }

    # 2. Iterate and Generate
    for agent, coords in locations.items():
        print(f"📡 Sector Update: Fetching terrain for {agent.upper()}...")
        
        # Fetch a UNIQUE basemap for each agent's specific location
        # Filename is mission-specific so we don't overwrite the master
        agent_tile = fetch_basemap(
            coords['lat'], 
            coords['lon'], 
            filename=f"{agent}_basemap_tile.png"
        )

        if agent_tile:
            overlay_agent_icon(agent_tile, agent_name=agent)
        else:
            print(f"⚠️ Warning: Could not establish visual for {agent.upper()}")

    print("-------------------------------------------")
    print("✅ TACTICAL SPREAD COMPLETE. 3 unique sectors established.")