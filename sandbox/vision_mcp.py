import os
import sys
import logging
from mcp.server.fastmcp import FastMCP
from google import genai
from PIL import Image
from dotenv import load_dotenv

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("FloodPulse-Vision")

## --- PATH SHIELD ---
# Get the directory of this file (sandbox/)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Move up ONE level to get to the project root
PROJECT_ROOT = os.path.dirname(script_dir)
sys.path.append(PROJECT_ROOT)

# --- ENVIRONMENT LOADING ---
dotenv_path = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

# --- CLIENT INITIALIZATION ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logger.error("CRITICAL: GOOGLE_API_KEY not found in .env at %s", dotenv_path)
    sys.exit(1)

mcp = FastMCP("FloodPulse-Vision")
client = genai.Client(api_key=api_key)

@mcp.tool()
def analyze_mbagathi_risk(agent_name: str, lat: float, lon: float) -> str:
    """Fuses Terrain Map and Pulse Data to analyze flood risk."""
    
    # Adjusted to look in the correct levels folder structure
    map_path = os.path.join(PROJECT_ROOT, "levels", "level_1", "assets", "maps", f"{agent_name}_mission_map.png")

    if not os.path.exists(map_path):
        logger.error(f"Missing map file: {map_path}")
        return "Error: Mission map not found."

    try:
        # UPDATED: Import from tools.weather_tools
        from tools.weather_tools import get_nairobi_pulse
        pulse = get_nairobi_pulse(agent_name, lat, lon)
        
        img = Image.open(map_path)
        
        prompt_text = (
            f"Nairobi FloodPulse. Agent: {agent_name}. Conditions: {pulse['status']}. "
            "Analyze the terrain for potential flood sumps based on this map."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt_text, img]
        )
        
        return f"🛰️ REPORT: {response.text}"

    except Exception as e:
        logger.exception("Fusion process failed")
        return f"Internal Fusion Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()