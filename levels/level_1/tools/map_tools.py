import os
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

# Pathing setup
PROJECT_ROOT = Path(__file__).resolve().parents[3]
BASEMAPS_DIR = PROJECT_ROOT / "levels" / "level_1" / "assets" / "basemaps"
MAPS_DIR = PROJECT_ROOT / "levels" / "level_1" / "assets" / "maps"
ICONS_DIR = PROJECT_ROOT / "levels" / "level_0" / "outputs"

# Ensure directories exist upon import
for directory in [BASEMAPS_DIR, MAPS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

def fetch_basemap(lat: float, lon: float, filename: Path, zoom: int = 17):
    """Fetches satellite tile from Google Maps."""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY not found in environment.")
        
    url = (
        f"https://maps.googleapis.com/maps/api/staticmap?"
        f"center={lat},{lon}&zoom={zoom}&size=640x640"
        f"&maptype=satellite&key={api_key}"
    )
    response = requests.get(url)
    response.raise_for_status()
    
    img = Image.open(BytesIO(response.content))
    img.save(filename)
    return img

def generate_mission_map(responder_name: str, lat: float, lon: float, zoom: int = 17):
    """
    Generates a map image with an overlaid icon for a mission location.
    """
    # Normalize name to lowercase for filesystem consistency
    safe_name = responder_name.lower()
    
    tile_path = BASEMAPS_DIR / f"{safe_name}_basemap.png"
    map_path = MAPS_DIR / f"{safe_name}_mission_map.png"
    icon_path = ICONS_DIR / f"{safe_name}_icon.png"

    # Idempotency: Return existing map if it exists
    if map_path.exists():
        return str(map_path)

    # Fetch fresh satellite data
    basemap = fetch_basemap(lat, lon, tile_path, zoom)
    
    # Overlay icon (if exists)
    if icon_path.exists():
        icon = Image.open(icon_path).convert("RGBA").resize((64, 64))
        # Center coordinates for a 640x640 map: (640-64)/2 = 288
        basemap.paste(icon, (288, 288), icon)
    
    basemap.save(map_path)
    return str(map_path)