
"""
FloodPulse Nairobi - Persona Customization
Select your role (Commuter, Responder, Strategist) and define Sarah/Juma/Kamau.
"""

import json
import os
import random
import sys

# Configuration file is in project root
# CONFIG_FILE = "../../config.json"
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

# FloodPulse Role Mapping (Replaces Attire)
ROLES = {
    "1": ("Stranded Commuter (Sarah)", "professional attire, holding a glowing smartphone, blue distress aura"),
    "2": ("Boda First-Responder (Juma)", "high-visibility green reflective vest, motorcycle helmet, rugged street gear"),
    "3": ("Urban Strategist (Kamau)", "smart corporate attire, analytical expression, tech-blue silhouette"),
}

# Localized Nairobi traits to ensure cultural accuracy
RANDOM_TRAITS = [
    "wearing a Kenyan flag beaded bracelet",
    "braided hair style",
    "short cropped hair",
    "shaved head",
    "wearing a subtle Ankara-patterned accessory",
    "determined expression",
    "focused on a mobile device",
]

def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: config.json not found at {CONFIG_FILE}.")
        sys.exit(1)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config: dict) -> None:
    """Updates the config file safely."""
    # Ensure we don't accidentally lose system settings
    # In a production app, you might use a separate 'user_profile.json'
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print("✓ Configuration synced to project root.")

def get_role() -> tuple:
    """Prompt user to select a FloodPulse role."""
    print("\n🌊 Welcome to the FloodPulse Nairobi Simulation")
    print("Select your persona for the Mbagathi Basin mission:")

    for key, (name, _) in ROLES.items():
        print(f"  {key}. {name}")

    while True:
        choice = input("\nChoice [1-3, default=1]: ").strip() or "1"
        if choice in ROLES:
            name, description = ROLES[choice]
            # Assign suit_color based on role for visual grouping
            color_map = {"1": "Blue", "2": "Green", "3": "Gold"}
            print(f"✓ Role Selected: {name}")
            return name.split(" (")[0], description, color_map[choice]
        print("Please enter 1, 2, or 3.")

def get_appearance() -> str:
    """Add cultural markers automatically to save credits on retries."""
    print("\nDescribe your persona's specific look (or Enter for random):")
    user_input = input("> ").strip()

    # We append the Kenyan bracelet automatically to ensure it's in the prompt
    cultural_marker = "wearing a Kenyan flag beaded bracelet"
    
    if user_input == "":
        trait = random.choice(RANDOM_TRAITS)
        appearance = f"{trait}, {cultural_marker}"
    else:
        appearance = f"{user_input}, {cultural_marker}"
    
    print(f"✓ Appearance set: {appearance}")
    return appearance

def get_location(default_coords: dict) -> dict:
    """Allow user to override default coordinates."""
    print(f"\n🌍 Current mission focus: {default_coords}")
    choice = input("Use default coordinates? [Y/n]: ").strip().lower()
    
    if choice == 'n':
        lat = input("Enter Latitude: ").strip()
        lng = input("Enter Longitude: ").strip()
        return {"lat": float(lat), "lng": float(lng)}
    
    return default_coords

def main():
    config = load_config()

    print("\n🌍 Preparing FloodPulse Nairobi Mission...")
    
    # Check if we are doing a single selection or initializing the full team
    mode = input("Generate (1) Single Persona or (2) Initialize Trinity? [default=1]: ").strip() or "1"

    if mode == "2":
        # This prepares the config with the metadata needed for batching
        config["mission_mode"] = "trinity"
        save_config(config)
        print("\n✅ Mission set to Trinity Mode. create_identity.py will now generate all 3 personas.")
    else:
        # Standard single persona selection
        username, role_desc, theme_color = get_role()
        config["username"] = username
        config["suit_color"] = theme_color
        config["appearance"] = f"{role_desc}, {get_appearance()}"
        config["mission_mode"] = "single"

        # Only prompt for custom location if in single mode
        config["coords"] = get_location(config.get("default_coords"))
        print(f"\n✅ Configuration Locked for {username}!")

    save_config(config)
    print("Next: Run 'python create_identity.py' to generate assets.")

if __name__ == "__main__":
    main()
    