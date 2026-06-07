from config import MODELS
from google.adk.agents import Agent
from levels.level_1.tools.weather_tools import get_nairobi_pulse_tool

weather_gatherer = Agent(
    name="WeatherGatherer",
    model=MODELS["sub_agent"],
    instruction="""
    You are a meteorological data specialist.
    1. Receive a lat/lon request.
    2. Call 'get_nairobi_pulse_tool' with these coordinates.
    3. Output the result clearly: "WEATHER STATUS: [status] | Rainfall: [rain_mm_h]mm/h".
    4. Do not offer advice; report the telemetry only.
    """,
    tools=[get_nairobi_pulse_tool]
)