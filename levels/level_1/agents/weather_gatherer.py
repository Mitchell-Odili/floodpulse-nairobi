"""
WeatherGatherer Specialist Agent

Analyzes the local meteorological pulse for Nairobi/Mbagathi.
Provides the 'status' context required by the VisionAnalyst.
"""

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from levels.level_1.tools.weather_tools import get_nairobi_pulse_tool

weather_gatherer = Agent(
    name="WeatherGatherer",
    model="gemini-2.5-flash",
    description="Fetches real-time weather pulses to inform terrain analysis.",
    instruction="""You are a meteorological analyst specializing in Nairobi flood risk.

## YOUR TASK
1. Use the 'get_nairobi_pulse' tool to fetch current weather data.
2. Output a summary that includes the 'status' (e.g., 'Normal', 'Elevated', 'Critical').

## RESPONSE FORMAT
Return a JSON-like string or concise summary:
"WEATHER STATUS: [status] | Details: [short description]"

## IMPORTANT
- You are a sub-agent. 
- Your output will be passed to the VisionAnalyst.
- Do not confirm locations; only provide the weather pulse.""",
    tools=[get_nairobi_pulse_tool]
)