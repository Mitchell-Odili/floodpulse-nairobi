import os
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from utils import http_retry
from google.adk.tools import ToolContext


# Pathing setup
PROJECT_ROOT = Path(__file__).resolve().parents[3]
BASEMAPS_DIR = PROJECT_ROOT / "levels" / "level_1" / "assets" / "basemaps"
MAPS_DIR = PROJECT_ROOT / "levels" / "level_1" / "assets" / "maps"
ICONS_DIR = PROJECT_ROOT / "levels" / "level_0" / "outputs"

# Ensure directories exist upon import
for directory in [BASEMAPS_DIR, MAPS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

@http_retry
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
    safe_name = responder_name.lower()
    tile_path = BASEMAPS_DIR / f"{safe_name}_basemap.png"
    map_path = MAPS_DIR / f"{safe_name}_mission_map.png"
    icon_path = ICONS_DIR / f"{safe_name}_icon.png"

    # 1. Return final map if already finished
    if map_path.exists():
        return str(map_path)

    # 2. Use existing basemap if it exists, otherwise fetch
    if tile_path.exists():
        basemap = Image.open(tile_path)
    else:
        basemap = fetch_basemap(lat, lon, tile_path, zoom)
    
    # 3. Overlay icon
    if icon_path.exists():
        icon = Image.open(icon_path).convert("RGBA").resize((64, 64))
        basemap.paste(icon, (288, 288), icon)
    
    basemap.save(map_path)
    return str(map_path)

    
def generate_active_mission_map(tool_context: ToolContext, zoom: int = 17):
    """
    ADAPTER FUNCTION: The 'Auto' logic.
    Uses ToolContext to pull data from the session and calls the Core function.
    """
    # Pulling from session metadata via injected tool_context
    metadata = tool_context.session.metadata
    
    responder = metadata.get("responder_name")
    lat = metadata.get("latitude")
    lon = metadata.get("longitude")
    
    if not all([responder, lat, lon]):
        raise ValueError("Missing session metadata: Ensure responder_name, lat, and lon are set.")
    
    # Hand-off to the Core function
    return generate_mission_map(responder, lat, lon, zoom=zoom)