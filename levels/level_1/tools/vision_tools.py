import io
import os
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

def analyze_terrain_tool(target_user: str, pulse_status: str) -> str:
    """
    Analyzes terrain map images to identify flood risks for a specific user.
    'target_user' should be the name of the person (e.g., 'Sarah').
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # 1. Normalize the filename to match files like 'sarah_mission_map.png'
    filename = f"{target_user.lower()}_mission_map.png"
    
    # 2. Locate asset dynamically
    # This assumes the file is in: project_root/levels/level_1/assets/maps/
    project_root = Path(__file__).resolve().parents[2]
    map_path = project_root / "levels" / "level_1" / "assets" / "maps" / filename
    
    # 3. Validation and Debugging
    if not map_path.exists():
        directory = map_path.parent
        # Returns a helpful error if the file isn't found
        return f"Error: Map for '{target_user}' not found. Expected: {filename} in {directory}"

    # 4. Prepare image for Gemini
    img = Image.open(map_path)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    
    # 5. Build prompt
    prompt = (
        f"Analyze the terrain map for {target_user}. "
        f"Current flood pulse status: {pulse_status}. "
        "Identify potential flood sumps and risk level."
    )
    
    # 6. Generate analysis
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_text(text=prompt),
            types.Part.from_bytes(data=img_byte_arr.getvalue(), mime_type="image/png")
        ]
    )
    
    return response.text