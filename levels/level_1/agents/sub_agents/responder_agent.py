from config import MODELS
from pydantic import BaseModel, Field
from google.adk.agents import Agent

class FinalVerdict(BaseModel):
    status: str = Field(description="Final safety status: SAFE, WARNING, or CRITICAL")
    reason: str = Field(description="Concise justification for the status")
    route_advice: str = Field(description="Actionable evacuation guidance")

# The Commander expects these keys in its input dictionary
class MissionInputs(BaseModel):
    weather_telemetry: dict # In a production system, you'd import the actual WeatherTelemetry class
    terrain_telemetry: dict # Import TerrainTelemetry


responder_agent = Agent(
    name="Responder_Unit",
    model=MODELS["sub_agent"],
    instruction="""
    You are the Mission Commander for the Mbagathi Basin.
    
    ## TASK
    Synthesize the provided 'weather_telemetry' and 'terrain_telemetry' to produce a final safety verdict.
    
    ## LOGIC RULES
    1. CRITICAL: If weather_telemetry['status'] is 'Critical Pulse' OR terrain_telemetry['terrain_hazard'] is 'High-Risk'.
    2. WARNING: If weather_telemetry['status'] is 'Moderate Pulse' AND terrain_telemetry['terrain_hazard'] is 'Vulnerable'.
    3. SAFE: Otherwise.
    
    ## DATA INTEGRATION
    - Incorporate 'evacuation_advice' from terrain_telemetry into your output.
    - If telemetry data is 'Data Unavailable', treat it as a neutral factor.
    """,
    input_schema=MissionInputs,
    output_schema=FinalVerdict,
    output_key="final_verdict"
)