import os
import sys
from mcp.server.fastmcp import FastMCP
from google import genai
from PIL import Image
from dotenv import load_dotenv

# --- PATH SHIELD ---
# Ensures the 'levels' folder is always findable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

try:
    from levels.level_2.weather_service import get_nairobi_pulse
except ImportError:
    # Fallback if the path logic above fails in specific environments
    def get_nairobi_pulse(name, lat, lon):
        return {"status": "Weather Service Offline", "rain_mm_h": 0, "flash_index": 0}

load_dotenv()

# Initialize Server
mcp = FastMCP("FloodPulse-Vision")

# Initialize Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@mcp.tool()
def analyze_mbagathi_risk(agent_name: str, lat: float, lon: float):
    """
    Fuses Terrain and Pulse into a single risk report.
    """
    # 1. Path Resolution
    script_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(script_dir, f"{agent_name}_on_mission.png")

    if not os.path.exists(map_path):
        return f"Error: Map not found for {agent_name}."

    try:
        # 2. Data Gathering
        pulse = get_nairobi_pulse(agent_name, lat, lon)
        img = Image.open(map_path)
        
        # 3. The New SDK Content Format
        # We explicitly pass the prompt and the PIL image object
        prompt_text = f"Nairobi FloodPulse. Agent: {agent_name}. Pulse: {pulse['status']}. Analyze map for sumps."

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt_text, img]
        )
        
        # 4. Clean Output
        # Ensure we return a clean string to the MCP pipe
        return f"🛰️ REPORT: {response.text}"

    except Exception as e:
        # Crucial: Return the error as a string, don't let the script crash
        return f"Internal Fusion Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()