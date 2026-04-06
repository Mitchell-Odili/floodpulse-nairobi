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

def fetch_basemap():
    """Fetches the satellite tile and saves it locally in Level 1."""
    print(f"🛰️ Requesting satellite tile for Mbagathi Basin...")
    
    url = (
        f"https://maps.googleapis.com/maps/api/staticmap?"
        f"center={SARAH_LAT},{SARAH_LON}&zoom={ZOOM}&size={SIZE}"
        f"&maptype=satellite&key={API_KEY}"
    )
    
    response = requests.get(url)
    if response.status_code == 200:
        # Save map inside the current level_1 folder
        img = Image.open(BytesIO(response.content))
        img.save("mbagathi_basemap.png")
        print("✓ Basemap saved locally in Level 1.")
        return img
    else:
        print(f"❌ Error fetching map: {response.text}")
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
    if not API_KEY:
        print("❌ API Key missing! Check your .env file.")
    else:
        mbagathi_map = fetch_basemap()
        if mbagathi_map:
            overlay_agent_icon(mbagathi_map, "sarah")