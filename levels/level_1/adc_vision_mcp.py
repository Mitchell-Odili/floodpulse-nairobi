import json
import sys
import logging
from pathlib import Path
from google import genai
from google.genai import types
from mcp.server.fastmcp import FastMCP
from PIL import Image

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("FloodPulse-Vision")

# --- PATH & CONFIG RESOLUTION ---
def find_project_root(start_path: Path, target_file="config.json"):
    for parent in [start_path] + list(start_path.parents):
        if (parent / target_file).exists():
            return parent
    return start_path.parent

PROJECT_ROOT = find_project_root(Path(__file__).resolve())
CONFIG_FILE = PROJECT_ROOT / "config.json"

# Add project root to sys.path to enable imports from the project structure
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Load Config
try:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
except Exception as e:
    logger.error(f"CRITICAL: Could not load config at {CONFIG_FILE}: {e}")
    sys.exit(1)

project_id = config.get("project_id")
if not project_id:
    logger.error("CRITICAL: 'project_id' not found in config.json")
    sys.exit(1)

# --- CLIENT INITIALIZATION ---
# Using Vertex AI via Application Default Credentials (ADC)
client = genai.Client(
    vertexai=True,
    project=project_id,
    location="us-central1"
)

# Initialize MCP
mcp = FastMCP("FloodPulse-Vision")

@mcp.tool()
def analyze_mbagathi_risk(agent_name: str, lat: float, lon: float) -> str:
    """Fuses Terrain Map and Pulse Data to analyze flood risk."""
    
    # 1. Clean the agent_name to remove whitespace/newlines
    clean_name = agent_name.strip()
    
    # 2. Resolve map path dynamically
    map_path = PROJECT_ROOT / "levels" / "level_1" / "assets" / "maps" / f"{clean_name.lower()}_mission_map.png"
    
    logger.info(f"Looking for map at: {map_path}")

    if not map_path.exists():
        return f"Error: Mission map not found at {map_path}"

    try:
        # Import dynamically from the project root
        from levels.level_2.weather_service import get_nairobi_pulse
        pulse = get_nairobi_pulse(clean_name, lat, lon)
        
        # Load image
        img = Image.open(map_path)
        
        prompt_text = (
            f"Nairobi FloodPulse. Agent: {clean_name}. Conditions: {pulse['status']}. "
            "Analyze the terrain for potential flood sumps based on this map."
        )

        # Call the model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt_text),
                        types.Part.from_bytes(data=img.tobytes() if hasattr(img, 'tobytes') else b'', mime_type="image/png")
                    ]
                )
            ]
        )
        return f"🛰️ REPORT: {response.text}"

    except Exception as e:
        logger.exception("Fusion process failed")
        return f"Internal Fusion Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()