import os
import sys
import logging
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from google import genai
from PIL import Image
from dotenv import load_dotenv

# --- PATH SHIELD & SYSTEM PATH SETUP ---
# Identify the project root based on this file's location (sandbox/vision_mcp.py)
# Moving up one level from sandbox/ to the project root
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Ensure project root is at the very beginning of sys.path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import MODELS

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("FloodPulse-Vision")

# --- ENVIRONMENT LOADING ---
dotenv_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# --- CLIENT INITIALIZATION ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logger.error("CRITICAL: GOOGLE_API_KEY not found in .env at %s", dotenv_path)
    sys.exit(1)

mcp = FastMCP("FloodPulse-Vision")
client = genai.Client(api_key=api_key)

# --- TOOLS ---
@mcp.tool()
def analyze_mbagathi_risk(agent_name: str, lat: float, lon: float) -> str:
    """Fuses Terrain Map and Pulse Data to analyze flood risk."""
    
    # Path to the asset - now resolved via PROJECT_ROOT
    map_path = PROJECT_ROOT / "levels" / "level_1" / "assets" / "maps" / f"{agent_name}_mission_map.png"

    if not map_path.exists():
        logger.error(f"Missing map file: {map_path}")
        return "Error: Mission map not found."

    try:
        # Absolute import now works because PROJECT_ROOT is in sys.path
        from levels.level_1.tools.weather_tools import get_nairobi_pulse_tool
        
        pulse = get_nairobi_pulse_tool(agent_name, lat, lon)
        
        # Check if the tool returned an error first
        if "error" in pulse:
            return f"Telemetry Unavailable: {pulse['error']}"
                
        img = Image.open(map_path)
        
        # Constructing the high-fidelity risk assessment prompt
        prompt_text = (
            f"--- NAIROBI FLOODPULSE RISK ASSESSMENT ---\n"
            f"Target Agent: {agent_name}\n"
            f"Environmental Status: {pulse['status']} ({pulse['flash_index']} Flash Index)\n"
            f"Rainfall Intensity: {pulse['rain_mm_h']} mm/h\n"
            f"Task: Analyze the visual terrain features of this map to identify "
            f"vulnerable sumps and high-risk bottlenecks. Given the current "
            f"{pulse['status']}, evaluate the likelihood of immediate arterial "
            f"flooding at these coordinates. Provide a 'Safety Rating' (0-100) and "
            f"a list of recommended high-ground evacuation routes visible in the map."
        )

        response = client.models.generate_content(
            model=MODELS["vision_model"],
            contents=[prompt_text, img]
        )
        
        return f"🛰️ REPORT: {response.text}"

    except ImportError as ie:
        logger.exception("Failed to import tool modules")
        return f"Import Error: {str(ie)}"
    except Exception as e:
        logger.exception("Fusion process failed")
        return f"Internal Fusion Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()