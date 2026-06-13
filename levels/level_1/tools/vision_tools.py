import os
import json
from PIL import Image
from config import MODELS
from utils import http_retry
from google import genai # for api calls
from google.genai import Client
from google.adk.tools import ToolContext


@http_retry
def analyze_terrain_tool(tool_context: ToolContext) -> dict:

    """
    Adapter: Uses injected ToolContext to retrieve responder info,  
    and perform structured terrain analysis. 
    
    Returns:
        dict: Structured terrain telemetry for schema mapping.
    """
    # 1. Identity Resolution: Use the injected tool_context
    metadata = tool_context.session.metadata
    responder_name = session.metadata.get("responder_name")

    if not responder_name:
        raise ValueError("Session metadata missing 'responder_name'.")

    # 2. File Resolution: Locate the map for the identified responder
    map_path = os.path.join(
        os.path.dirname(__file__), "..", "assets", "maps", 
        f"{responder_name}_mission_map.png"
    )

    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Map for {responder_name} not found at {map_path}")

    # 3. Vision Processing: Identify terrain features using the configured model
        
    # Using Application Default Credentials identity
    client = Client(   
        vertexai=True, 
        project=os.getenv("PROJECT_ID"), 
        location=os.getenv("LOCATION")
    )

    # client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))  # API call option 

    model_name = MODELS["vision_model"]

    with Image.open(map_path) as img:
        # Prompting for raw JSON return to satisfy the Pydantic schema
        prompt = (
            "Analyze this terrain map. Identify the hazard level ('Low', 'Vulnerable', 'High-Risk'), "
            "estimate slope percentage (float), list detected obstacles, and provide a single-sentence "
            "evacuation bearing. Return valid JSON ONLY with these exact keys: "
            "'terrain_hazard', 'slope_percentage', 'obstacles', 'evacuation_advice'."
        )
        
        response = client.models.generate_content(
            model=model_name,  # Configurable
            contents=[prompt, img]
        )


    # 4. Data Extraction: Parse the model's text into a dictionary
    try:
        # Clean response if the model included markdown blocks
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(json_text)
    except Exception as e:
        raise ValueError(f"Failed to parse terrain analysis as JSON: {str(e)}")
