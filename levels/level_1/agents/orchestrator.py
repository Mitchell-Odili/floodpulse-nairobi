import concurrent.futures
from config import MODELS
from google.adk.agents import Agent
from .sub_agents.weather_agent import weather_gatherer
from .sub_agents.vision_agent import vision_analyst
from .sub_agents.responder_agent import responder_agent
from utils.state_manager import update_registry, load_registry

# 1. Define the Orchestrator Agent (The Director)
floodpulse_director = Agent(
    name="FloodPulse_Director",
    model=MODELS["director"],
    sub_agents=[weather_gatherer, vision_analyst, responder_agent],
    instruction="""
    You are the FloodPulse Director. 
    
    1. GREETING: Start every new mission by greeting the user professionally.
    2. PURPOSE: Lead flood risk assessments for the Mbagathi Basin.
    3. DATA COLLECTION: Request Name, Latitude, and Longitude if missing.
    4. EXECUTION: Synthesize data gathered from sub-agents into a high-fidelity risk report.
    5. ROUTING: If asked for an evacuation route, provide step-by-step guidance based on terrain safety.
    
    TONE: Professional, authoritative, and direct.
    """
)

# 2. Studio Architecture Class
class FloodPulseStudio:
    def __init__(self, director):
        self.director = director

    def execute_parallel_gathering(self, context: str):
        """Pattern: Parallel - Trigger sub-agents simultaneously (Section 3)."""
        tasks = [
            (weather_gatherer, f"Gather telemetry: {context}"),
            (vision_analyst, f"Analyze terrain: {context}")
        ]
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_agent = {executor.submit(agent.chat, task): agent for agent, task in tasks}
            return {future_to_agent[f].name: f.result() for f in concurrent.futures.as_completed(future_to_agent)}

    def run(self, user_input: str, responder_name: str = None):
        """Pattern: Loop - Manage the interaction lifecycle (Section 6)."""
        
        # Idempotency Check (Section 5)
        if responder_name:
            registry = load_registry()
            if registry.get(responder_name, {}).get("status") == "COMPLETE":
                return f"✅ Mission for {responder_name} already resolved."

        # Parallel Perception
        data_snapshot = self.execute_parallel_gathering(user_input)
        
        # Reasoning (Synthesis)
        synthesis_prompt = f"Assessment data: {data_snapshot}. Finalize safety status and directives."
        response = self.director.chat(synthesis_prompt)
        
        # Persistence
        if responder_name:
            update_registry(responder_name, {"status": "COMPLETE", "data": data_snapshot})
            
        return response

# 3. Singleton Instance
studio = FloodPulseStudio(floodpulse_director)

def run_mission(user_input: str, responder_name: str = None):
    """Entry point for the Studio interaction loop."""
    print(f"📡 {floodpulse_director.name}: Starting Studio Interaction Loop...")
    return studio.run(user_input, responder_name)