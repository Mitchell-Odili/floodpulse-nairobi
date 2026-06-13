from config import MODELS
from pydantic import BaseModel, Field
from google.adk.agents import SequentialAgent, Agent
from levels.level_1.agents.sub_agents.weather_agent import weather_gatherer
from levels.level_1.agents.sub_agents.vision_agent import vision_analyst
from levels.level_1.agents.sub_agents.responder_agent import responder_agent
from levels.level_1.tools.context_tools import update_mission_context


# 2. Define the Pipeline of workers
pipeline = SequentialAgent(
    name="FloodPulse_Workflow",
    sub_agents=[weather_gatherer, vision_analyst, responder_agent],
    description="Gathering, Analyzing, and Responding to flood risks."
)

# 2. Define your Director
# The Director orchestrates the user interaction and triggers the pipeline
floodpulse_director = Agent(
    name="FloodPulse_Director",
    model=MODELS["director"],
    instruction="""
    You are the FloodPulse Director. 
    1. GREETING: Start every new mission by greeting the user professionally.
    2. PURPOSE: Lead flood risk assessments for the Mbagathi Basin.
    3. DATA COLLECTION: Request Name, Latitude, and Longitude if missing.Do not trigger the pipeline until you have all three pieces of data.
    4. CONTEXT PERSISTENCE: As soon as you receive the responder name, latitude, and longitude from the user, 
        you MUST call the 'update_mission_context' tool to save this data. 
        Do not proceed with analysis until this tool has been successfully executed.
    5. ANALYSIS: Once the context is set, initiate the 'FloodPulse_Workflow'.
    6. REPORTING: Present the final verdict from 'final_verdict' key to the user.
    
    TONE: Professional, authoritative, and direct.
    """,
    tools=[update_mission_context],
    sub_agents=[pipeline], # The pipeline is now a specialized sub-agent
    output_key="mission_data"    
)