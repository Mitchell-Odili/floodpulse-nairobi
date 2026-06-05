
"""
FloodPulse Nairobi - Create Identity Script
Orchestrates the avatar generation for the Mbagathi Basin Simulation.
"""

import json
import os
import sys
import requests
from generator import generate_explorer_avatar

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

    return config

def main():
    config = load_config()
    os.makedirs("outputs", exist_ok=True)

    # 1. Define the pool of candidates
    trinity = [
        {"id": "sarah", "role": "Stranded Commuter", "color": "Blue", "appearance": "Professional attire, blue distress aura"},
        {"id": "juma", "role": "Boda First-Responder", "color": "Green", "appearance": "High-vis reflective vest, motorcycle helmet"},
        {"id": "kamau", "role": "Urban Strategist", "color": "Gold", "appearance": "Smart corporate attire, tech-blue silhouette"}
    ]

    # 2. Determine Scope (Trinity or Single)
    mode = config.get("mission_mode", "trinity")
    targets = trinity if mode == "trinity" else [next(p for p in trinity if p['id'] == config.get("id", "sarah"))]

    print(f"\n🚀 Launching Identity Phase in {mode.upper()} mode...")

    for persona in targets:
        portrait_path = f"outputs/{persona['id']}_portrait.png"
        icon_path = f"outputs/{persona['id']}_icon.png"

        if os.path.exists(portrait_path) and os.path.exists(icon_path):
            print(f"✅ {persona['id']} assets exist. Skipping.")
            continue

        # 3. Inject Persona Context into the global config
        # We merge system defaults (coords, api_base) with persona specifics
        persona_config = config.copy()
        persona_config.update({
            "username": f"{persona['role']} ({persona['id'].capitalize()})",
            "suit_color": persona["color"],
            "appearance": f"{persona['appearance']}, wearing a Kenyan flag beaded bracelet"
        })

        print(f"🎨 Generating {persona['id']}...")
        generate_explorer_avatar(persona_config, portrait_path, icon_path)

    print("\n🌍 Level 0 Complete: Identity confirmed.")

if __name__ == "__main__":
    main()
