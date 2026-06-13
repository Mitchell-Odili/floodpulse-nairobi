import asyncio
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.genai import Client
from levels.level_1.agents.orchestrator import floodpulse_director

load_dotenv()

# Initialize the client using the .env variables
client = Client(
    vertexai=os.getenv("USE_VERTEX_AI") == "true",
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION")
)

# Initialize session with metadata for state templating
# This allows sub-agents to access {responder_name}, {latitude}, etc.
async def run_mission():
    session_service = InMemorySessionService()
    
    await session_service.create_session(
        app_name="floodpulse_app",
        user_id="user_01",
        session_id="session_01",
        metadata={
            "responder_name": "Juma",
            "latitude": -1.3165,
            "longitude": 36.8135
        }
    )
    
    runner = Runner(
        app_name="floodpulse_app",
        agent=floodpulse_director,
        session_service=session_service,
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text="Perform a flood risk assessment for the active mission.")]
    )

    print("🚀 FloodPulse Mission Control Online")
    print("--- Starting Mission ---")

    # Run the mission loop
    for update in runner.run(
        session_id="session_01",
        user_id="user_01",
        new_message=user_message
    ):

    # Handle the output from the structured Director
        print(update)

    # Access the final structured result (MissionContext)
    final_session = await session_service.get_session("session_01")
    mission_data = final_session.metadata.get("mission_data")

    if mission_data:
        print(f"\n--- Mission Data Captured ---")
        print(f"Responder: {mission_data.get('responder_name')}")
        print(f"Risk Level: {mission_data.get('risk_level')}")

    print("--- Mission Complete ---")

if __name__ == "__main__":
    # Start the async event loop
    asyncio.run(run_mission())