from config import MODELS
from typing import List
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from levels.level_1.tools.vision_tools import analyze_terrain_tool
from levels.level_1.tools.map_tools import generate_active_mission_map # Import the dynamic tool

class VisionTelemetry(BaseModel):
    terrain_hazard: str = Field(description="The assessed risk level (e.g., 'Low', 'Vulnerable', 'High-Risk')")
    slope_percentage: float = Field(description="Estimated slope percentage")
    obstacles: List[str] = Field(description="List of detected physical obstacles")
    evacuation_advice: str = Field(description="Clear, actionable safe routing guidance")
    telemetry_type: str = Field(default="terrain")

vision_analyst = Agent(
    name="VisionAnalyst",
    model=MODELS["sub_agent"],
    description="Analyzes terrain maps and imagery for flood risks.", 
    instruction="""You are a terrain analyst. 
    1. YOUR GOAL: Identify flood risks and evacuation paths.
    2. CAPABILITY: Use 'generate_active_mission_map' to obtain the map and 
       'analyze_terrain_tool' to parse it. 
    3. AUTONOMY: Always call the map tool first, then the analysis tool.
    4. OUTPUT: Populate the TerrainTelemetry schema.,
   """,
    tools=[analyze_terrain_tool, generate_active_mission_map],
    output_schema=VisionTelemetry,
    output_key="terrain_telemetry"
)