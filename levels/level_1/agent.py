"""
Level 1: FloodPulse Orchestrator - Root Agent

This is the main entry point for the FloodPulse mission. 
It coordinates weather gathering and terrain vision analysis.

Architecture:
- Root Agent (FloodPulseOrchestrator): Coordinates the pipeline.
  - WeatherGatherer: Fetches current pulse status.
  - VisionAnalyst: Analyzes terrain maps based on the gathered pulse.

Key ADK Pattern: Sequential Pipeline
- The output of the WeatherGatherer is automatically passed 
  into the VisionAnalyst via the orchestration flow.
"""

import sys
from pathlib import Path

# Add the project root (the folder containing 'levels/') to the path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

# Now you can use clean imports from the root


import os
from dotenv import load_dotenv
from google.adk.agents import SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from levels.level_1.agents.weather_gatherer import weather_gatherer
from levels.level_1.agents.vision_analyst import vision_analyst

# Load environment variables once at startup
load_dotenv()

print(f"DEBUG: Current Python Executable: {sys.executable}")
print(f"DEBUG: Python Path: {sys.path}")

# =============================================================================
# BEFORE AGENT CALLBACK
# =============================================================================

async def setup_mission_context(callback_context: CallbackContext) -> None:
    """
    Reads dynamic coordinates from environment variables or a default source,
    making them available to the entire agent hierarchy.
    """
    # This replaces your old 'customize.py' logic
    callback_context.state["nairobi_lat"] = os.getenv("MISSION_LAT", "-1.3148")
    callback_context.state["nairobi_lon"] = os.getenv("MISSION_LON", "36.8115")
    callback_context.state["mission_name"] = "FloodPulse"

# =============================================================================
# ROOT ORCHESTRATOR
# =============================================================================

# The root_agent is what the ADK CLI ('adk web') looks for.
# It acts as the pipeline controller.

root_agent = SequentialAgent(
    name="FloodPulseOrchestrator",
    description="Coordinates weather pulse gathering and terrain vision analysis.",
    sub_agents=[weather_gatherer, vision_analyst],
    before_agent_callback=setup_mission_context # <--- THIS IS THE MISSING LINK
)

# Explicitly expose root_agent for the ADK entry point
__all__ = ["root_agent"]