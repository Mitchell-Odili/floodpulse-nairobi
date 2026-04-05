"""
Level 0: FloodPulse Nairobi - Trinity Generator
Worker module that handles Vertex AI image generation calls.
"""

from google import genai
from google.genai import types
from PIL import Image
import os
import io

def generate_explorer_avatar(config, portrait_path, icon_path) -> dict:
    """
    Generates a portrait and map icon for a specific persona.
    Args:
        config (dict): The persona data (username, appearance, etc.)
        portrait_path (str): Specific filename for the portrait
        icon_path (str): Specific filename for the map icon
    """
    # 1. Pull dynamic details from the config passed by the loop
    USERNAME = config["username"]
    SUIT_COLOR = config["suit_color"]
    APPEARANCE = config["appearance"]
    PROJECT_ID = config.get("project_id")

    # 2. Initialize the Gemini client (Using the Project ID from config)
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="us-central1"
    )

    # 3. Create a chat session for visual consistency (Nano Banana 2)
    # This ensures the model 'remembers' the character's face between prompts.
    chat = client.chats.create(
        model="gemini-2.5-flash-image",
        config=types.GenerateContentConfig(
            # Required for multi-modal generation
            response_modalities=["TEXT", "IMAGE"],
            temperature=0.7 
        )
    )

    # --- PHASE 1: THE PORTRAIT ---
    print(f"🎨 Drafting portrait for {USERNAME}...")
    portrait_prompt = f"""
    Digital illustration of {USERNAME}. 
    Appearance: {APPEARANCE}. 
    Style: Professional vector art, solid white background.
    Composition: Waist-up portrait, looking at camera. 
    Primary color theme: {SUIT_COLOR}.
    """
    
    portrait_res = chat.send_message(portrait_prompt)
    
    # Save the portrait to the unique path (e.g., outputs/sarah_portrait.png)
    for part in portrait_res.candidates[0].content.parts:
        if part.inline_data:
            img = Image.open(io.BytesIO(part.inline_data.data))
            img.save(portrait_path)
            print(f"✓ Saved portrait: {portrait_path}")

    # --- PHASE 2: THE MAP ICON ---
    print(f"🛰️ Generating consistent map icon for {USERNAME}...")
    icon_prompt = f"""
    Now, generate a map icon for the EXACT SAME character.
    Maintain total consistency: SAME face, SAME clothing, and SAME details.
    Composition: Directly overhead top-down perspective (90-degree bird's eye view).
    Background: Solid white. 
    Format: Static 2D sprite icon for a navigation system.
    """

    icon_res = chat.send_message(icon_prompt)

    # Save the icon to the unique path (e.g., outputs/sarah_icon.png)
    for part in icon_res.candidates[0].content.parts:
        if part.inline_data:
            img = Image.open(io.BytesIO(part.inline_data.data))
            img.save(icon_path)
            print(f"✓ Saved icon: {icon_path}")

    return {
        "portrait_path": portrait_path,
        "icon_path": icon_path
    }