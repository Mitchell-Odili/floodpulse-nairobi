
"""
FloodPulse Nairobi - Persona Customization
Select your role (Commuter, Responder, Strategist) and define Sarah/Juma/Kamau.
"""

import json
import os
import random
import sys

# Configuration file is in project root
CONFIG_FILE = "../../config.json"

# FloodPulse Role Mapping (Replaces Space Suits)
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
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

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

def main():
    config = load_config()

    # 1. Set Role and Theme Color
    username, role_desc, theme_color = get_role()
    config["username"] = username
    config["suit_color"] = theme_color # Keeping key name for generator.py compatibility

    # 2. Set Appearance with Local Markers
    config["appearance"] = f"{role_desc}, {get_appearance()}"

    save_config(config)
    print(f"\n✅ Configuration Locked for {username}!")
    print("Next: Run 'python create_identity.py' to generate assets on Vertex AI.")

if __name__ == "__main__":
    main()