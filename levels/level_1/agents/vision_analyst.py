from google.adk.agents import Agent
from levels.level_1.tools.vision_tools import analyze_terrain_tool

vision_analyst = Agent(
    name="VisionAnalyst",
    model="gemini-2.5-flash",
    description="Analyzes terrain maps for flood risks.",
    instruction="""You are a terrain analyst. 
    1. Access the 'pulse_status' from the context provided by the WeatherGatherer.
    2. Call 'analyze_terrain_tool' with the current agent name and pulse status.
    3. Output the final flood risk report.""",
    tools=[analyze_terrain_tool]
)