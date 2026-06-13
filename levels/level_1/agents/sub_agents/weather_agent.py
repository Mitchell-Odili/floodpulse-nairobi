from config import MODELS
from typing import Optional
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from levels.level_1.tools.weather_tools import get_active_weather_pulse, get_nairobi_pulse_tool

class WeatherTelemetry(BaseModel):
    rain_mm_h: Optional[float] = Field(description="Rainfall intensity in mm/h", default=None)
    flash_index: Optional[float] = Field(description="Normalized risk index from 0 to 1", default=None)
    status: str = Field(description="The pulse status: 'Low Pulse', 'Moderate Pulse', or 'Critical Pulse'", default="Data Unavailable")
    telemetry_type: str = Field(default="weather")


weather_gatherer = Agent(
    name="WeatherGatherer",
    model=MODELS["sub_agent"],
    instruction="""
    You are a meteorological data specialist.
    1. TOOL USAGE: Call 'get_active_weather_pulse'.
    2. OUTPUT: Return the weather data exactly as provided by the tool.
    """,
    tools=[get_active_weather_pulse],
    output_schema=WeatherTelemetry,
    output_key="weather_telemetry"
)