"""
Level 0: Avatar Generator

This module generates your unique persona avatars using
multi-turn image generation with Gemini for
character consistency across portrait and icon.

=== CODELAB INSTRUCTIONS ===

You will implement three steps in the generate_explorer_avatar() function:

1. STEP_1_CREATE_CHAT_SESSION
   Create a chat session to maintain character consistency

2. STEP_2_GENERATE_PORTRAIT
   Generate the explorer portrait with your customizations

3. STEP_3_GENERATE_ICON
   Generate consistent map icons using the same chat session

Follow the instructions in the codelab to complete each step.
"""

from google import genai
from google.genai import types
from PIL import Image
import json
import os
import io


def generate_explorer_avatar(config: dict, portrait_path: str, icon_path: str) -> dict:
    """
    Generate portrait and icon using multi-turn chat for consistency.

    The key technique here is using a CHAT SESSION rather than independent
    API calls. This allows Gemini to "remember" the character it created
    in the first turn, ensuring the icon matches the portrait. 

    Generates a consistent portrait and icon using Gemini 3.5 Flash.
    Accepts config and paths as arguments for maximum flexibility.

    Returns:
        dict with portrait_path and icon_path
    """

    # =========================================================================
    # STEP_1_CREATE_CHAT_SESSION
    # =========================================================================    #
    # Create a chat session using client.chats.create() with:
    # - model: "gemini-3.1-flash-image" (Nano Banana 2)
    # - config: GenerateContentConfig with response_modalities=["TEXT", "IMAGE"]
    #
    # Hint: You need to use types.GenerateContentConfig
    # =========================================================================
    # STEP_1_CREATE_CHAT_SESSION
    # Create a chat session to maintain character consistency across generations.
    # The chat session preserves context between turns, so Gemini "remembers"
    # what it generated and can create consistent variations.
    
    # Initialize Gemini 3.1 Flash Client
    client = genai.Client(
        vertexai=True,
        project=config.get("project_id"),
        location="us-central1"
    )

    # 1. CREATE CHAT SESSION
    # Using Gemini 3.1 Flash for improved reasoning and image fidelity
    chat = client.chats.create(
        model="gemini-3.1-flash-image",
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        )
    )

    # =========================================================================
    # STEP_2_GENERATE_PORTRAIT
    # =========================================================================
    # 1. Create a portrait_prompt string that includes:
    #    - APPEARANCE, USERNAME, and SUIT_COLOR variables
    #    - Style requirements (digital illustration, white background, etc.)
    #
    # 2. Send the prompt using chat.send_message(portrait_prompt)
    #
    # 3. Extract the image from the response:
    #    - Loop through portrait_response.candidates[0].content.parts
    #    - Find the part where part.inline_data is not None
    #    - Convert to PIL Image: Image.open(io.BytesIO(part.inline_data.data))
    #    - Save to "outputs/portrait.png"
    #
    # 4. Print progress messages for user feedback
    # =========================================================================
    # STEP_2_GENERATE_PORTRAIT
    # First turn: Generate the explorer portrait.
    # This establishes the character that will be referenced in subsequent turns.

    # 2. GENERATE PORTRAIT
    portrait_prompt = f"""Create a stylized persona portrait.
    
    Character: {config['username']}
    Appearance: {config['appearance']}
    Suit color: {config['suit_color']}
    
    STYLE REQUIREMENTS:
    - Digital illustration, clean lines, vibrant colors.
    - Solid white background (#FFFFFF) - NO gradients.
    - Head and shoulders, 3/4 view.
    """

    print(f"🎨 Generating portrait for {config['username']}...")
    portrait_response = chat.send_message(portrait_prompt)
    
    # Extract image
    portrait_image = None
    for part in portrait_response.candidates[0].content.parts:
        if part.inline_data:
            portrait_image = Image.open(io.BytesIO(part.inline_data.data))
            portrait_image.save(portrait_path)
            break
            
    if not portrait_image:
        raise Exception("Failed to generate portrait.")

    # =========================================================================
    # MODULE_5_STEP_3_GENERATE_ICON
    # =========================================================================
    #
    # 1. Create an icon_prompt that asks for the SAME character
    #    - Emphasize consistency: "SAME person, SAME face, SAME suit"
    #    - Request tighter crop (head and shoulders only)
    #    - Request white background and square aspect ratio
    #
    # 2. Send the prompt using chat.send_message(icon_prompt)
    #    - The chat session remembers the character from step 2!
    #
    # 3. Extract and save the icon image to "outputs/icon.png"
    #
    # 4. Print progress messages for user feedback
    # =========================================================================
    # STEP_3_GENERATE_ICON
    # Second turn: Generate a consistent icon for the map.
    # Because we're in the same chat session, Gemini remembers the character
    # from the portrait and will maintain visual consistency.

    # 3. GENERATE CONSISTENT ICON
    icon_prompt = """Generate a circular map marker icon of this SAME character.
    
    STRICT CONSTRAINTS:
    - PERSISTENCE: Maintain identical facial features and suit details.
    - COMPOSITION: Head-and-shoulders, perfectly centered.
    - FORMAT: Solid #FFFFFF white background.
    - SCALE: Optimized for 64x64px map display.
    """

    print(f"🖼️ Generating map icon for {config['username']}...")
    icon_response = chat.send_message(icon_prompt)
    
    # Extract image
    icon_image = None
    for part in icon_response.candidates[0].content.parts:
        if part.inline_data:
            icon_image = Image.open(io.BytesIO(part.inline_data.data))
            icon_image.save(icon_path)
            break
            
    if not icon_image:
        raise Exception("Failed to generate icon.")

    return {
        "portrait_path": portrait_path,
        "icon_path": icon_path
    }

if __name__ == "__main__":
    # This block allows you to run `python generator.py` for a quick test
    if os.path.exists("config.json"):
        with open("config.json") as f:
            test_config = json.load(f)
            # Inject a test persona for the standalone test
            test_config.update({"username": "Sarah", "appearance": "Professional", "suit_color": "Blue"})
            
            os.makedirs("outputs", exist_ok=True)
            generate_explorer_avatar(test_config, "outputs/test_p.png", "outputs/test_i.png")
            print("✅ Standalone test complete.")
    else:
        print("⚠️ No config.json found for standalone test.")