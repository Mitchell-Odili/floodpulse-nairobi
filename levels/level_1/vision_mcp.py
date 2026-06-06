import os
import sys
import logging
from mcp.server.fastmcp import FastMCP
from google import genai
from PIL import Image
from dotenv import load_dotenv

import warnings
import sys

# --- LOGGING SETUP ---
# Redirect logging to sys.stderr to keep stdout reserved for MCP communication
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("FloodPulse-Vision")

# --- PATH SHIELD ---
# Sets PROJECT_ROOT to the root directory regardless of where this file is run
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# --- ENVIRONMENT LOADING ---
# Load from root, forcing overwrite of system variables to ensure local .env takes priority
dotenv_path = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

# --- CLIENT INITIALIZATION ---
# Validate key before initializing to prevent silent crashes
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logger.error("CRITICAL: GOOGLE_API_KEY not found in .env at %s", dotenv_path)
    # We exit here so the Inspector doesn't hang in an EOF loop
    sys.exit(1)

# Initialize MCP and GenAI Client
mcp = FastMCP("FloodPulse-Vision")
client = genai.Client(api_key=api_key)

@mcp.tool()
def analyze_mbagathi_risk(agent_name: str, lat: float, lon: float) -> str:
    """Fuses Terrain Map and Pulse Data to analyze flood risk."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(script_dir, "assets", "maps", f"{agent_name}_mission_map.png")

    if not os.path.exists(map_path):
        logger.error(f"Missing map file: {map_path}")
        return "Error: Mission map not found."

    try:
        # Import dynamically to avoid issues if module isn't in scope
        from levels.level_2.weather_service import get_nairobi_pulse
        pulse = get_nairobi_pulse(agent_name, lat, lon)
        
        img = Image.open(map_path)
        
        prompt_text = (
            f"Nairobi FloodPulse. Agent: {agent_name}. Conditions: {pulse['status']}. "
            "Analyze the terrain for potential flood sumps based on this map."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash", # Updated to stable flash model string
            contents=[prompt_text, img]
        )
        
        return f"🛰️ REPORT: {response.text}"

    except Exception as e:
        logger.exception("Fusion process failed")
        return f"Internal Fusion Error: {str(e)}"

if __name__ == "__main__":
    # Ensure no print statements exist in this file that are not sent to stderr
    mcp.run()