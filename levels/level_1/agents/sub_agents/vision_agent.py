from google.adk.agents import Agent
from levels.level_1.tools.vision_tools import analyze_terrain_tool
from levels.level_1.tools.map_tools import generate_mission_map # Import the dynamic tool

vision_analyst = Agent(
    name="VisionAnalyst",
    model="gemini-2.5-flash",
    description="Analyzes terrain maps and imagery for flood risks.", 
    instruction="""You are a terrain analyst. 
    1. YOUR GOAL: Identify flood risks and evacuation paths.
    2. CAPABILITY: You can generate maps using 'generate_mission_map' and analyze 
       them with 'analyze_terrain_tool'.
    3. AUTONOMY: If you don't have a map for the requested location, call 
       'generate_mission_map' first to get visual data, then analyze it.
    4. OUTPUT: Provide a clear flood risk report and safe routing advice.""",
    tools=[analyze_terrain_tool, generate_mission_map],
)