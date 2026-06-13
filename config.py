import os
from dotenv import load_dotenv

# Load .env 
load_dotenv()

MODELS = {
    "director": "gemini-2.5-flash",
    "sub_agent": "gemini-2.5-flash",
    "vision_model": "gemini-2.5-flash"
}

