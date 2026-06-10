from config import MODELS
from google.adk.agents import SequentialAgent, Agent
from levels.level_1.agents.sub_agents.weather_agent import weather_gatherer
from levels.level_1.agents.sub_agents.vision_agent import vision_analyst
from levels.level_1.agents.sub_agents.responder_agent import responder_agent

# 1. Define the Pipeline of workers
pipeline = SequentialAgent(
    name="FloodPulse_Workflow",
    sub_agents=[weather_gatherer, vision_analyst, responder_agent],
    description="Gathering, Analyzing, and Responding to flood risks."
)

# 2. Define your Director with the personality and instructions
# The Director acts as the "Face" and "Brain" that uses the workflow
floodpulse_director = Agent(
    name="FloodPulse_Director",
    model=MODELS["director"],
    sub_agents=[pipeline], # The pipeline is now a specialized sub-agent
    instruction="""
    You are the FloodPulse Director. 
    1. GREETING: Start every new mission by greeting the user professionally.
    2. PURPOSE: Lead flood risk assessments for the Mbagathi Basin.
    3. DATA COLLECTION: Request Name, Latitude, and Longitude if missing.
    4. EXECUTION: Use your sub-agent pipeline to synthesize data into a high-fidelity risk report.
    5. ROUTING: If asked for an evacuation route, provide step-by-step guidance based on terrain safety.
    
    TONE: Professional, authoritative, and direct.
    """
)