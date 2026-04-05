
"""
FloodPulse Nairobi - Create Identity Script
Orchestrates the avatar generation for the Mbagathi Basin Simulation.
"""

import json
import os
import sys
import requests

# Configuration
# CONFIG_FILE = "../config.json" # Adjusted path for levels/level_0/ structure
# 1. Get the directory where THIS script/notebook is located
current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

# 2. Find the 'floodpulse-nairobi' root specifically
# This splits the path and finds the project folder, then joins it back together
path_parts = current_dir.split(os.sep)
if 'floodpulse-nairobi' in path_parts:
    root_idx = path_parts.index('floodpulse-nairobi')
    PROJECT_ROOT = os.sep.join(path_parts[:root_idx + 1])
else:
    # Fallback: Go up two levels if the folder name isn't found
    PROJECT_ROOT = os.path.abspath(os.path.join(current_dir, "..", ".."))

# 3. Define the final path
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config.json")
print(f" Routing to config at: {CONFIG_FILE}")

def load_config() -> dict:
    """Load configuration from the project root."""
    if not os.path.exists(CONFIG_FILE):
        print(f" Error: config.json not found at {CONFIG_FILE}.")
        print("Please ensure your config.json is in the project root.")
        sys.exit(1)

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    # Validate required fields for FloodPulse
    required_fields = ["event_code", "api_base", "project_id"]
    missing = [f for f in required_fields if f not in config]
    if missing:
        print(f" Error: Missing config fields: {', '.join(missing)}")
        sys.exit(1)

    # Check for persona customization
    if "appearance" not in config:
        print(" Error: Avatar preferences (appearance) not set in config.json.")
        sys.exit(1)

    return config


def generate_avatar(config, portrait_path, icon_path) -> dict:
    """Calls the user's generator code to create Sarah/Juma/Kamau sprites."""
    try:
        from generator import generate_explorer_avatar
    except ImportError as e:
        print(f" Error importing generator: {e}")
        sys.exit(1)

    os.makedirs("outputs", exist_ok=True)

    try:
        result = generate_explorer_avatar(config, portrait_path, icon_path)
    except Exception as e:
        print(f" Error during generation: {e}")
        sys.exit(1)

    if not result or "portrait_path" not in result or "icon_path" not in result:
        print(" Error: generator.py must return portrait_path and icon_path")
        sys.exit(1)

    return result


def upload_avatar(config: dict, portrait_path: str, icon_path: str) -> dict:
    """
    Upload avatar images to the FloodPulse API.
    Note: If you haven't built the Level 2 backend yet, this will fail.
    For now, we'll wrap it in a try/except to allow local-only testing.
    """
    api_base = config["api_base"]
    participant_id = config["participant_id"]
    url = f"{api_base}/participants/{participant_id}/avatar"

    print(f"📡 Attempting upload to {api_base}...")
    
    try:
        with open(portrait_path, "rb") as p_file, open(icon_path, "rb") as i_file:
            files = {
                "portrait": ("portrait.png", p_file, "image/png"),
                "icon": ("icon.png", i_file, "image/png")
            }
            # Timeout set to 5s for local testing; increase if using remote GCP
            response = requests.post(url, files=files, timeout=5)
            return response.json()
    except Exception:
        print("⚠️  Backend not reachable. Skipping upload (Level 2 dependency).")
        return {"status": "local_success"}


def print_success(config: dict):
    """Print the FloodPulse confirmation box."""
    username = config["username"]
    event = config["event_code"]
    # Default to Mbagathi Basin coordinates if not set
    lat = config.get("coords", {}).get("lat", "-1.3211")
    lng = config.get("coords", {}).get("lng", "36.8041")

    print()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                ✅ NAIROBI IDENTITY CONFIRMED!                 ║")
    print("╠═══════════════════════════════════════════════════════════════╣")
    print("║                                                               ║")
    print(f"║  Persona: {username:<51} ║")
    print(f"║  Deployment: {event:<48} ║")
    print(f"║  Coordinates: {lat}, {lng:<36} ║")
    print("║                                                               ║")
    print("║  🗺️  Explorer registered in Mbagathi Basin Graph.             ║")
    print("║                                                               ║")
    print("║  ✅ Level 0 complete! Ready for Level 1: Terrain Discovery.   ║")
    print("║                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════╝")




def main():
    # 1. First, find your config (The "Nairobi Handshake")
    config = load_config()
    
    # 2. Site Prep: Ensure the directory exists locally
    os.makedirs("outputs", exist_ok=True)
    
    # 3. Define the Trinity (Sarah is the priority)
    trinity = [
        {"id": "sarah", "role": "Stranded Commuter", "color": "Blue", "appearance": "Professional attire, blue distress aura"},
        {"id": "juma", "role": "Boda First-Responder", "color": "Green", "appearance": "High-vis reflective vest, motorcycle helmet"},
        {"id": "kamau", "role": "Urban Strategist", "color": "Gold", "appearance": "Smart corporate attire, tech-blue silhouette"}
    ]

    for persona in trinity:
        portrait_path = f"outputs/{persona['id']}_portrait.png"
        icon_path = f"outputs/{persona['id']}_icon.png"

        # CREDIT SAVER: Check if this specific persona already exists
        if os.path.exists(portrait_path) and os.path.exists(icon_path):
            print(f"✅ {persona['role']} ({persona['id']}) assets found. Skipping...")
            continue

        print(f"🚀 Initializing Vertex AI for {persona['role']} ({persona['id']})...")
        
        # Inject persona details into config for the generator
        config["username"] = f"{persona['role']} ({persona['id'].capitalize()})"
        config["suit_color"] = persona["color"]
        config["appearance"] = f"{persona['appearance']}, wearing a Kenyan flag beaded bracelet"

        # Step 1: Generate AI Assets (Pass the specific paths to the generator)
        # Ensure your generate_avatar() function accepts these paths!
        result = generate_avatar(config, portrait_path, icon_path)
        
        if result:
            print(f"✓ {persona['id'].capitalize()} Assets Generated.")
            # Step 2: Network Sync (Optional)
            # upload_avatar(config, portrait_path, icon_path)

    # Step 3: Final Confirmation
    print("\n🌍 FloodPulse Identity Phase Complete.")
    print("Check 'levels/level_0/outputs/' for Sarah, Juma, and Kamau.")


if __name__ == "__main__":
    main()