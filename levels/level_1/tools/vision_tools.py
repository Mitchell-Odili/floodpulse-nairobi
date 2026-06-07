import os
from google import genai
from google.genai import types
from PIL import Image
# Import your centralized config
from config import MODELS 

def analyze_terrain_tool(target_user: str) -> str:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Use the configured model instead of a hardcoded string
    model_name = MODELS["vision_model"] 
    
    map_path = os.path.join(os.path.dirname(__file__), "..", "assets", "maps", f"{target_user}_mission_map.png")
    
    if not os.path.exists(map_path):
        return "TERRAIN STATUS: Unknown | Details: Map file not found."

    with Image.open(map_path) as img:
        prompt = (
            f"Analyze this terrain map for {target_user}. "
            "Identify risk level as 'Stable', 'Vulnerable', or 'High-Risk'. "
            "Output format: 'TERRAIN STATUS: [Category] | Reason: [Brief explanation]'"
        )
        
        response = client.models.generate_content(
            model=model_name, # Configurable
            contents=[prompt, img]
        )
    
    return response.text