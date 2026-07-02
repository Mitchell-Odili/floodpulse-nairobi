import os
import json
from pathlib import Path
from PIL import Image
from config import MODELS
from utils import http_retry
from google.genai import Client
from google.adk.tools import ToolContext

@http_retry
def analyze_terrain_tool(tool_context: ToolContext) -> dict:
    """
    Adapter: Retrieves responder info and performs structured terrain analysis.
    """
    # 1. Identity Resolution
    metadata = tool_context.session.state
    raw_responder_name = metadata.get("responder_name")

    if not raw_responder_name:
        raise ValueError("Session metadata missing 'responder_name'.")

    # Force lowercase for consistent file lookups
    responder_name = raw_responder_name.lower()

    # 2. Robust File Resolution
    # Resolve the path to the assets folder using absolute path navigation
    # This assumes structure: .../levels/level_1/tools/analyze_terrain.py
    # And maps are at:       .../levels/level_1/assets/maps/
    script_dir = Path(__file__).resolve().parent
    map_path = (script_dir.parent / "assets" / "maps" / f"{responder_name}_mission_map.png").resolve()

    if not map_path.exists():
        raise FileNotFoundError(f"Map for {responder_name} not found at {map_path}. Please verify the file exists.")

    # 3. Vision Processing
    client = Client(
        vertexai=True,
        project=os.getenv("PROJECT_ID"),
        location=os.getenv("LOCATION")
    )

    model_name = MODELS["vision_model"]

    with Image.open(map_path) as img:
        prompt = (
            "Analyze this terrain map. Identify the hazard level ('Low', 'Vulnerable', 'High-Risk'), "
            "estimate slope percentage (float), list detected obstacles, and provide a single-sentence "
            "evacuation bearing. Return valid JSON ONLY with these exact keys: "
            "'terrain_hazard', 'slope_percentage', 'obstacles', 'evacuation_advice'."
        )
        
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt, img]
        )

    # 4. Data Extraction
    try:
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(json_text)
    except Exception as e:
        raise ValueError(f"Failed to parse terrain analysis as JSON: {str(e)}")